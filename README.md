# CS5-7319-Final-Project-Group-8-LYU-WU
# Architecture Comparison and Rationale

## Event-Driven Architecture vs Layered Architecture

### 1. Structural Comparison

**Event-Driven Architecture** - Uses an EventBus as the central
communication hub. - UI publishes events; handlers subscribe to and
process these events. - Highly decoupled and flexible.

**Layered Architecture** - A clear top-down structure: Presentation →
Application → Domain → Infrastructure. - Scenes and UI follow a
predictable call flow. - Easier to understand and maintain for smaller
projects.

### 2. Control Flow

**Event-Driven** - Indirect control flow: actions trigger events, events
activate handlers, handlers update state. - Hard to trace end-to-end
execution.

**Layered** - Direct and linear: GameMain calls scenes, scenes call UI
and PlayerState. - Much easier to trace and debug.

### 3. Coupling and Dependencies

**Event-Driven** - Loose coupling among components. - EventBus becomes a
central dependency that must be carefully managed.

**Layered** - Moderate coupling between layers, but simple and
predictable. - Dependencies are transparent and easier to maintain.

### 4. Extensibility and Scalability

**Event-Driven** - Very scalable and extensible: new features = new
events + new handlers. - Great for complex interactions, multiple
subsystems reacting simultaneously.

**Layered** - Extensible but less flexible than event-driven. - Best for
linear or moderately complex flows.

### 5. Debugging and Testing

**Event-Driven** - Debugging is harder due to event ordering and hidden
execution paths. - Our prototype encountered a real event-sequencing
bug.

**Layered** - Debugging is straightforward due to explicit call paths. -
No risk of event timing issues.

### 6. Suitability for This Game

**Event-Driven** - Overkill for a small, linear adventure game.

**Layered** - Perfectly matches the game's sequential structure (Caruth
→ Junkins → Library). - Scenes map cleanly to the layered structure.

------------------------------------------------------------------------

## Why We Chose the Layered Architecture

1.  **Simplicity and Clarity**\
    The layered architecture provides clear boundaries, making it ideal
    for teaching, grading, and understanding.

2.  **Ease of Debugging**\
    Sequential call paths avoid the complexity of asynchronous event
    chains.

3.  **Better Fit for Linear Story-Based Games**\
    The game's flow is inherently sequential rather than reactive.

4.  **Lower Architectural Risk**\
    Event-driven systems require careful management of event handling
    and timing.\
    Layered systems avoid these pitfalls.

5.  **Observed Issues in Event-Driven Prototype**\
    The event-driven version produced a real ordering bug, highlighting
    the complexity and fragility of the approach.

**Conclusion:**\
The Layered Architecture is the optimal choice for a small, scene-based
narrative game like *Find Treasure in SMU*, balancing clarity,
maintainability, and simplicity while avoiding unnecessary complexity.
