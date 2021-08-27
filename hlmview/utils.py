from .models import GamObject, GamMeasurement, GamObjectrelation
from enum import Enum
from django.utils import timezone
from datetime import timedelta

NO_HELIUM = "N/A"
STALE_AGE_HOURS = 12
INVALID_VALUE = -1.000  # default value if object has no volume for conversion from fill % to litres


class ObjectTypeID(Enum):
    GCM = 16  # gas counter module
    SLD = 18  # software level device obj. type id is 18
    Coordinator = 1
    OxygenLevel = 22  # Oxygen Level = Type & Class ID 22
    PRESSURE_SENSOR = 6
    CONTAMINATION = 10


class ObjectClassID(Enum):
    GAS_COUNTER_MODULE = 16
    HeLevelModule = 17  # helium level module
    LEVELMETER = 13
    VESSEL = 2
    CRYOSTAT = 4
    GAS_COUNTER = 7


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


def fetch_r108_data():
    data = {
        "cb-turbine-100": GamMeasurement.objects.filter(mea_object=ObjectID.CB_TURBINE_100.value).last().mea_value1,
        "cb-turbine-101": GamMeasurement.objects.filter(mea_object=ObjectID.CB_TURBINE_101.value).last().mea_value1,
        "buffer-pressure": GamMeasurement.objects.filter(mea_object=ObjectID.BUFFER_PRESSURE.value).last().mea_value1,
        "mother-dewar": {
            "fill": GamMeasurement.objects.filter(mea_object=ObjectID.MOTHER_DEWAR.value).last().mea_value1,
            "l": GamMeasurement.objects.filter(mea_object=ObjectID.MOTHER_DEWAR.value).last().mea_value5
        },
        "main-he-purity": GamMeasurement.objects.filter(mea_object=ObjectID.MAIN_HE_PURITY.value).last().mea_value2,
        "mcp-inventory": GamMeasurement.objects.filter(mea_object=ObjectID.R108_MCP_INVENTORY.value).last().mea_value5,
        "balloon": {
            "mbar": None,  # TODO: PV needs to be implemented in the IOC
            "l": None  # TODO: Volume is 22^3
        }
    }

    data["helium-no-transport"] = sum(
        [x for x in [data["mcp-inventory"], data["mother-dewar"]["l"], data["balloon"]["l"]] if x is not None])

    R108_coordinators_data = get_building_data(DisplayGroupID.R108.value)
    data["total-helium"] = sum(
        [x for x in [data["helium-no-transport"], R108_coordinators_data["he_total"]] if x is not None])

    return data


def get_previous_measurement(hour, object_id):
    measurement = GamMeasurement.objects.filter(mea_object=object_id)
    last_mea = measurement.last()
    previous_mea = None
    if last_mea is not None and last_mea.mea_date is not None:
        previous_mea_date = last_mea.mea_date - timedelta(days=1)
        previous_mea_date = previous_mea_date.replace(hour=hour, minute=0, second=0)
        # add a limit to how far back we check
        limit = previous_mea_date - timedelta(days=1)
        measurement = measurement.filter(mea_date__gte=limit, mea_date__lte=previous_mea_date)
        previous_mea = measurement.last()
    return last_mea, previous_mea


def calculate_differences(current_measurement, previous):
    if current_measurement is not None and previous is not None:
        diff = current_measurement - previous
        if previous == 0:
            if current_measurement == 0:
                percentage_diff = 0
            else:
                percentage_diff = "N/A"
        else:
            if previous < 0 < current_measurement:
                percentage_diff = abs(current_measurement - previous)
                previous = abs(previous)
            else:
                percentage_diff = (abs(current_measurement) - abs(previous))
            percentage_diff = percentage_diff / previous * 100
            # abs of values to avoid increasing a negative value having a negative percent change
    else:
        return None

    if percentage_diff != "N/A":
        operator = ""

        if percentage_diff >= 0:
            percentage_diff = abs(percentage_diff)  # handle -0
            operator = "+"
        percentage_diff = f"{operator}{percentage_diff:.2f}%"
    if diff is not None:
        if diff >= 0:
            operator = "+"
        diff = f"{percentage_diff}\t{operator}{diff:.2f}"
    else:
        diff = percentage_diff
    return diff


def prepare_objects_data(objects):
    data = []
    for obj in objects:
        last_mea, previous_mea = get_previous_measurement(8, obj.ob_id)
        obj_data = {
            'ob_id': obj.ob_id,
            'ob_name': obj.ob_name,
            'ob_type': obj.ob_objecttype_id,
            'ob_type_name': obj.ob_objecttype.ot_name,
            'ob_comment': obj.ob_comment,
            'ob_class_name': obj.ob_objecttype.ot_objectclass.oc_name,
            'mea_values': [None, None, None, None, None],
            'mea_date': last_mea.mea_date if last_mea else None,
            'dg_name': obj.ob_displaygroup.dg_name if obj.ob_displaygroup else None,
            'ob_posinformation': obj.ob_posinformation
        }
        if last_mea is not None:
            obj_data['mea_values'] = [
                last_mea.mea_value1,
                last_mea.mea_value2,
                last_mea.mea_value3,
                last_mea.mea_value4,
                last_mea.mea_value5
            ]
            if previous_mea is not None:
                temp_list = []
                previous_list = [
                    previous_mea.mea_value1,
                    previous_mea.mea_value2,
                    previous_mea.mea_value3,
                    previous_mea.mea_value4,
                    previous_mea.mea_value5
                ]
                for i in range(5):

                    current_measurement = obj_data['mea_values'][i]
                    previous = previous_list[i]
                    diff = calculate_differences(current_measurement, previous)
                    if diff is None:
                        temp_list.append(f"{current_measurement}")
                    else:
                        temp_list.append(f"{current_measurement}\t{diff}")
                obj_data['mea_values'] = temp_list
        data.append(obj_data)

    return data


def get_building_data(display_group_id):
    building_data = {
        "he_total": 0,
        "oxygen": "N/A",
        "purity": "N/A",
        "coordinators": get_coordinators_data(building_display_id=display_group_id),
        "warnings": {
            "stale_devices": 0,
            "no_value_devices": 0
        }
    }

    building_data["he_total"] = sum([x["he_total"] for x in building_data["coordinators"]])
    building_data["warnings"]["stale_devices"] = [x["warnings"]["stale_devices"] for x in building_data["coordinators"]
                                                  if len(x["warnings"]["stale_devices"]) > 0]
    building_data["warnings"]["no_value_devices"] = [x["warnings"]["no_value_devices"] for x in
                                                     building_data["coordinators"] if
                                                     len(x["warnings"]["no_value_devices"]) > 0]

    building_oxygen_levels = GamObject.objects.filter(
        ob_objecttype_id=ObjectTypeID.OxygenLevel.value,
        ob_displaygroup_id=display_group_id
    )
    if building_oxygen_levels:
        oxygen_level_meas = [GamMeasurement.objects.filter(mea_object=obj.ob_id).last() for obj in
                             building_oxygen_levels]
        oxygen_level = sum([mea.mea_value1 for mea in oxygen_level_meas])
        building_data["oxygen"] = oxygen_level

    if display_group_id in dg_purity_objects:
        purity_obj = GamMeasurement.objects.filter(mea_object=dg_purity_objects[display_group_id]).last()
        if purity_obj:
            building_data["purity"] = purity_obj.mea_value2

    return building_data


def get_coordinators_data(building_display_id):
    building_coordinators = GamObject.objects.filter(
        ob_objecttype_id=ObjectTypeID.Coordinator.value,
        ob_endofoperation=None,
        ob_displaygroup_id=building_display_id
    )
    coordinators = []
    for coord in building_coordinators:
        coordinator_data = {
            "id": coord.ob_id,
            "name": coord.ob_name,
            "he_total": 0,
            "devices": get_devices_data(coordinator=coord),
            "warnings": {
                "stale_devices": [],
                "no_value_devices": []
            }
        }
        coordinator_data["he_total"] = sum(
            [x["he_value"] for x in coordinator_data["devices"] if x["he_value"] and x["he_value"] != NO_HELIUM])
        coordinator_data["warnings"]["stale_devices"] = [x["name"] for x in coordinator_data["devices"] if
                                                         x["warnings"]["is_stale"] is True]
        coordinator_data["warnings"]["no_value_devices"] = [x["name"] for x in coordinator_data["devices"] if
                                                            x["warnings"]["no_value"] is True]

        coordinators.append(coordinator_data)

    return coordinators


def get_devices_data(coordinator):
    relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object=coordinator).order_by(
        '-or_date_assignment')
    devices = []

    for rel in relations:
        device = rel.or_object_id_assigned
        if device.ob_objecttype.ot_objectclass_id in [ObjectClassID.HeLevelModule.value,
                                                      ObjectClassID.LEVELMETER.value]:
            last_mea = GamMeasurement.objects.filter(mea_object=device.ob_id).last()

            he_value = last_mea.mea_value5 if last_mea.mea_value5 and last_mea.mea_value5 != INVALID_VALUE else NO_HELIUM

            time_after_is_stale = timedelta(hours=STALE_AGE_HOURS)
            time_since_last_update = timezone.now() - last_mea.mea_date

            device_data = {
                "id": device.ob_id,
                "name": device.ob_name,
                "fill_percentage": last_mea.mea_value1,
                "he_value": he_value,
                "last_update": last_mea.mea_date,
                "warnings": {
                    "is_stale": time_since_last_update > time_after_is_stale,
                    "no_value": he_value == NO_HELIUM
                }
            }

            devices.append(device_data)

    return devices


def get_object_module(object_id: int, object_class: int = None):
    """
    Get the module of the object with the given ID.

    Args:
        object_id (int): The object ID whose relations to check for the module.
        object_class (int, optional): The object's class ID, if None it will be queried.

    Returns:
        (GamObject): The module object, None if not found.
    """
    if object_class is None:
        obj = GamObject.get_or_none(GamObject.ob_id == object_id)
        if obj is None:
            return None
        object_class = obj.ob_objecttype.ot_objectclass.oc_name
    if object_class in [ObjectClassID.VESSEL.value, ObjectClassID.CRYOSTAT.value]:
        return _get_module_object(object_id, ObjectTypeID.SLD.value)
    elif object_class == ObjectClassID.GAS_COUNTER.value:
        return _get_module_object(object_id, ObjectTypeID.GCM.value)
    else:
        return None



def _get_module_object(object_id: int, module_type: int):
    obj_relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id=object_id).order_by('-or_date_assignment')
    module = next((rel.or_object_id_assigned for rel in obj_relations if rel.or_object_id_assigned.ob_objecttype_id == module_type), None)
    return module
