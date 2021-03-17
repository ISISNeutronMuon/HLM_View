from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('measurements/', views.measurements, name='measurements'),
    path('details/', views.detail, name='detail'),
    path('details/<int:object_id>', views.detail, name='detail'),
    path('object_search/', views.object_search, name='object_search'),
    path('objectnames/', views.get_object_names, name='object_names'),  # object-search-autocomplete.js
    path('objects_table_data/', views.get_objects_table_data, name='objects_table_data'),
    path('measurement_types/', views.get_measurement_types, name='measurement_types'),
    path('display_groups/', views.get_display_groups, name='display_groups'),
    path('object_measurements/<int:object_id>', views.get_object_measurements, name='object_measurements')
]