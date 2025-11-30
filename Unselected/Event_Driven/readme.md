# Event-Driven Adventure Game

## *1. Platform, Runtime, and Dependencies*

> The Event-Driven Architecture version of the project is implemented in **Python 3.10+**.

**Platform:**
- Python 3.10 or above  
- Operating System: Windows / macOS / Linux  
- GUI Framework: tkinter (bundled with standard Python installations)  
- No external libraries are required  

All code for the Event-Driven version is located under:
```
Event-Driven/
```

---

## *2. How to Run the Event-Driven Version*

1. Install Python 3.10 or above.  
2. Ensure tkinter is available (default on Windows/macOS).  
3. Open a terminal and navigate to the Event-Driven directory:
   ```bash
   cd Selected/Event-Driven
   ```
4. Run the game:
   ```bash
   python main.py
   ```

---

## *3. Overview of the Event-Driven Architecture*

> The Event-Driven Architecture organizes the system around independent components that communicate exclusively through events.  
> Instead of invoking methods directly, components publish events to a central **EventBus** and subscribe only to the events they care about.

In this game, every major gameplay action — moving between scenes, picking up items, using items, and advancing the story — is modeled as an event flowing through the system.  
This creates a clean separation between UI, game logic, and game state.

---

## *4. Advantages (Pros)*

* Loose coupling: UI, logic, and state do not directly call each other.  
* Highly extensible: new scenes, items, or mechanics can be added by introducing new events and handlers.  
* Clear separation of responsibilities: Systems handle logic, UI handles presentation, GameState stores data.  
* Natural fit for game behavior: Player actions naturally map to events.  

---

## *5. Disadvantages (Cons)*

* Harder to trace: event chains can be non-linear, involving multiple handlers.  
* EventBus is a single point of failure: incorrect registration or dispatch breaks the entire flow.  
* Event order matters: publishing too early or too late can lead to inconsistent states.  

---

## *6. UML Diagram*
