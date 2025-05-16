# src/a3/crew.py

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool

# Import your tools (ensure these files are correct from previous steps)
from a3.tools.ComfyUITool import ComfyUITool
from a3.tools.FreesoundTool import FreesoundTool

# Import the necessary LLM class
from langchain_openai import ChatOpenAI

# --- Define your LLM ---
llm_model = "o3-mini" # Confirmed model identifier

# Ensure we use the official OpenAI API base
llm_api_base = os.getenv("OPENAI_API_BASE")
if llm_api_base:
    print(f"Warning: OPENAI_API_BASE is set ({llm_api_base}), but using official OpenAI API. Ignoring API base.")
    llm_api_base = None # Override to ensure default is used

# Get API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY environment variable not found. OpenAI API calls will likely fail.")

try:
    # Configure LLM parameters for official OpenAI API
    llm_config = {
        "model": llm_model,
        "api_key": openai_api_key,
        "temperature": 1.0,  # Keep supported temperature
        # --- Attempt to disable 'stop' via model_kwargs ---
        #"model_kwargs": {"stop": None} # Pass stop=None via model_kwargs
        # If this doesn't work, the next thing to try is:
        "model_kwargs": {"stop": []}
    }

    # Initialize the LLM instance
    llm = ChatOpenAI(**llm_config)
    print(f"LLM Initialized with model: {llm_model}, temperature: 1.0. Attempting to disable stop sequences via model_kwargs={{'stop': None}}.")

except Exception as e:
    print(f"Fatal Error Initializing LLM: {e}")
    print("Please check your LLM configuration and ensure OPENAI_API_KEY is correctly set.")
    raise


@CrewBase
class GameBuilderCrew:
    # Paths relative to this file (src/a3/) - Assuming they are correct
    agents_config = 'config/agents.yaml'
    tasks_config  = 'config/tasks.yaml'

    # --- Tool Definitions ---
    @tool
    def comfyui(self) -> ComfyUITool:
         # Ensure ComfyUITool uses the latest corrected __init__
         return ComfyUITool(server_url="http://127.0.0.1:8188")

    @tool
    def freesound(self) -> FreesoundTool:
         # Ensure FreesoundTool uses the latest corrected __init__
         # Remember to set FREESOUND_API_KEY environment variable
         return FreesoundTool(api_key="", output_dir="sounds")

    # --- Agent Definitions (Ensure llm=llm is passed to ALL agents) ---
    @agent
    def main_coder(self) -> Agent:
        return Agent(
                config=self.agents_config['main_coder'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def ui_ux_designer(self) -> Agent:
         return Agent(
                config=self.agents_config['ui_ux_designer'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def narrative_designer(self) -> Agent:
        return Agent(
                config=self.agents_config['narrative_designer'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def map_designer(self) -> Agent:
        return Agent(
                config=self.agents_config['map_designer'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def npc_ai_designer(self) -> Agent:
        return Agent(
                config=self.agents_config['npc_ai_designer'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def inventory_quest_designer(self) -> Agent:
        return Agent(
                config=self.agents_config['inventory_quest_designer'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def image_assets_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['image_assets_generator'],
            tools=[self.comfyui()],
            llm=llm, # Pass configured LLM
            verbose=True
        )

    @agent
    def audio_assets_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['audio_assets_generator'],
            tools=[self.freesound()],
            llm=llm, # Pass configured LLM
            verbose=True
        )

    @agent
    def asset_integrator(self) -> Agent:
        return Agent(
                config=self.agents_config['asset_integrator'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def tester_debugger(self) -> Agent:
        return Agent(
                config=self.agents_config['tester_debugger'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def template_integrator(self) -> Agent:
        return Agent(
                config=self.agents_config['template_integrator'],
                llm=llm, # Pass configured LLM
                verbose=True
            )

    @agent
    def project_coordinator(self) -> Agent:
        return Agent(
                config=self.agents_config['project_coordinator'],
                llm=llm, # Pass configured LLM
                verbose=True
            )


    # --- Task Definitions ---
    @task
    def game_engine_development(self) -> Task:
         return Task(config=self.tasks_config['game_engine_development'])
    @task
    def ui_development(self) -> Task:
        return Task(config=self.tasks_config['ui_development'])
    @task
    def narrative_design(self) -> Task:
        return Task(config=self.tasks_config['narrative_design'])
    @task
    def map_design(self) -> Task:
        return Task(config=self.tasks_config['map_design'])
    @task
    def npc_ai_development(self) -> Task:
        return Task(config=self.tasks_config['npc_ai_development'])
    @task
    def inventory_and_quest_system(self) -> Task:
        return Task(config=self.tasks_config['inventory_and_quest_system'])
    @task
    def generate_visual_assets(self) -> Task:
        return Task(config=self.tasks_config['generate_visual_assets'])
    @task
    def generate_audio_assets(self) -> Task:
        return Task(config=self.tasks_config['generate_audio_assets'])
    @task
    def integrate_assets(self) -> Task:
        return Task(config=self.tasks_config['integrate_assets'])
    @task
    def testing_and_quality_assurance(self) -> Task:
        return Task(config=self.tasks_config['testing_and_quality_assurance'])
    @task
    def game_deployment(self) -> Task:
        return Task(
            config=self.tasks_config['game_deployment'],
            output_file='index.html' # Ensure this output file is desired
        )


    # --- Crew Definition ---
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # Use the list of agent instances created by @agent decorators
            tasks=self.tasks,   # Use the list of task instances created by @task decorators
            process=Process.sequential,
            verbose=True
        )