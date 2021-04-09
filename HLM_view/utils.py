from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation

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
