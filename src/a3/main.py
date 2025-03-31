#!/usr/bin/env python
import sys
import warnings
import time
from datetime import datetime
import yaml
from a3.crew import GameBuilderCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    # Read the game template file
    try:
        with open('templates/game_template.html', 'r') as f:
            template_content = f.read()
            print("Read game template")
    except FileNotFoundError:
        raise Exception("Game template file not found. Make sure 'templates/game_template.html' exists.")

    # Read the game design file (instead of user_instructions)
    try:
        with open('src/a3/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)
            print("Read game design")
    except FileNotFoundError:
        raise Exception("Game design file not found. Make sure 'config/gamedesign.yaml' exists.")

    # Provide game-specific inputs to the crew
    inputs = {
        "game_template": template_content,
        "game_title": "Resign and Reborn",
        "game": examples['example4_rpg']
    }
    
    # Retry loop in case of rate limit errors
    while True:
        try:
            final_game_code = GameBuilderCrew().crew().kickoff(inputs=inputs)
            break  # Break out of loop if successful
        except Exception as e:
            if "rate limit" in str(e).lower():
                print("Rate limit hit. Retrying in 30 seconds...")
                time.sleep(30)
            else:
                raise Exception(f"An error occurred while running the crew: {e}")

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("Final integrated game code:")
    print(final_game_code)
    

def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        with open('templates/game_template.html', 'r') as f:
            template_content = f.read()
        with open('src/a3/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)
            print("Read game design for training")
    except FileNotFoundError as e:
        raise Exception(f"Required file not found: {e}")

    inputs = {
        "game_template": template_content,
        "game_title": "Resign and Reborn",
        "game": examples['example4_rpg']
    }

    try:
        GameBuilderCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GameBuilderCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    try:
        with open('templates/game_template.html', 'r') as f:
            template_content = f.read()
        with open('src/a3/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)
            print("Read game design for testing")
    except FileNotFoundError as e:
        raise Exception(f"Required file not found: {e}")

    inputs = {
        "game_template": template_content,
        "game_title": "Resign and Reborn",
        "game": examples['example4_rpg']
    }

    try:
        GameBuilderCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
