# game_state.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
from events import SceneId, ItemId


@dataclass
class GameState:
    current_scene: SceneId = SceneId.TOWN
    inventory: Dict[ItemId, int] = field(default_factory=dict)
    flags: Dict[str, bool] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)

    def append_log(self, text: str) -> None:
        self.log.append(text)

    # ----- Titles / Text -----
    def get_scene_title(self) -> str:
        return {
            SceneId.TOWN: "Town",
            SceneId.FOREST: "Forest",
            SceneId.RUINS: "Ruins",
        }.get(self.current_scene, "Unknown")

    def scene_description(self, s: SceneId) -> str:
        return {
            SceneId.TOWN: "A quiet town where your journey begins.",
            SceneId.FOREST: "A dark forest rumored to hide ancient secrets.",
            SceneId.RUINS: "An ancient stone ruin lies ahead, sealed shut.",
        }[s]

    def item_title(self, item: ItemId) -> str:
        titles = {
            ItemId.KEY: "Ancient Key",
            ItemId.POTION: "Healing Potion",
        }
        return titles.get(item, "Unknown")

    # ----- Inventory / Flags -----
    def add_item(self, item: ItemId, qty: int = 1) -> None:
        if qty <= 0:
            return
        self.inventory[item] = self.inventory.get(item, 0) + qty

    def remove_item(self, item: ItemId, qty: int = 1) -> None:
        if qty <= 0:
            return
        cur = self.inventory.get(item, 0)
        if cur <= 0:
            return
        remain = cur - qty
        if remain > 0:
            self.inventory[item] = remain
        else:
            self.inventory.pop(item, None)

    def has_item(self, item: ItemId) -> bool:
        return self.inventory.get(item, 0) >= 1

    def set_flag(self, k: str, v: bool = True) -> None:
        self.flags[k] = v

    def get_flag(self, k: str) -> bool:
        return self.flags.get(k, False)
