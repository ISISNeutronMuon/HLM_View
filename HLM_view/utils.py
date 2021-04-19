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


class ObjectID(Enum):
    R80_TOTAL = 139
    R55_TOTAL = 135
    R53_TOTAL = 129
    R108_MCP_INVENTORY = 185

# IDs of objects which store the purity value of the building
dg_purity_objects = {
    DisplayGroupID.R108.value: 177,
    DisplayGroupID.R55.value: 71,
    DisplayGroupID.R80.value: 73
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


def get_building_data(display_group_id):
    building_data = {
        "he_total": 0, 
        "oxygen": "N/A",
        "purity": "N/A",
        "coordinators": get_coordinators_data(building_display_id=display_group_id)
    }

    building_data["he_total"] = round(sum([float(x["he_total"]) for x in building_data["coordinators"]]), 3)

    building_oxygen_levels = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.OxygenLevel.value, ob_displaygroup_id=display_group_id)
    if building_oxygen_levels:
        oxygen_level_meas = [GamMeasurement.objects.filter(mea_object=obj.ob_id).last() for obj in building_oxygen_levels]
        oxygen_level = sum([round(mea.mea_value1, 3) for mea in oxygen_level_meas])
        building_data["oxygen"] = oxygen_level

    if display_group_id in dg_purity_objects:
        building_data["purity"] = GamMeasurement.objects.filter(mea_object=dg_purity_objects[display_group_id]).last().mea_value2

    return building_data

def get_coordinators_data(building_display_id):
    building_coordinators = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.Coordinator.value, ob_endofoperation=None, ob_displaygroup_id=building_display_id)
    coordinators = []
    for coord in building_coordinators:
        coordinator_data = {
            "id": coord.ob_id,
            "name": coord.ob_name,
            "he_total": 0,
            "devices": get_devices_data(coordinator_id=coord.ob_id)
        }
        coordinator_data["he_total"] = round(sum([x["he_value"] for x in coordinator_data["devices"] if x["he_value"]]), 3)
        coordinators.append(coordinator_data)

    return coordinators

def get_devices_data(coordinator_id):
    relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id=coordinator_id).order_by('-or_date_assignment')
    devices = []

    for rel in relations:
        device = rel.or_object_id_assigned
        if device.ob_objecttype.ot_objectclass_id == ObjectClassID.HeLevelModule.value:  # if device object class is helium level module
            last_mea = GamMeasurement.objects.filter(mea_object=device.ob_id).last()

            no_volume = -1.000  # default value if object has no volume for conversion from fill % to litres
            he_value = last_mea.mea_value5 if last_mea.mea_value5 != no_volume else 0

            device_data = {
                "id": device.ob_id,
                "name": device.ob_name,
                "fill_percentage": last_mea.mea_value1,
                "he_value": he_value,
                "last_update": last_mea.mea_date
            }
            devices.append(device_data)
    
    return devices
