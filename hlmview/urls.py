from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('measurements/', views.measurements, name='measurements'),
    path('details/', views.detail, name='detail'),
    path('details/<int:object_id>', views.detail, name='detail'),
    path('object_search/', views.object_search, name='object_search'),
    path('building/<str:building>', views.building, name='building'),
    path('high-pressure-system/', views.high_pressure_system, name='high_pressure_system'),
    path('objectnames/', views.get_object_names, name='object_names'),
    path('objects_table_data/', views.get_objects_table_data, name='objects_table_data'),
    path('measurement_types/', views.get_measurement_types, name='measurement_types'),
    path('display_groups/', views.get_display_groups, name='display_groups'),
    path('object_classes/', views.get_object_classes, name='object_classes'),
    path('object_measurements/<int:object_id>', views.get_object_measurements, name='object_measurements'),
    path('general_data/<str:building_id>', views.get_general_data, name='general_data'),
    path('overview_data/', views.get_overview_data, name='overview_data'),
    path('he_recovery_data/', views.get_he_recovery_data, name='he_recovery_data'),
    path('hps_data/', views.get_high_pressure_data, name='hps_data')
]