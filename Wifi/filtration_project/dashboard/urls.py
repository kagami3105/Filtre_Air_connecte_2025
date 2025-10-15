from django.urls import path
from . import views, api

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    # CRUD Filter
    path('filters/create/', views.filter_create, name='filter_create'),
    path('filters/<int:pk>/', views.filter_detail, name='filter_detail'),
    path('filters/<int:pk>/update/', views.filter_update, name='filter_update'),
    path('filters/<int:pk>/delete/', views.filter_delete, name='filter_delete'),

    # Data list
    path('data/', views.data_list, name='data_list'),

    # AJAX actions
    path('filters/<int:pk>/toggle/', views.toggle_filter, name='toggle_filter'),
    path('filters/<int:pk>/speed/', views.set_speed, name='set_speed'),

    # Wi-Fi setup
    path('wifi/', views.wifi_setup, name='wifi_setup'),

    # MCU API
    path('api/mcu/<int:filter_id>/data/', api.mcu_post_data, name='mcu_post_data'),
    path('api/mcu/<int:filter_id>/state/', api.mcu_get_filter_state, name='mcu_get_filter_state'),
    path('api/mcu/wifi/', api.mcu_get_wifi_config, name='mcu_get_wifi_config'),


    path('wifi/', views.wifi_setup, name='wifi_setup'),
    path('api/wifi/', api.mcu_get_wifi, name='mcu_get_wifi'),
    path('api/status/', api.mcu_post_status, name='mcu_post_status'),
    path('networks/', views.show_networks, name='show_networks'),
    path('api/networks/', views.receive_networks, name='receive_networks'),
    path('api/sensor/', views.receive_sensor_data, name='receive_sensor_data'),
    path('sensor-data/', views.show_sensor_data, name='show_sensor_data'),
    path('sensor-data/json/', views.sensor_data_json, name='sensor_data_json'),


    path('api/receive_sensor_data/', views.receive_sensor_data, name='receive_sensor_data'),
    path('api/sensor_data_json/', views.sensor_data_json, name='sensor_data_json'),
    path('capteurs/', views.show_sensor_data, name='show_sensor_data'),

]