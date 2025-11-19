# systems.py
from __future__ import annotations
from events import (
    SceneId, ItemId,
    SceneChangeRequested, SceneChanged,
    ItemUseRequested, ItemUsed,
    ItemAcquired, PlotAdvanced,
)
from game_state import GameState


# ---- Scene change ----
def handle_scene_change(state: GameState, ev: SceneChangeRequested):
    prev = state.current_scene
    state.current_scene = ev.to_scene
    return SceneChanged(new_scene=ev.to_scene, prev_scene=prev)


# ---- SceneChanged -> narrative ----
def handle_scene_changed(state: GameState, ev: SceneChanged):
    s = ev.new_scene

    if s == SceneId.TOWN:
        if ev.prev_scene is None:
            return PlotAdvanced(
                plot="MAIN", step="INTRO",
                text="You arrive in a quiet town. Rumors speak of ruins deep in the forest."
            )
        return PlotAdvanced(
            plot="MAIN", step="BACK_TOWN",
            text="You return to town. The warm lights feel comforting."
        )

    if s == SceneId.FOREST:
        if not state.get_flag("key_hint_shown"):
            state.set_flag("key_hint_shown", True)
            return PlotAdvanced(
                plot="MAIN", step="FOREST_ENTER",
                text="The forest is dark and damp. Something metallic glimmers beneath a tree root..."
            )
        return PlotAdvanced(
            plot="MAIN", step="FOREST_BACK",
            text="You step into the forest again. Wind rustles through the leaves."
        )

    if s == SceneId.RUINS:
        if not state.get_flag("ruins_gate_open"):
            return PlotAdvanced(
                plot="MAIN", step="RUINS_LOCKED",
                text="You reach the ruins. The massive stone gate is tightly shut. A keyhole is carved in the stone."
            )
        return PlotAdvanced(
            plot="MAIN", step="RUINS_OPEN",
            text="The ancient gate stands open, cold steps leading down into darkness."
        )


# ---- Use item ----
def handle_item_use(state: GameState, ev: ItemUseRequested):
    if ev.item == ItemId.POTION:
        if not state.has_item(ItemId.POTION):
            return PlotAdvanced(plot="MAIN", step="NO_POTION",
                                text="You don't have a potion.")
        state.remove_item(ItemId.POTION, 1)
        return (
            ItemUsed(item=ItemId.POTION),
            PlotAdvanced(plot="MAIN", step="HEAL",
                         text="You drink the healing potion and feel revitalized.")
        )

    if ev.item == ItemId.KEY:
        if state.current_scene != SceneId.RUINS:
            return PlotAdvanced(plot="MAIN", step="KEY_WRONG_PLACE",
                                text="The key doesn't fit anything here. Perhaps the ruin's gate.")
        if state.get_flag("ruins_gate_open"):
            return PlotAdvanced(plot="MAIN", step="GATE_ALREADY_OPEN",
                                text="The gate is already open.")
        if not state.has_item(ItemId.KEY):
            return PlotAdvanced(plot="MAIN", step="NO_KEY",
                                text="You don't have the key.")
        state.remove_item(ItemId.KEY, 1)
        state.set_flag("ruins_gate_open", True)
        return (
            ItemUsed(item=ItemId.KEY),
            PlotAdvanced(plot="MAIN", step="GATE_OPEN",
                         text="The ancient mechanism turns with a heavy click. The stone gate opens.")
        )


# ---- Pick up item (NO re-emitting ItemAcquired) ----
def handle_pickup(state: GameState, ev: ItemAcquired):
    if ev.item == ItemId.KEY:
        if state.get_flag("key_taken"):
            return PlotAdvanced(plot="MAIN", step="ALREADY_HAVE_KEY",
                                text="You already picked up the Ancient Key.")
        state.set_flag("key_taken", True)

    state.add_item(ev.item, 1)
    return PlotAdvanced(plot="MAIN", step="GET_ITEM",
                        text=f"You picked up: {state.item_title(ev.item)}.")


# ---- Registry ----
def register_all_systems(bus, state: GameState):
    bus.subscribe(SceneChangeRequested, lambda ev: handle_scene_change(state, ev))
    bus.subscribe(SceneChanged,         lambda ev: handle_scene_changed(state, ev))
    bus.subscribe(ItemUseRequested,     lambda ev: handle_item_use(state, ev))
    bus.subscribe(ItemAcquired,         lambda ev: handle_pickup(state, ev))
