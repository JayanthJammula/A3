#!/usr/bin/env python
import warnings
import time
import yaml
import types
import os
from datetime import datetime

# Shim for litellm/crewai OpenAIObject compatibility
try:
    import openai._models  # noqa: F401
except ModuleNotFoundError:
    from openai.openai_object import OpenAIObject
    shim = types.ModuleType("openai._models")
    shim.BaseModel = OpenAIObject
    import sys
    sys.modules["openai._models"] = shim

from a3.crew import GameBuilderCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    # Load HTML template
    tpl_path = os.path.join("templates", "game_template.html")
    if not os.path.exists(tpl_path):
        raise FileNotFoundError("Missing templates/game_template.html")
    with open(tpl_path, "r") as f:
        template = f.read()

    # Load game design YAML
    gd_path = os.path.join("src", "a3", "config", "gamedesign.yaml")
    if not os.path.exists(gd_path):
        raise FileNotFoundError("Missing src/a3/config/gamedesign.yaml")
    with open(gd_path, "r", encoding="utf-8") as f:
        examples = yaml.safe_load(f)

    inputs = {
        "game_template": template,
        "game_title":    "Resign and Reborn",
        "game":          examples,
    }

    # Build and run the Crew (tools are bound via _tool_functions in crew.py)
    crew = GameBuilderCrew().crew()

    # Kick off with retry on rate limits
    while True:
        try:
            final_code = crew.kickoff(inputs=inputs)
            break
        except Exception as e:
            if "rate limit" in str(e).lower():
                print("Rate limit hit, retrying in 30 seconds...")
                time.sleep(30)
            else:
                raise

    print("\n########################")
    print("Final integrated game code:")
    print("########################\n")
    print(final_code)

if __name__ == "__main__":
    run()
