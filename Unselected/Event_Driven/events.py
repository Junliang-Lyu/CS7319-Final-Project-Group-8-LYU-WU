from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Dict

class SceneId(Enum):
    TOWN = auto()
    FOREST = auto()
    RUINS = auto()

class ItemId(Enum):
    KEY = auto()
    POTION = auto()

class PlotId(Enum):
    MAIN = auto()

@dataclass(frozen=True)
class BaseEvent:
    pass

@dataclass(frozen=True)
class SceneChangeRequested(BaseEvent):
    to_scene: SceneId

@dataclass(frozen=True)
class ItemUseRequested(BaseEvent):
    item: ItemId

@dataclass(frozen=True)
class SceneChanged(BaseEvent):
    new_scene: SceneId
    prev_scene: Optional[SceneId]

@dataclass(frozen=True)
class ItemAcquired(BaseEvent):
    item: ItemId
    source: str = ""

@dataclass(frozen=True)
class ItemUsed(BaseEvent):
    item: ItemId

@dataclass(frozen=True)
class PlotTrigger(BaseEvent):
    trigger: str
    context: Optional[Dict[str, Any]] = None

@dataclass(frozen=True)
class PlotAdvanced(BaseEvent):
    plot: PlotId
    step: str
    text: str
