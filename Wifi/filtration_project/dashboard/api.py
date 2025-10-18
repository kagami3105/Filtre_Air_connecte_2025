# dashboard/api.py
# Endpoints HTTP simples pour que le microcontrôleur (ESP) poste/obtienne des données.
# Utilise JsonResponse pour renvoyer des réponses JSON et HttpResponseBadRequest pour
# renvoyer une 400 en cas de payload invalide.

import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Import des modèles utilisés pour stocker/répondre aux données
from .models import Filter, MicrocontrollerData
from .models import WifiConfig, DeviceStatus


# Endpoint POST pour que le microcontrôleur envoie une lecture de capteurs
# URL attendue par ex: POST /api/mcu/data/3/  (3 = filter_id)
# Corps attendu: JSON contenant les clés "temperature" et "humidity"
# Exemple payload: {"temperature": 22.5, "humidity": 55.0}
#
# Décorateurs:
# - @csrf_exempt : autorise les requêtes POST sans token CSRF (utile pour devices IoT)
# - @require_http_methods(['POST']) : n'accepte que les méthodes POST
@csrf_exempt
@require_http_methods(['POST'])
def mcu_post_data(request, filter_id):
    try:
        # On lit le corps de la requête et on parse le JSON
        payload = json.loads(request.body.decode('utf-8'))
        # On force le type pour s'assurer que les valeurs sont bien numériques
        temperature = float(payload['temperature'])
        humidity = float(payload['humidity'])
    except (KeyError, ValueError, json.JSONDecodeError):
        # KeyError : clé manquante dans le JSON
        # ValueError : conversion en float a échoué
        # JSONDecodeError : JSON malformé
        return HttpResponseBadRequest('Invalid payload')

    # On récupère l'objet Filter correspondant (ou None si inexistant)
    f = Filter.objects.filter(pk=filter_id).first()
    if not f:
        # Si le filter_id n'existe pas, on renvoie 400 (mauvaise requête)
        return HttpResponseBadRequest('Unknown filter')

    # Création et sauvegarde d'une nouvelle entrée MicrocontrollerData liée au Filter
    d = MicrocontrollerData.objects.create(filter=f, temperature=temperature, humidity=humidity)

    # On renvoie un JSON confirmant l'opération et l'id de l'enregistrement créé
    return JsonResponse({'ok': True, 'id': d.id})


# Endpoint GET pour que le microcontrôleur récupère l'état du filtre (on/off et vitesse)
# Exemple: GET /api/mcu/filter/3/state/
# Renvoie: {"status": true, "fan_speed": 50}
@require_http_methods(['GET'])
def mcu_get_filter_state(request, filter_id):
    # On récupère le Filter demandé
    f = Filter.objects.filter(pk=filter_id).first()
    if not f:
        return HttpResponseBadRequest('Unknown filter')
    # On renvoie le statut et la vitesse du ventilateur en JSON
    return JsonResponse({'status': f.status, 'fan_speed': f.fan_speed})


# Ancien/optionnel: endpoint pour récupérer la config Wi‑Fi depuis la session HTTP
# Ici, il lit la config stockée dans la session Django (probablement utilisée côté web admin)
# Exemple: GET /api/mcu/get_wifi_config/
# Remarque: utiliser la session n'est pas adapté pour un device IoT — utiliser une table (WifiConfig) est préférable.
@require_http_methods(['GET'])
def mcu_get_wifi_config(request):
    ssid = request.session.get('wifi_ssid', '')
    password = request.session.get('wifi_password', '')
    return JsonResponse({'ssid': ssid, 'password': password})


# Endpoint GET pour récupérer la configuration Wi‑Fi stockée dans la DB (modèle WifiConfig)
# Si aucun enregistrement n'existe, get_or_create(id=1) en crée un (singleton simple)
# Renvoie: {"ssid": "...", "password": "..."}
@require_http_methods(['GET'])
def mcu_get_wifi(request):
    wifi, _ = WifiConfig.objects.get_or_create(id=1)
    return JsonResponse({'ssid': wifi.ssid, 'password': wifi.password})


# Endpoint POST pour que le microcontrôleur envoie son statut (connecté, IP, message)
# Exemple payload: {"connected": true, "ip_address": "192.168.1.100", "message": "Connecté"}
#
# Mêmes remarques CSRF/HTTP que pour mcu_post_data
@csrf_exempt
@require_http_methods(['POST'])
def mcu_post_status(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        # On récupère les champs en donnant des valeurs par défaut si absents
        connected = bool(payload.get('connected', False))
        ip = str(payload.get('ip_address', ''))
        message = str(payload.get('message', ''))
    except (ValueError, json.JSONDecodeError):
        # JSON invalide ou mauvaise conversion
        return HttpResponseBadRequest('Invalid payload')

    # On stocke et on met à jour un singleton DeviceStatus (id=1)
    status, _ = DeviceStatus.objects.get_or_create(id=1)
    status.connected = connected
    status.ip_address = ip
    status.message = message
    status.save()

    # Réponse JSON minimale confirmant l'opération
    return JsonResponse({'ok': True})
