Resign and Reborn
Resign and Reborn is an HTML5 tile-based RPG game built using Phaser.js (v3.55.2). The game is packaged as a single, self-contained HTML file with embedded CSS and JavaScript. It is designed to run on both desktop and mobile browsers, featuring smooth scene transitions, interactive dialogue, and responsive UI elements.

Overview
The game is set on a 20x20 tile-based map. It features:

A central town enclosed by a fence, containing four houses and two interactive NPCs.

A surrounding forest with two types of ground tiles:

Grass: Standard walkable terrain.

HighGrass: Tiles that may trigger a random encounter (5% chance) when stepped on.

A dialogue system that allows branching dialogue when interacting with NPCs.

A turn-based card battle system triggered by random encounters.

Multiple scenes including a narrative-driven PrologueScene, an ExplorationScene, a CardBattleScene, and an optional SkillTreeScene.

A fully integrated UI including a main menu, settings, instructions, HUD, quest log, and inventory panel.

Features
Tile-Based Map: A dynamic 20x20 grid with a central town and forest areas.

Player Controls:

Desktop: Move using arrow keys; interact using SPACE; open instructions with I and the main menu with M.

Mobile/Tablet: On-screen D-pad in the bottom-left and action buttons in the bottom-right for interactions, inventory toggling, and exiting NPC dialogue.

Responsive UI: Clean, mobile-friendly design with a centered game container and intuitive UI overlays.

Dialogue System: NPC interactions feature multi-page, branching dialogue that pauses movement during conversations.

Random Encounters: Forest "highGrass" tiles can trigger a turn-based card battle.

Scene Transitions: Smooth transitions between the prologue, exploration, battle, and skill tree scenes.

Integrated Crew System: Developed with a modular crew approach where each agent (e.g., main coder, UI/UX designer, narrative designer, etc.) contributed to different aspects of the game.

Run the Game:

Simply open the index.html file in any modern web browser (Chrome, Firefox, Safari, or Edge). No additional server setup is needed.

Mobile Access:

The game is fully responsive. When accessed on mobile or tablet devices, on-screen controls (a D-pad and action buttons) will automatically appear in the bottom corners.

File Structure
index.html:
The complete, deployable HTML file containing all embedded CSS and JavaScript code.

templates/game_template.html:
The reference game template used during development (if applicable).

src/a3/config/gamedesign.yaml:
Contains detailed game design instructions and specifications.

config/agents.yaml:
Configuration for the various development agents (e.g., main coder, UI/UX designer, narrative designer, etc.).

config/tasks.yaml:
Definitions of the development tasks (e.g., game engine development, UI development, narrative design, etc.).

crew.py, main.py:
Scripts for running the modular crew system that integrates contributions from multiple agents.

Development
The project is developed using a modular "crew" approach. Each agent is responsible for a different aspect of the game:

Main Coder: Implements the core game engine with Phaser.js.

UI/UX Designer: Develops the responsive HTML and CSS for all UI elements.

Narrative Designer: Crafts the narrative content and branching dialogue.

Map Designer: Designs the 20x20 tile-based map and game environment.

NPC AI Designer: Implements interactive NPC behaviors and enemy logic.

Inventory & Quest Designer: Builds the systems for managing the player's inventory and active quests.

Tester/Debugger: Provides debugging code and test cases to ensure quality.

Template Integrator: Consolidates all components into a single, self-contained HTML file.

Project Coordinator: Oversees the integration of all elements to ensure cohesive delivery.

The crew system is orchestrated using Python (see crew.py and main.py), and configuration files in YAML format (agents.yaml, tasks.yaml, gamedesign.yaml).

Controls
Desktop Controls
Movement: Use the arrow keys (each press moves the player one 32x32 tile).

Interaction: Press SPACE to interact with NPCs, houses, or objects.

UI Navigation:

Press I to view instructions.

Press M to open the main menu.

Mobile/Tablet Controls
Movement: On-screen D-pad located in the bottom-left corner.

Action Buttons: In the bottom-right corner:

Interact: Triggers interactions (same as SPACE on desktop).

Inventory: Toggles the inventory panel.

Exit Dialogue: Cancels NPC dialogue (visible only when in dialogue).

Testing and Quality Assurance
The game includes various debug logs and test cases integrated into the code.

Use the provided testing routines (see main.py) to run QA tests.

Check the browser console for messages and error logs during gameplay.
