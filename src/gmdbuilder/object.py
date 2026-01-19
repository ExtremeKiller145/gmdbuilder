"""Object builder"""

from gmdkit.models.object import Object as kit_object
from gmdbuilder.internal_mappings.obj_prop import ObjProp
from gmdbuilder.object_types import Object as ObjectType
# Object

class Object:
    def __init__(self, object_id: int):
        self.dict: ObjectType = kit_object.DEFAULTS.get(object_id, {})
        return self
    
    
a = Object(2)
a.dict[ObjProp.ID]