from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation
from django.views.decorators.http import require_http_methods
from .utils import ObjectTypeID, DisplayGroupID, ObjectClassID, dg_purity_objects

buildings_config = [
        {
            "id": "R55",
            "displaygroup": DisplayGroupID.R55.value,
            "desc": "Target Station 1",
            "image": "images/R55_overview.png",
            "total_he_info": "(Dewars + cryostats)",
            "map": "R55_map.png"
        },
        {
            "id": "R80",
            "displaygroup": DisplayGroupID.R80.value,
            "desc": "Target Station 2",
            "image": "images/R80_overview.png",
            "total_he_info": "(Dewars + cryostats)",
            "map": "R80_map.png"
        },
        {
            "id": "R108",
            "displaygroup": DisplayGroupID.R108.value,
            "desc": "Helium Recovery",
            "image": "images/R108_overview.png",
            "total_he_info": "(Dewars + mother dewar + MCP gas + balloon)"
        },
        {
            "id": "R53",
            "displaygroup": DisplayGroupID.R53.value,
            "desc": "Materials Characterisation Lab",
            "image": "images/R53_overview.png",
            "total_he_info": "(Dewars + cryostats)"
        }
]

# Create your views here.
def index(request):
    context = {
        "buildings": buildings_config
    }

    return render(request, 'index.html', context)

def measurements(request):
    context = {}
    return render(request, 'measurements.html', context)

def detail(request, object_id=None):
    # Get object data (and check if exists)
    object_ = None
    try:
        object_ = GamObject.objects.get(ob_id=object_id)
    except GamObject.DoesNotExist:
        raise Http404(f"Object with ID {object_id} does not exist.")

    obj_relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id=object_.ob_id).order_by('-or_date_assignment')

    sld = next((rel.or_object_id_assigned for rel in obj_relations if rel.or_object_id_assigned.ob_objecttype_id == ObjectTypeID.SLD.value), None)

    # ID of object whose measurements to display (for Software Level Devices
    # which store the measurements of objects)
    meas_obj_id = sld.ob_id if sld else object_.ob_id

    types_obj = sld if sld else object_
    obj_class = types_obj.ob_objecttype.ot_objectclass
    mea_types = [obj_class.oc_measuretype1, obj_class.oc_measuretype2, obj_class.oc_measuretype3, obj_class.oc_measuretype4, obj_class.oc_measuretype5]

    # if object display group is mobile, check if attached to a coordinator and get position
    obj_relations_assigned = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id_assigned=object_.ob_id).order_by('-or_date_assignment')
    obj_coordinator = None
    if object_.ob_displaygroup_id == DisplayGroupID.Mobile.value:
        obj_coordinator = next((rel.or_object for rel in obj_relations_assigned if rel.or_object.ob_objecttype_id == ObjectTypeID.Coordinator.value), None)

    context = {
        'object': object_,
        'coordinator': obj_coordinator,
        'meas_obj_id': meas_obj_id,  
        'sld': sld,
        'mea_types': mea_types
    }
    return render(request, 'details.html', context)

def object_search(request):
    object_name_query = request.GET.get('q')
    try:
        object_ = GamObject.objects.get(ob_name=object_name_query)
    except GamObject.DoesNotExist:
        raise Http404(f'Found no object(s) with name "{object_name_query}".')

    object_id = object_.ob_id
    return redirect(detail, object_id=object_id)
    
def building(request, building):
    if building not in [x["id"] for x in buildings_config]:
        raise Http404(f'Building "{building}" not found.')

    context = {"building": next((x for x in buildings_config if x['id'] == building), None)}
    
    return render(request, 'building.html', context)

@require_http_methods(['GET'])
def get_general_data(request):
    coordinators = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.Coordinator.value, ob_endofoperation=None)

    def fetch_building_data(display_group_id: int):
        building_coordinators = [x for x in coordinators if x.ob_displaygroup_id == display_group_id]
        building_data = {
            "he_total": 0, 
            "oxygen": "N/A",
            "purity": "N/A",
            "coordinators": []
        }
        for coord in building_coordinators:
            coordinator_data = {
                "id": coord.ob_id,
                "name": coord.ob_name,
                "he_total": 0,
                "devices": []
            }
            relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id=coord.ob_id).order_by('-or_date_assignment')
            for rel in relations:
                device = rel.or_object_id_assigned
                if device.ob_objecttype.ot_objectclass_id == ObjectClassID.HeLevelModule.value:  # if device object class is helium level module
                    last_mea = GamMeasurement.objects.filter(mea_object=device.ob_id).last()
                    device_data = {
                        "id": device.ob_id,
                        "name": device.ob_name,
                        "value": round(float(last_mea.mea_value1), 3),
                        "last_update": last_mea.mea_date
                    }
                    coordinator_data["devices"].append(device_data)

            coordinator_data["he_total"] = round(sum([float(x["value"]) for x in coordinator_data["devices"]]), 3)
            building_data["coordinators"].append(coordinator_data)

        building_data["he_total"] = round(sum([float(x["he_total"]) for x in building_data["coordinators"]]), 3)

        oxygen_level_objects = GamObject.objects.filter(ob_objecttype_id=ObjectTypeID.OxygenLevel.value, ob_displaygroup_id=display_group_id)
        if oxygen_level_objects:
            oxygen_level_meas = [GamMeasurement.objects.filter(mea_object=obj.ob_id).last() for obj in oxygen_level_objects]
            oxygen_level = sum([round(mea.mea_value1, 3) for mea in oxygen_level_meas])
            building_data["oxygen"] = oxygen_level

        if display_group_id in dg_purity_objects:
            building_data["purity"] = GamMeasurement.objects.filter(mea_object=purity_objects[display_group_id]).last().mea_value2

        return building_data

    data = {}
    for building in buildings_config:
        data[building["id"]] = fetch_building_data(building["displaygroup"])

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_object_names(request):
    q = request.GET.get('q')

    if q:
        objects = GamObject.objects.filter(ob_name__icontains=q)
    else:
        objects = GamObject.objects.all()

    data = [{'name': obj.ob_name} for obj in objects]

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_object_measurements(request, object_id):
    measurements = GamMeasurement.objects.filter(mea_object=object_id).order_by('-mea_id')
    data = [
        {
            "mea_id": mea.mea_id, 
            "mea_date": mea.mea_date,
            "mea_value1": mea.mea_value1,
            "mea_value2": mea.mea_value2,
            "mea_value3": mea.mea_value3,
            "mea_value4": mea.mea_value4,
            "mea_value5": mea.mea_value5,
        } 
        for mea in measurements
    ]

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_measurement_types(request):
    data = {}  # store mea type by ob type as ob class is not in GamObject
    object_types = GamObjecttype.objects.all()
    for obj_type in object_types: 
        type_class = obj_type.ot_objectclass
        data[obj_type.ot_id] = [
            type_class.oc_measuretype1, type_class.oc_measuretype2, type_class.oc_measuretype3, 
            type_class.oc_measuretype4, type_class.oc_measuretype5
        ]
    
    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_display_groups(request):
    data = []
    display_groups = GamDisplaygroup.objects.all()
    
    for dg in display_groups:
        data.append({
            "dg_id": dg.dg_id,
            "dg_name": dg.dg_name,
            "dg_outofoperation": dg.dg_outofoperation
        })
    
    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_object_classes(request):
    data = []
    classes = GamObjectclass.objects.all()
    
    for class_ in classes:
        data.append({
            "oc_id": class_.oc_id,
            "oc_function_id": class_.oc_function_id,
            "oc_name": class_.oc_name,
            "oc_commment": class_.oc_comment
        })
    
    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_objects_table_data(request):
    objects = GamObject.objects.all()
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

    return JsonResponse(data, safe=False)
