"""Core utilities for working with ObjectType dicts."""


from typing import Literal, overload
from gmdbuilder.internal_mappings.obj_id import ObjId
from gmdbuilder.internal_mappings.obj_prop import ObjProp
from gmdbuilder.object_types import MoveType, ObjectType


SPAWNING_TRIGGER_IDS = {
    ObjId.Trigger.SPAWN,
    ObjId.Trigger.TOGGLE,
    ObjId.Trigger.STOP,
    ObjId.Trigger.COLLISION,
    ObjId.Trigger.INSTANT_COLLISION,
    ObjId.Trigger.INSTANT_COUNT
}

GROUP_FIELDS = {
    ObjProp.GROUPS,
    ObjProp.Trigger.Spawn.GROUP_ID,
    ObjProp.Trigger.Spawn.REMAPS,
    ObjProp.Trigger.Move.TARGET_POS
}


def _new_object(object_id: int):
    """actual new object implementation, returns ObjectType w/ defaults"""
    a: ObjectType = {}
    return a

# add overloads for this later
@overload
def new_object(object_id: Literal[901]) -> MoveType:
    ...
@overload
def new_object(object_id: int) -> ObjectType:
    ...
def new_object(object_id: int) -> ObjectType:
    return _new_object(object_id)