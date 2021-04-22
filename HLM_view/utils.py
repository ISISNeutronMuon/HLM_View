from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation
from enum import Enum

class ObjectTypeID(Enum):
    SLD = 18  # software level device obj. type id is 18
    Coordinator = 1
    OxygenLevel = 22  # Oxygen Level = Type & Class ID 22
    PRESSURE_SENSOR = 6
    CONTAMINATION = 10


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
    CB_TURBINE_100 = 182
    CB_TURBINE_101 = 183
    BUFFER_PRESSURE = 103
    MOTHER_DEWAR = 187
    MAIN_HE_PURITY = 91
    # TODO: BALLOON_PRESSURE =  No object in the DB - PV not yet implemented


# IDs of objects which store the purity value of the building
dg_purity_objects = {
    DisplayGroupID.R108.value: 177,
    DisplayGroupID.R55.value: 71,
    DisplayGroupID.R80.value: 73
}

# List of objects to display in the high pressure system view
# TODO: Configure HPS objects in the DB rather than here?
hps_objects = [
    70,  # TS1 He Gas Resupply
    71,  # TS1 Helium Resupply Purity
    72,  # TS2 He Gas Resupply
    73,  # TS2 Helium Resupply Purity
    74,  # MCP1 Impure He
    75,  # MCP2 Impure He
    76,  # Bank 2 Impure Helium Purity Avg
    77,  # MCP1 Helium Spare Storage Bank 5
    78,  # MCP2 Helium Spare Storage Bank 5
    79,  # Helium Spare Storage Bank 5 Purity
    80,  # MCP1 Helium Spare Storage Bank 6
    81,  # MCP2 Helium Spare Storage Bank 6
    82,  # Helium Spare Storage Bank 6 Purity
    83,  # MCP1 Helium Spare Storage Bank 7
    84,  # MCP2 Helium Spare Storage Bank 7
    85,  # Helium Spare Storage Bank 7 Purity
    86,  # MCP1 Helium Spare Storage Bank 8
    87,  # MCP2 Helium Spare Storage Bank 8
    88,  # Helium Spare Storage Bank 8 Purity
    89,  # MCP1 Main Helium
    90,  # MCP2 Main Helium
    91,  # Main Helium Purity
    92,  # MCP1 DLS Main Helium
    93,  # MCP2 DLS Main Helium
    94,  # DLS Main Helium Purity
]

def prepare_objects_data(objects):
    data = []
    for obj in objects:
        last_mea = GamMeasurement.objects.filter(mea_object=obj.ob_id).last()
        obj_data = {
            'ob_id': obj.ob_id,
            'ob_name': obj.ob_name,
            'ob_type': obj.ob_objecttype_id,
            'ob_type_name': obj.ob_objecttype.ot_name,
            'ob_comment': obj.ob_comment,
            'ob_class_name': obj.ob_objecttype.ot_objectclass.oc_name,
            'mea_values': [
                last_mea.mea_value1 if last_mea else None,
                last_mea.mea_value2 if last_mea else None,
                last_mea.mea_value3 if last_mea else None,
                last_mea.mea_value4 if last_mea else None,
                last_mea.mea_value5 if last_mea else None
            ],
            'mea_date': last_mea.mea_date if last_mea else None,
            'dg_name': obj.ob_displaygroup.dg_name if obj.ob_displaygroup else None,
            'ob_posinformation': obj.ob_posinformation,
        }   
        data.append(obj_data)

    return data

def get_building_data(display_group_id):
    building_data = {
        "he_total": 0, 
        "oxygen": "N/A",
        "purity": "N/A",
        "coordinators": get_coordinators_data(building_display_id=display_group_id)
    }

    building_data["he_total"] = sum([float(x["he_total"]) for x in building_data["coordinators"]])

    building_oxygen_levels = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.OxygenLevel.value, 
                                                    ob_displaygroup_id=display_group_id)
    if building_oxygen_levels:
        oxygen_level_meas = [GamMeasurement.objects.filter(mea_object=obj.ob_id).last() for obj in building_oxygen_levels]
        oxygen_level = sum([mea.mea_value1 for mea in oxygen_level_meas])
        building_data["oxygen"] = oxygen_level

    if display_group_id in dg_purity_objects:
        building_data["purity"] = GamMeasurement.objects.filter(mea_object=dg_purity_objects[display_group_id]).last().mea_value2

    return building_data

def get_coordinators_data(building_display_id):
    building_coordinators = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.Coordinator.value,
                                                    ob_endofoperation=None, 
                                                    ob_displaygroup_id=building_display_id)
    coordinators = []
    for coord in building_coordinators:
        coordinator_data = {
            "id": coord.ob_id,
            "name": coord.ob_name,
            "he_total": 0,
            "devices": get_devices_data(coordinator_id=coord.ob_id)
        }
        coordinator_data["he_total"] = sum([x["he_value"] for x in coordinator_data["devices"] if x["he_value"]])
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
