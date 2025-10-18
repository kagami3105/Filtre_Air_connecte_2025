# filtration_project/dashboard/urls.py
from django.urls import path
# On importe les vues et les endpoints API du dashboard
from . import views, api

# Namespace pour les URLs du dashboard
app_name = 'dashboard'

# Définition des routes URL pour le dashboard

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # Vue principale du dashboard

    # CRUD Filter
    path('filters/create/', views.filter_create, name='filter_create'), # Création d’un nouveau filtre
    path('filters/<int:pk>/', views.filter_detail, name='filter_detail'), # Détail d’un filtre spécifique
    path('filters/<int:pk>/update/', views.filter_update, name='filter_update'), # Mise à jour d’un filtre spécifique
    path('filters/<int:pk>/delete/', views.filter_delete, name='filter_delete'), # Suppression d’un filtre spécifique

    # Data list
    path('data/', views.data_list, name='data_list'), # Liste des données des microcontrôleurs

    # AJAX actions
    path('filters/<int:pk>/toggle/', views.toggle_filter, name='toggle_filter'), # Activer/désactiver un filtre
    path('filters/<int:pk>/speed/', views.set_speed, name='set_speed'), # Définir la vitesse du ventilateur

    # Wi-Fi setup
    path('wifi/', views.wifi_setup, name='wifi_setup'), # Configuration Wi-Fi via l’interface web

    # MCU API
    path('api/mcu/<int:filter_id>/data/', api.mcu_post_data, name='mcu_post_data'), # Endpoint pour poster les données du microcontrôleur
    path('api/mcu/<int:filter_id>/state/', api.mcu_get_filter_state, name='mcu_get_filter_state'), # Endpoint pour obtenir l’état du filtre
    path('api/mcu/wifi/', api.mcu_get_wifi_config, name='mcu_get_wifi_config'), # Endpoint pour obtenir la config Wi-Fi


    path('wifi/', views.wifi_setup, name='wifi_setup'), # Configuration Wi-Fi via l’interface web
    path('api/wifi/', api.mcu_get_wifi, name='mcu_get_wifi'), # Endpoint pour obtenir la config Wi-Fi
    path('api/status/', api.mcu_post_status, name='mcu_post_status'), # Endpoint pour poster le statut de l’appareil
    path('networks/', views.show_networks, name='show_networks'), # Afficher les réseaux scannés
    path('api/networks/', views.receive_networks, name='receive_networks'), # Endpoint pour recevoir les réseaux scannés
    path('api/sensor/', views.receive_sensor_data, name='receive_sensor_data'), # Endpoint pour recevoir les données des capteurs
    path('sensor-data/', views.show_sensor_data, name='show_sensor_data'), # Afficher les données des capteurs
    path('sensor-data/json/', views.sensor_data_json, name='sensor_data_json'), # Endpoint pour obtenir les données des capteurs en JSON


    path('api/receive_sensor_data/', views.receive_sensor_data, name='receive_sensor_data'), # Endpoint pour recevoir les données des capteurs
    path('api/sensor_data_json/', views.sensor_data_json, name='sensor_data_json'), # Endpoint pour obtenir les données des capteurs en JSON
    path('capteurs/', views.show_sensor_data, name='show_sensor_data'), # Afficher les données des capteurs

]