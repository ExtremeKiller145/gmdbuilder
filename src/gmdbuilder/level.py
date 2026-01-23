"""Type-safe level interface for Geometry Dash."""

from pathlib import Path

from gmdkit.models.level import Level as KitLevel  # type: ignore
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject  # type: ignore
from gmdkit.extra.live_editor import LiveEditor  # type: ignore

from gmdbuilder.object_types import ObjectType
from gmdbuilder.validation import ValidationError

WEBSOCKET_URL_DEFAULT = "ws://127.0.0.1:1313" # for live server default URl, same as gmdkit's default

objects: list[ObjectType] = []    
_kit_level: KitLevel | None = None
_export_path: str | Path | None = None
_live_editor: LiveEditor | None = None
_live_editor_connected: bool = False

def from_file(file_path: str | Path):
    """Load level from .gmd file"""
    _kit_level = KitLevel.from_file(str(file_path))
    _load_objects_from_kit()

def from_live_editor(url: str | None = None):
    """
    Load level from WSLiveEditor, iAndyHD3's Geode Mod.
    Github Link: https://github.com/iAndyHD3/WSLiveEditor
    """
    _live_editor = LiveEditor(url or WEBSOCKET_URL_DEFAULT)
    _live_editor.connect()
    _live_editor_connected = True

def _load_objects_from_kit():
    """Internal: Load objects from kit level into typed dict format"""
    if _kit_level is None:
        raise RuntimeError("No level loaded")
    
    objects: list[ObjectType] = []
    for kit_obj in _kit_level.objects:
        # Convert int keys to 'a<int>' string keys
        typed_obj: ObjectType = {} # type: ignore
        for int_key, value in kit_obj.items():
            str_key = f"a{int_key}"
            typed_obj[str_key] = value
        objects.append(typed_obj)
object_queue = []
def export(file_path: str | Path | None = None):
    """Export level to file or live editor.

    Args:
        file_path: Path to save to. Will override the source path if not given.
    """
    if _kit_level is None and not _live_editor_connected:
        raise RuntimeError("No level loaded. Use Level.from_file() or Level.from_live_editor() first")
    
    for obj in object_queue:
        for resolve in obj.get('_pending_validations', []):
            try:
                resolve(objects, object_queue)
            except ValidationError as e:
                raise ValidationError(f"Validation failed for queued object: {e}")
        objects.append(obj)
    object_queue.clear()
    
    if file_path:
        _export_to_file(str(file_path))
    elif _live_editor_connected:
        _export_to_live_editor()
    else:
        raise RuntimeError("No export destination. Provide file_path or use Level.from_live_editor()")

def _export_to_file(file_path: str) -> None:
    """Internal: Save to .gmd file"""
    if _kit_level is None:
        raise RuntimeError("Cannot export to file without loaded level")
    
    if _kit_level is None:
        raise RuntimeError("No level loaded")
    
    kit_objects = KitObjectList()
    for obj in objects:
        # Convert 'a<int>' keys back to int keys
        kit_obj_dict = {}
        for str_key, value in obj.items():
            if str_key.startswith('a') and len(str_key) > 1:
                int_key = int(str_key[1:])
                kit_obj_dict[int_key] = value
        
        kit_obj = KitObject()
        kit_obj.update(kit_obj_dict)
        kit_objects.append(kit_obj)
    
    _kit_level.objects = kit_objects
    _kit_level.to_file(file_path)

def _export_to_live_editor():
    """Internal: Send to WSLiveEditor"""
    if _live_editor is None:
        raise RuntimeError("Live editor not connected")
    
    # Convert typed dicts back to int keys and create kit objects
    kit_objects = KitObjectList()
    for obj in objects:
        kit_obj_dict = {}
        for str_key, value in obj.items():
            if str_key.startswith('a') and len(str_key) > 1:
                int_key = int(str_key[1:])
                kit_obj_dict[int_key] = value
        
        kit_obj = KitObject()
        kit_obj.update(kit_obj_dict)
        kit_objects.append(kit_obj)
    
    _live_editor.add_objects(kit_objects)

