# Find Treasure in SMU – Layered Architecture Version

This README describes the Layered Architecture implementation of the game “Find Treasure in SMU”.

The goal of this version is to organize the code into clear layers:
- Presentation
- Application
- Domain
- Infrastructure

It is intended to be submitted together with the layered version of the code.

---

## 1. Project Overview

The game is a small, text-based adventure:

- Start at the Title Screen.
- Visit Caruth Hall.
- Go to Junkins Building.
- Finish in the Library, where the player can open a safe and find the treasure.

The player interacts with the game by clicking buttons in a simple UI.
Each scene presents a few options (inspect objects, talk to NPCs, move to the next building).
Progress is driven by a shared PlayerState.

---

## 2. Layered Architecture

The code is organized into four logical layers:

### 2.1 Presentation Layer

Responsible for drawing UI elements and handling player input.

Contains:
- ui.py – buttons, scene text rendering, message popups, password input screen, ending screen.
- Scene modules in scenes/ – how each scene looks and which options the player can choose.

### 2.2 Application Layer

Controls the high-level flow of the game.

Contains:
- main.py – the main game loop that decides which scene to run next.

### 2.3 Domain Layer

Represents the core game logic and state.

Contains:
- player.py – the PlayerState class:
  - Tracks flags such as saw_poster, talked_professor, got_key.
  - Stores collected items in an items list.
  - Provides add_item(name) to record new items.

### 2.4 Infrastructure Layer

Provides shared technical services.

Contains:
- settings.py – pygame initialization, window size, fonts, colors, helper function for loading background images.
- assets/ – image files for background:
  - title_bg.png
  - caruth_bg.png
  - junkins_bg.png
  - library_bg.png

The layers depend only in a top-down direction:

Presentation → Application → Domain → Infrastructure

There is no circular dependency between layers.

---

## 3. Code Structure

A typical folder structure for the layered implementation:

project_root/
├── main.py
├── settings.py
├── player.py
├── ui.py
├── scenes/
│   ├── title.py
│   ├── caruth.py
│   ├── junkins.py
│   └── library.py
└── assets/
    ├── title_bg.png
    ├── caruth_bg.png
    ├── junkins_bg.png
    └── library_bg.png

### Key files

- main.py
  - Runs the main loop.
  - Tracks the current scene name: "title", "caruth", "junkins", "library", or "end".
  - Calls the corresponding scene and updates current_scene.

- ui.py
  - Provides reusable UI helpers:
    - draw_button
    - draw_scene
    - draw_inventory
    - message_scene
    - password_input_scene
    - ending_scene

- player.py
  - Defines PlayerState:
    - saw_poster
    - talked_professor
    - got_key
    - items list

- settings.py
  - Initializes pygame, window settings, fonts, colors.
  - Loads background images:
    - BG_TITLE
    - BG_CARUTH
    - BG_JUNKINS
    - BG_LIBRARY

- scenes/
  - title.py – title screen with START and QUIT.
  - caruth.py – Caruth Hall scene.
  - junkins.py – Junkins Building scene.
  - library.py – Library scene with safe & ending.

Each scene returns the name of the next scene or "end".

---

## 4. Flow of the Layered Game

1. Start in "title".
2. Player clicks START → calls caruth_scene().
3. Player checks bulletin, talks to professor → unlocks Junkins.
4. Player gets key from Junkins → unlocks Library.
5. In Library:
   - Must have key
   - Must have seen poster (safe code)
   - Then password input appears
6. Correct code → ending_scene → "end".

---

## 5. How to Run

Install pygame:
pip install pygame

Run:
python main.py

---

## 6. Why This Layered Design Was Used

- Clear responsibilities per file
- Simple, linear control flow
- Easier to debug compared to event-driven version
- No event ordering issues
- Perfect fit for a small, scene-based adventure game
- All UI and state logic are centralized logically

Therefore, the Layered Architecture is chosen as the final architecture.
