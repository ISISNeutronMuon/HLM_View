from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import GamObject, GamMeasurement, GamObjecttype, GamObjectclass, GamDisplaygroup, GamObjectrelation
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def measurements(request):
    context = {}
    return render(request, 'measurements.html', context)

def detail(request, object_id=''):
    # Get object data (and check if exists)
    object_ = None
    try:
        object_ = GamObject.objects.get(ob_id=object_id)
    except GamObject.DoesNotExist:
        raise Http404(f"Object with ID {object_id} does not exist.")

    sld = None
    obj_relations = GamObjectrelation.objects.filter(or_date_removal=None, or_object_id=object_.ob_id).order_by('-or_date_assignment')
    for rel in obj_relations:
        # software level device obj. type id is 18
        if rel.or_object_id_assigned.ob_objecttype_id == 18:
            sld = rel.or_object_id_assigned
            break

    # ID of object whose measurements to display (for Software Level Devices
    # which store the measurements of objects)
    meas_obj_id = sld.ob_id if sld else object_.ob_id

    types_obj = sld if sld else object_
    obj_class = types_obj.ob_objecttype.ot_objectclass
    mea_types = [obj_class.oc_measuretype1, obj_class.oc_measuretype2, obj_class.oc_measuretype3, obj_class.oc_measuretype4, obj_class.oc_measuretype5]

    context = {
        'object': object_,
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
    

def R80(request):
    context = {}
    return render(request, 'r80.html', context)

def R55(request):
    context = {}
    return render(request, 'r55.html', context)

def R53(request):
    context = {}
    return render(request, 'r53.html', context)

@require_http_methods(['GET'])
def get_overview_data(request):
    # TODO
    data = {
        "R55": {"he_total": 55},
        "R80": {"he_total": 80},
        "R53": {"he_total": 53},
        "R108": {"he_total": 108},
    }

    return JsonResponse(data, safe=False)

@require_http_methods(['GET'])
def get_R80_data(request):
    # TODO
    data = {
        "r80_west": 1,
        "r80_east": 2,
        "r80_total": 3,
        "r53_total": 16,
        "o2_ts2_west": 7,
        "o2_ts2_east": 8,
        "let_df": 4,
        "let_nimrod": 5,
        "imat": 6,
        "maglab": 9,
        "maglab_df": 10,
        "wish": 11,
        "wish_df": 12,
        "larmor_offspec": 13,
        "zoom_sans2d_polref": 14,
        "zoom_df": 15
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
