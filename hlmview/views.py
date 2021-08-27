from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
import urllib
from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation
from django.views.decorators.http import require_http_methods
from .utils import ObjectTypeID, DisplayGroupID, ObjectID, get_building_data, get_devices_data, prepare_objects_data, \
hps_objects, fetch_r108_data, get_object_module, get_previous_measurement, calculate_differences

GRAFANA_HOST = 'localhost'

buildings_config = [
        {
            "id": "R55",
            "displaygroup": DisplayGroupID.R55.value,
            "desc": "Target Station 1",
            "image": "images/R55_overview.png",
            "total_he_info": "(Dewars + cryostats)",
            "map": "R55_map.png",
            "graphs": [ObjectID.R55_TOTAL.value]
        },
        {
            "id": "R80",
            "displaygroup": DisplayGroupID.R80.value,
            "desc": "Target Station 2",
            "image": "images/R80_overview.png",
            "total_he_info": "(Dewars + cryostats)",
            "map": "R80_map.png",
            "graphs": [ObjectID.R80_TOTAL.value]
        },
        {
            "id": "R108",
            "displaygroup": DisplayGroupID.R108.value,
            "desc": "Helium Recovery",
            "image": "images/R108_overview.png",
            "total_he_info": "(Dewars + mother dewar + MCP gas + balloon)",
            "graphs": [ObjectID.R108_MCP_INVENTORY.value],
            "custom_view": "r108.html",
            "custom_data": {
                "cb_turbine_100": ObjectID.CB_TURBINE_100.value, 
                "cb_turbine_101": ObjectID.CB_TURBINE_101.value,
                "buffer_pressure": ObjectID.BUFFER_PRESSURE.value,
                "mcp_liquid_he_inv": ObjectID.R108_MCP_INVENTORY.value,
                "main_he_purity": ObjectID.MAIN_HE_PURITY.value,
                "mother_dewar": ObjectID.MOTHER_DEWAR.value
            }
        },
        {
            "id": "R53",
            "displaygroup": DisplayGroupID.R53.value,
            "desc": "Materials Characterisation Lab",
            "image": "images/R53_overview.png",
            "total_he_info": "(Dewars + cryostats)",
            "graphs": [ObjectID.R53_TOTAL.value]
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

    object_module = None
    assigned_object = None
    devices_data = None
    obj_relations_assigned = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id_assigned=object_.ob_id).order_by('-or_date_assignment')

    # If object is a Coordinator, fetch devices data
    if object_.ob_objecttype_id == ObjectTypeID.Coordinator.value:
        devices_data = get_devices_data(object_.ob_id)
    else:
        # If object IS a module, find assigned object. If not, search if object has a module.
        if object_.ob_objecttype_id in [ObjectTypeID.SLD.value, ObjectTypeID.GCM.value]:
            assigned_object = next((rel.or_object for rel in obj_relations_assigned), None)
        else:
            object_module = get_object_module(object_.ob_id, object_.ob_objecttype.ot_objectclass.oc_id)

    # ID of object whose measurements to display (for Object Modules, e.g. SLDs/GCMs etc.
    # which store the measurements of objects)
    meas_obj = object_module if object_module else object_

    obj_class = meas_obj.ob_objecttype.ot_objectclass
    mea_types = [obj_class.oc_measuretype1, obj_class.oc_measuretype2, obj_class.oc_measuretype3, obj_class.oc_measuretype4, obj_class.oc_measuretype5]

    # if object display group is mobile, check if attached to a coordinator and get position
    obj_coordinator = None
    if object_.ob_displaygroup_id == DisplayGroupID.Mobile.value:
        obj_coordinator = next((rel.or_object for rel in obj_relations_assigned if rel.or_object.ob_objecttype_id == ObjectTypeID.Coordinator.value), None)

    context = {
        'object': object_,
        'coordinator': obj_coordinator,
        'meas_obj': meas_obj,  
        'module': object_module,
        'is_module': object_.ob_objecttype_id in [ObjectTypeID.SLD.value, ObjectTypeID.GCM.value],
        'assigned_object': assigned_object,
        'devices_data': devices_data,
        'mea_types': mea_types,
        'grafana_host': GRAFANA_HOST
    }

    return render(request, 'details.html', context)

def search_results(request, encoded_dict):
    search_results = urllib.parse.parse_qs(encoded_dict)
    results = []

    for key, value in search_results.items():
        current = {}
        object_ = GamObject.objects.get(ob_id=value[0])
        current["url"] = "details/{}".format(value[0])
        current["name"] = object_.ob_name
        current["id"] = value[0]
        results.append(current)

    return render(request, 'search_results.html', {"results": results})

def object_search(request):
    object_name_query = request.GET.get('q')
    object_ = GamObject.objects.filter(ob_name=object_name_query)

    if not object_:
        raise Http404(f'Found no object(s) with name "{object_name_query}".')

    if len(object_) > 1:
        results_dict = {}
        count = 1
        for item in object_:
            results_dict["search_results{}".format(count)] = item.ob_id
            count += 1
        encoded_dict = urllib.parse.urlencode(results_dict)
        return redirect(search_results, encoded_dict=encoded_dict)

    object_id = object_[0].ob_id
    return redirect(detail, object_id=object_id)
    
def building(request, building):
    if building not in [x["id"] for x in buildings_config]:
        raise Http404(f'Building "{building}" not found.')

    building_configuration = next((x for x in buildings_config if x['id'] == building), None)

    context = {
        "building": building_configuration,
        "grafana_host": GRAFANA_HOST
    }

    # If builing has custom content, render its custom view (which extends the default building view)
    if building_configuration.get('custom_view', None):
        return render(request, building_configuration['custom_view'], context)
    else:
        return render(request, 'building.html', context)

def high_pressure_system(request):
    context = {}
    return render(request, 'high-pressure.html', context)

@require_http_methods(['GET'])
def get_overview_data(request):
    data = {}
    for building in buildings_config:
        data[building["id"]] = get_building_data(building["displaygroup"])

    # Add custom R108 data as the total He value for R108
    r108_data = fetch_r108_data()
    data["R108"]["he_total"] = r108_data["total-helium"]

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_general_data(request, building_id):
    building_config = next((building for building in buildings_config if building["id"] == building_id), None)

    if not building_config:
        raise Http404(f"Could not fetch data - Building {building_id} was not found.")

    data = get_building_data(building_config["displaygroup"])

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_he_recovery_data(request):
    data = fetch_r108_data()

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_high_pressure_data(request):
    mcps = GamObject.objects.filter(ob_id__in=hps_objects, ob_objecttype_id=ObjectTypeID.PRESSURE_SENSOR.value)
    purity = GamObject.objects.filter(ob_id__in=hps_objects, ob_objecttype_id=ObjectTypeID.CONTAMINATION.value)

    data = {
        "mcps": prepare_objects_data(mcps),
        "purity": prepare_objects_data(purity)
    }

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
def get_object_measurements_change(request, object_id, hour=8):
    last_mea, previous_mea = get_previous_measurement(hour, object_id)
    data = {"diffs": None,
            "mea_date2": None,
            "mea_date_diff" : None,}
    data["diffs"] = {
            "mea_diff1": None,
            "mea_diff2": None,
            "mea_diff3": None,
            "mea_diff4": None,
            "mea_diff5": None,
           }
    if last_mea is not None:
        data["mea_date1"] = last_mea.mea_date.date()
        data["mea_id1"] = last_mea.mea_id
        if previous_mea is not None:
            last_list = [
                    last_mea.mea_value1,
                    last_mea.mea_value2,
                    last_mea.mea_value3,
                    last_mea.mea_value4,
                    last_mea.mea_value5
            ]
            previous_list = [
                    previous_mea.mea_value1,
                    previous_mea.mea_value2,
                    previous_mea.mea_value3,
                    previous_mea.mea_value4,
                    previous_mea.mea_value5
            ]
            for i in range(5):
                diff = calculate_differences(last_list[i], previous_list[i])
                if last_list[i] is None and diff is None:
                    data["diffs"]["mea_diff{}".format(i+1)] = None
                else:
                    data["diffs"]["mea_diff{}".format(i+1)] = f"{last_list[i]}\t{diff}"
            data["mea_date2"] = previous_mea.mea_date.date()
            data["mea_id2"] = previous_mea.mea_id
    
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
    data = prepare_objects_data(objects)

    return JsonResponse(data, safe=False)
