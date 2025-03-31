from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class GameBuilderCrew:
    """GameBuilder crew for the Magical 2D RPG Game using Phaser.js"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def main_coder(self) -> Agent:
        # The main coder develops the game engine and integrates code outputs from other agents.
        return Agent(
            config=self.agents_config['main_coder'],
            verbose=True
        )

    @agent
    def ui_ux_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_ux_designer'],
            verbose=True
        )

    @agent
    def narrative_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['narrative_designer'],
            verbose=True
        )

    @agent
    def map_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['map_designer'],
            verbose=True
        )

    @agent
    def npc_ai_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['npc_ai_designer'],
            verbose=True
        )

    @agent
    def inventory_quest_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['inventory_quest_designer'],
            verbose=True
        )

    @agent
    def tester_debugger(self) -> Agent:
        return Agent(
            config=self.agents_config['tester_debugger'],
            verbose=True
        )

    @agent
    def template_integrator(self) -> Agent:
        return Agent(
            config=self.agents_config['template_integrator'],
            verbose=True
        )
    
    @agent
    def project_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['project_coordinator'],
            verbose=True
        )

    @task
    def game_engine_development(self) -> Task:
        return Task(
            config=self.tasks_config['game_engine_development']
        )

    @task
    def ui_development(self) -> Task:
        return Task(
            config=self.tasks_config['ui_development']
        )

    @task
    def narrative_design(self) -> Task:
        return Task(
            config=self.tasks_config['narrative_design']
        )

    @task
    def map_design(self) -> Task:
        return Task(
            config=self.tasks_config['map_design']
        )

    @task
    def npc_ai_development(self) -> Task:
        return Task(
            config=self.tasks_config['npc_ai_development']
        )

    @task
    def inventory_and_quest_system(self) -> Task:
        return Task(
            config=self.tasks_config['inventory_and_quest_system']
        )

    @task
    def testing_and_quality_assurance(self) -> Task:
        return Task(
            config=self.tasks_config['testing_and_quality_assurance']
        )

    @task
    def game_deployment(self) -> Task:
        return Task(
            config=self.tasks_config['game_deployment'],
            output_file='index.html'
        )

    @crew
    def crew(self) -> Crew:
        # Executes all tasks sequentially.
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
