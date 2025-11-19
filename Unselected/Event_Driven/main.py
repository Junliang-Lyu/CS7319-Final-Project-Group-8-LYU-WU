# main.py
from __future__ import annotations
from event_bus import EventBus
from game_state import GameState
from systems import register_all_systems
from events import (
    SceneId, ItemId,
    SceneChangeRequested, ItemUseRequested,
    PlotAdvanced
)


def attach_basic_log(bus: EventBus, state: GameState) -> None:
    def on_plot(ev: PlotAdvanced):
        print(f"[STORY] {ev.text}")
        state.append_log(ev.text)
    bus.subscribe(PlotAdvanced, on_plot)


def demo_flow(bus: EventBus, state: GameState) -> None:
    print("=== DEMO START ===")
    bus.publish(SceneChangeRequested(SceneId.FOREST))
    bus.publish(SceneChangeRequested(SceneId.RUINS))
    bus.publish(ItemUseRequested(ItemId.KEY))
    bus.publish(SceneChangeRequested(SceneId.RUINS))
    print("=== DEMO END ===")


def main() -> None:
    print("[main] start")
    bus = EventBus()
    state = GameState()
    register_all_systems(bus, state)
    attach_basic_log(bus, state)
    print("[main] systems ready")

    try:
        import ui
        print("[main] ui loaded")
        app = ui.UI(bus, state)
        print("[main] entering UI mainloop")
        app.run()
    except Exception as e:
        import traceback
        print("[main] UI failed, fallback demo:", repr(e))
        traceback.print_exc()
        demo_flow(bus, state)


if __name__ == "__main__":
    main()
