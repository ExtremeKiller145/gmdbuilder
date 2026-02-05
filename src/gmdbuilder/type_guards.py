"""
Type guard functions for narrowing ObjectType to specific subclasses.

These functions help the type checker understand that when you check an object's ID,
you can safely access properties specific to that object type.

Example:
    ```
    for obj in level.objects:
        if is_move_trigger(obj):
            # Type checker now knows obj is MoveType
            obj[ObjProp.Trigger.Move.MOVE_X] = 0
            obj[ObjProp.Trigger.Move.MOVE_Y] = 0
    ```
"""
from typing import TypeGuard

import gmdbuilder.object_typeddict as td
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.mappings.obj_id import ObjId


def is_move_trigger(obj: td.ObjectType) -> TypeGuard[td.MoveType]:
    """Check if object is a Move trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.MOVE


def is_rotate_trigger(obj: td.ObjectType) -> TypeGuard[td.RotateType]:
    """Check if object is a Rotate trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.ROTATE


def is_alpha_trigger(obj: td.ObjectType) -> TypeGuard[td.AlphaType]:
    """Check if object is an Alpha trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.ALPHA


def is_color_trigger(obj: td.ObjectType) -> TypeGuard[td.ColorType]:
    """Check if object is a Color trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.COLOR


def is_pulse_trigger(obj: td.ObjectType) -> TypeGuard[td.PulseType]:
    """Check if object is a Pulse trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.PULSE


def is_spawn_trigger(obj: td.ObjectType) -> TypeGuard[td.SpawnType]:
    """Check if object is a Spawn trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.SPAWN


def is_toggle_trigger(obj: td.ObjectType) -> TypeGuard[td.ToggleType]:
    """Check if object is a Toggle trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.TOGGLE


def is_count_trigger(obj: td.ObjectType) -> TypeGuard[td.CountType]:
    """Check if object is a Count trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.COUNT


def is_follow_trigger(obj: td.ObjectType) -> TypeGuard[td.FollowType]:
    """Check if object is a Follow trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.FOLLOW


def is_stop_trigger(obj: td.ObjectType) -> TypeGuard[td.StopType]:
    """Check if object is a Stop trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.STOP


def is_touch_trigger(obj: td.ObjectType) -> TypeGuard[td.TouchType]:
    """Check if object is a Touch trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.TOUCH


def is_animate_trigger(obj: td.ObjectType) -> TypeGuard[td.AnimateType]:
    """Check if object is an Animate trigger."""
    return obj.get(ObjProp.ID) == ObjId.Trigger.ANIMATE
