from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation

from enum import Enum

class ObjectTypeID(Enum):
    SLD = 18  # software level device obj. type id is 18
    Coordinator = 1
    OxygenLevel = 22  # Oxygen Level = Type & Class ID 22


class ObjectClassID(Enum):
    HeLevelModule = 17  # helium level module


class DisplayGroupID(Enum):
    R108 = 1
    R80 = 2
    R55 = 3
    Mobile = 9
    R53 = 10


# IDs of objects which store the purity value of the building
dg_purity_objects = {
    DisplayGroupID.R108: 177,
    DisplayGroupID.R55: 71,
    DisplayGroupID.R80: 73
}

def get_helium_value(object_id: int):
    try:
        obj = GamObject.objects.get(ob_id=object_id)
    except GamObject.DoesNotExist:
        return None

    last_measurement = GamMeasurement.objects.filter(mea_object=object_id).last()
    
    value = {
        10: lambda x: x.mea_value2,
        12: lambda x: x.mea_value5,
        18: lambda x: x.mea_value5,
        22: lambda x: x.mea_value1,
    }[obj.ob_objecttype_id](last_measurement)

    return value
