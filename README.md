# Resign and Reborn

**Resign and Reborn** is an immersive HTML5 tile-based RPG game developed using Phaser.js (v3.55.2). Packaged as a single, self-contained HTML file with embedded CSS and JavaScript, the game offers smooth scene transitions, interactive dialogue, and a responsive user interface designed for both desktop and mobile browsers.

---

## Overview

Set on a 20x20 tile-based map, **Resign and Reborn** transports you into a richly detailed world featuring:

- **A Central Town:**  
  A charming town enclosed by a fence that hosts four houses and two interactive NPCs.

- **A Lush Forest:**  
  Surrounding the town is a dense forest filled with standard "grass" tiles and special "highGrass" tiles that hold a 5% chance of triggering a turn-based card battle.

- **Dynamic Gameplay:**  
  Engage in branching dialogues with NPCs, trigger random encounters, and experience a turn-based battle system reminiscent of classic Pokémon games.

- **Multiple Scenes:**  
  Enjoy a narrative-driven prologue that transitions seamlessly into the main exploration, card battle encounters, and even an optional skill tree for character upgrades.

- **Integrated User Interface:**  
  A fully integrated UI features a main menu, settings, instructions, a heads-up display (HUD), quest log, and inventory panel—all styled for an optimal user experience.

- **Modular Crew System:**  
  Developed using a modular “crew” approach, multiple specialized agents (e.g., main coder, UI/UX designer, narrative designer, etc.) contributed to create a cohesive and polished final product.

---

## Features

- **Tile-Based Map:**  
  A dynamic 20x20 grid featuring a central town and surrounding forest with varied terrain:
  - **Town Area:** Enclosed by a fence with 4 houses and 2 NPCs.
  - **Forest Area:** Standard "grass" and special "highGrass" tiles that can trigger random encounters, alongside impassable "tree" tiles.

- **Player Controls:**  
  - **Desktop:** Use arrow keys to move (one 32x32 tile per press), SPACE to interact, I to view instructions, and M for the main menu.
  - **Mobile/Tablet:** On-screen D-pad in the bottom-left for movement and action buttons in the bottom-right for interaction, inventory toggling, and dialogue cancellation.

- **Responsive UI:**  
  A clean, mobile-friendly design with a centered game container and intuitive overlays for the HUD, quest log, and inventory.

- **Dialogue System:**  
  Multi-page, branching dialogue that pauses gameplay during NPC interactions and offers clear numeric choices.

- **Random Encounters:**  
  Special "highGrass" tiles in the forest have a 5% chance to trigger a turn-based card battle.

- **Scene Transitions:**  
  Smooth, explicit transitions between the prologue, exploration, battle, and skill tree scenes.

- **Integrated Crew Workflow:**  
  Built using a modular crew approach with dedicated roles for coding, UI/UX, narrative, map design, NPC AI, inventory/quest systems, quality assurance, and project integration.

---

## How to Run the Game

Simply open the `index.html` file in any modern web browser (Chrome, Firefox, Safari, or Edge). No additional server setup is required.

### Mobile Access

The game is fully responsive. When accessed on mobile or tablet devices, on-screen controls appear in the bottom corners:
- **Bottom Left:** A D-pad for movement.
- **Bottom Right:** Action buttons for interaction, inventory toggling, and an exit dialogue option during NPC conversations.

---

## File Structure

- **index.html:**  
  The final, deployable HTML file containing all embedded CSS and JavaScript code.

- **templates/game_template.html:**  
  The reference game template used during development (if applicable).

- **src/a3/config/gamedesign.yaml:**  
  Contains detailed game design instructions and specifications.

- **config/agents.yaml:**  
  Configuration files for the various development agents (e.g., main coder, UI/UX designer, narrative designer, etc.).

- **config/tasks.yaml:**  
  Definitions of the development tasks (e.g., game engine development, UI development, narrative design, etc.).

- **crew.py, main.py:**  
  Scripts for running the modular crew system that integrates contributions from multiple agents.

---

## Development

The project is developed using a modular "crew" approach. Each agent is responsible for a specific aspect:

- **Main Coder:** Implements the core game engine using Phaser.js.
- **UI/UX Designer:** Creates responsive, polished UI components (HUD, menus, dialogue boxes, etc.).
- **Narrative Designer:** Crafts immersive narrative content and interactive dialogue.
- **Map Designer:** Designs the 20x20 tile-based game map and diverse terrain.
- **NPC AI Designer:** Develops interactive NPC behavior and enemy logic.
- **Inventory & Quest Designer:** Builds systems for managing the player's inventory and quests.
- **Tester/Debugger:** Conducts debugging and quality assurance to ensure a robust final product.
- **Template Integrator:** Consolidates all components into a single, deployable HTML file.
- **Project Coordinator:** Oversees the integration of all elements to ensure a cohesive experience.

The crew system is orchestrated using Python (see `crew.py` and `main.py`), with configuration files in YAML format.

---

## Controls

### Desktop Controls
- **Movement:**  
  Use the arrow keys (each press moves the player one 32x32 tile).
- **Interaction:**  
  Press SPACE to interact with NPCs, houses, or objects.
- **UI Navigation:**  
  - Press I to view instructions.
  - Press M to open the main menu.

### Mobile/Tablet Controls
- **Movement:**  
  On-screen D-pad (located in the bottom-left corner) to move.
- **Action Buttons:**  
  Located in the bottom-right corner:
  - **Interact:** Triggers interactions (same as SPACE on desktop).
  - **Inventory:** Toggles the inventory panel.
  - **Exit Dialogue:** Cancels NPC dialogue (visible only during dialogue).

---

## Testing and Quality Assurance

The game includes debug logs and testing routines integrated into the code.  
- Run the provided testing routines (see `main.py`) to verify that all controls, UI elements, and scene transitions work correctly.
- Check the browser console for messages and error logs during gameplay.

---

## Credits

Developed with contributions from multiple specialized agents:
- **Main Coder**
- **UI/UX Designer**
- **Narrative Designer**
- **Map Designer**
- **NPC AI Designer**
- **Inventory & Quest Designer**
- **Tester/Debugger**
- **Template Integrator**
- **Project Coordinator**

