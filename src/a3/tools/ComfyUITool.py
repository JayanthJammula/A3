# src/a3/tools/ComfyUITool.py
import os
import requests
import time
import json
from crewai.tools.base_tool import BaseTool
from typing import Optional, List, Dict, Any # Keep Any for __init__
from pydantic import BaseModel, Field, ValidationError

# --- Define Pydantic Input Model ---
# This explicitly tells CrewAI what arguments _run expects
class ComfyUIToolInput(BaseModel):
    prompts: List[str] = Field(..., description="List of text prompts for image generation.")
    size: Optional[str] = Field(default="1024x1024", description="Image dimensions (e.g., '1024x1024'). Defaults to '1024x1024'.")


class ComfyUITool(BaseTool):
    # --- Define tool attributes required by BaseTool ---
    name: str = "comfyui"
    description: str = (
        "Generates multiple images via the local ComfyUI server based on a list of prompts. "
        "Input MUST be a dictionary containing 'prompts' (list of strings) and optional 'size' (string, e.g., '1024x1024')."
    )
    args_schema: type[BaseModel] = ComfyUIToolInput # Link the explicit schema

    # --- Define tool-specific fields ---
    server_url: str
    output_dir: str

    # Simplified __init__ - BaseTool handles fields via Pydantic
    def __init__(self, server_url: str = "http://127.0.0.1:8188", **data: Any):
         resolved_output_dir = "images"
         # Pass server_url and resolved output_dir explicitly to super()
         # data allows other Pydantic fields (like description if not set above) to be passed
         super().__init__(server_url=server_url, output_dir=resolved_output_dir, **data)
         os.makedirs(self.output_dir, exist_ok=True)
         print(f"ComfyUITool initialized with explicit schema and run signature. Output directory: {os.path.abspath(self.output_dir)}")


    # --- Use EXPLICIT signature for _run, matching args_schema ---
    # CrewAI should now validate input against ComfyUIToolInput BEFORE calling this
    def _run(self, prompts: List[str], size: Optional[str] = "1024x1024") -> str:
        """
        Generates multiple images using ComfyUI based on a validated list of prompts and size.
        Args:
            prompts (List[str]): Validated list of text prompts.
            size (Optional[str]): Validated image dimensions string. Defaults internally if None/omitted.
        Returns:
            JSON string: {"success": true, "results": [...]} or {"success": false, "error": "..."}
        """
        # Arguments 'prompts' and 'size' should have been validated by CrewAI/Pydantic by this point
        print(f"ComfyUITool _run received validated args: prompts={'list' if isinstance(prompts, list) else type(prompts)}, size='{size}'")

        # Ensure size has a default value if validation allowed None
        effective_size = size if size is not None else "1024x1024"

        # --- Looping/generation logic (uses validated args) ---
        results = []
        overall_success = True

        for i, prompt_text in enumerate(prompts):
            filename = f"image_{i}.png"
            full_path = os.path.abspath(os.path.join(self.output_dir, filename))
            print(f"ComfyUITool: Processing item {i}: Generating image '{filename}' with prompt: '{prompt_text[:100]}...'")

            try:
                # Pass the validated or defaulted size
                generated_path = self.generate(prompt_text, effective_size, filename)
                if os.path.exists(generated_path):
                     print(f"ComfyUITool: Success for item {i}. Image saved to {generated_path}")
                     results.append({"index": i, "status": "success", "path": generated_path, "prompt": prompt_text})
                else:
                     error_msg = f"generate method claimed success but file not found at {generated_path}"
                     print(f"ComfyUITool Error for item {i}: {error_msg}")
                     results.append({"index": i, "status": "error", "error": error_msg, "prompt": prompt_text})
                     overall_success = False
            except Exception as e:
                import traceback
                tb_str = traceback.format_exc()
                error_msg = f"Failed to generate image for item {i} ('{filename}'). Error: {e}"
                print(f"ComfyUITool Error for item {i}: {error_msg}\nTraceback:\n{tb_str}")
                results.append({"index": i, "status": "error", "error": str(e), "prompt": prompt_text})
                overall_success = False

        print(f"ComfyUITool: Finished processing batch. Overall Success: {overall_success}")
        return json.dumps({"success": overall_success, "results": results})

    # --- generate method remains unchanged ---
    def generate(self, prompt: str, size: str, filename: str) -> str:
        # (Make sure this uses STRING keys for workflow nodes)
        try:
            w, h = map(int, size.lower().split("x"))
        except ValueError:
            raise ValueError(f"Invalid size format: '{size}'. Must be WIDTHxHEIGHT, e.g. '1024x1024'")

        workflow = {
            "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "AnythingV5.safetensors"}}, # VERIFY THIS FILENAME!
            "5": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
            "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["4", 1]}},
            "3": {"class_type": "KSampler", "inputs": {
                    "seed": int(time.time() * 1000) % (2**32),
                    "steps": 20, "cfg": 8.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
                    "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]
                 }},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
            "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "ComfyUI_AutoGen", "images": ["8", 0]}}
        }

        # API Call
        try:
            res = requests.post(f"{self.server_url}/prompt", json={"prompt": workflow}, timeout=90)
            res.raise_for_status()
            data = res.json()
            pid = data.get("prompt_id")
            if not pid:
                raise RuntimeError(f"No prompt_id in ComfyUI response: {data}")
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                 response_text = e.response.text
                 raise RuntimeError(f"ComfyUI server HTTP error ({e.response.status_code}) on {self.server_url}/prompt: {e}. Response: {response_text}")
            else:
                 raise RuntimeError(f"ComfyUI server connection error ({self.server_url}/prompt): {e}")
        except Exception as e:
             raise RuntimeError(f"Error during ComfyUI /prompt request or response parsing: {e}")

        # Polling
        hist = None
        for i in range(60):
            try:
                h_res = requests.get(f"{self.server_url}/history/{pid}", timeout=10)
                h_res.raise_for_status()
                hist_data = h_res.json()
                if pid in hist_data and "outputs" in hist_data[pid]:
                    hist = hist_data
                    break
            except Exception:
                pass
            time.sleep(1)
        else:
            raise RuntimeError(f"ComfyUI timed out waiting for history (prompt_id: {pid})")

        # Image Extraction
        img_bytes = None
        final_filename_in_comfy = None
        if hist and pid in hist:
            outputs = hist[pid].get("outputs", {})
            for node_id, node_output in outputs.items():
                 if node_id == "9" and "images" in node_output:
                    images = node_output.get("images", [])
                    if images:
                        img_info = images[0]
                        final_filename_in_comfy = img_info.get("filename")
                        if not final_filename_in_comfy: continue
                        try:
                            view_res = requests.get(
                                f"{self.server_url}/view",
                                params={
                                    "filename": final_filename_in_comfy,
                                    "subfolder": img_info.get("subfolder", ""),
                                    "type": img_info.get("type", "output")},
                                timeout=30)
                            view_res.raise_for_status()
                            img_bytes = view_res.content
                            break
                        except Exception as e:
                            print(f"ComfyUITool.generate: Warning - Failed to fetch image view for {final_filename_in_comfy}: {e}")

        if img_bytes is None:
            raise RuntimeError(f"No image data retrieved from ComfyUI history (prompt_id: {pid})")

        # Saving
        output_path = os.path.abspath(os.path.join(self.output_dir, filename))
        try:
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            return output_path
        except IOError as e:
            raise RuntimeError(f"Failed to save image to {output_path}: {e}")