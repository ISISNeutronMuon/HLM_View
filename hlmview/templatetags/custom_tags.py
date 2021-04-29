from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_object_names(object_list):
    return [x.ob_name for x in object_list]
