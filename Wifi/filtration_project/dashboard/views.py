from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .models import Filter, MicrocontrollerData
from .forms import FilterForm, WifiConfigForm

from .models import WifiConfig, DeviceStatus
from .forms import WifiConfigForm

from django.utils import timezone

from .models import ScannedNetwork, WifiConfig
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
from .models import ScannedNetwork
from . import api

from django.core.serializers.json import DjangoJSONEncoder
from .models import SensorData
from django.db.models import Avg

from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

 # fonctions de vue pour le dashboard
@login_required
def dashboard_view(request): # Affiche le tableau de bord principal avec la liste des filtres
    filters = Filter.objects.prefetch_related('data').all() # Précharge les données associées pour optimisation
    return render(request, 'dashboard/dashboard.html', {'filters': filters}) # Fournit les filtres au template

# fonctions de vue pour la gestion des filtres
def filter_create(request):
    if request.method == 'POST': # création d'un nouveau filtre
        form = FilterForm(request.POST) # formulaire soumis
        if form.is_valid(): # si le formulaire est valide
            form.save() # on sauvegarde le nouveau filtre
            return redirect('dashboard:dashboard') # redirection vers le tableau de bord
    else:
        form = FilterForm() # sinon, on affiche un formulaire vide
    return render(request, 'dashboard/filter_form.html', {'form': form, 'title': 'Créer un filtre'}) # rendu du formulaire

# fonctions de vue pour la modification, suppression et détails des filtres
def filter_update(request, pk): # Modifie un filtre existant
    filter_obj = get_object_or_404(Filter, pk=pk) # Récupère le filtre ou renvoie 404
    if request.method == 'POST': # si le formulaire est soumis
        form = FilterForm(request.POST, instance=filter_obj) # formulaire avec les données existantes
        if form.is_valid(): # si le formulaire est valide
            form.save() # on sauvegarde les modifications
            return redirect('dashboard:filter_detail', pk=pk) # on redirige vers la page de détails du filtre
    else:
        form = FilterForm(instance=filter_obj) # sinon, on affiche le formulaire pré-rempli
    return render(request, 'dashboard/filter_form.html', {'form': form, 'title': 'Modifier le filtre'}) # rendu du formulaire

# fonctions de vue pour la suppression des filtres
def filter_delete(request, pk): # Supprime un filtre existant
    filter_obj = get_object_or_404(Filter, pk=pk) # Récupère le filtre ou renvoie 404
    if request.method == 'POST': # si le formulaire de confirmation est soumis
        filter_obj.delete() # on supprime le filtre
        return redirect('dashboard:dashboard') # on redirige vers le tableau de bord
    return render(request, 'dashboard/filter_detail.html', {'filter': filter_obj, 'delete_mode': True}) # rendu de la confirmation

# fonctions de vue pour les détails des filtres
def filter_detail(request, pk): # Affiche les détails d'un filtre
    filter_obj = get_object_or_404(Filter, pk=pk) # Récupère le filtre ou renvoie 404
    return render(request, 'dashboard/filter_detail.html', {'filter': filter_obj}) # rendu des détails du filtre

# fonctions de vue pour les actions sur les filtres (toggle, set speed)
@require_POST # Toggle marche/arrêt du filtre
def toggle_filter(request, pk): # bascule le statut du filtre
    f = get_object_or_404(Filter, pk=pk) # on récupère le filtre
    f.status = not f.status # on inverse le statut
    f.save() # on sauvegarde
    return JsonResponse({'status': f.status}) # on renvoie le nouveau statut en JSON

# fonctions de vue pour définir la vitesse du ventilateur
@require_POST # Définit la vitesse du ventilateur
def set_speed(request, pk): # définit la vitesse du ventilateur
    f = get_object_or_404(Filter, pk=pk) # on récupère le filtre
     # on récupère la vitesse depuis la requête POST
    try:
        speed = int(request.POST.get('fan_speed', f.fan_speed)) # on fait un cast en int
    except ValueError: # si ce n'est pas un int valide
        return HttpResponseBadRequest('Invalid speed') # on renvoie une erreur 400
     # on clamp la vitesse entre 0 et 100
    f.fan_speed = max(0, min(speed, 100))  # clamp entre 0 et 100
    f.save() # on sauvegarde
     # on renvoie la nouvelle vitesse en JSON
    return JsonResponse({'fan_speed': f.fan_speed}) # on renvoie la nouvelle vitesse en JSON

# fonctions de vue pour afficher les données des microcontrôleurs
def data_list(request): # Affiche la liste des données des microcontrôleurs
     # on récupère les 50 dernières entrées avec les filtres associés
    data = MicrocontrollerData.objects.select_related('filter').order_by('-timestamp')[:50]
    return render(request, 'dashboard/data_list.html', {'data': data}) # on rend le template avec les données

# fonctions de vue pour la configuration Wi-Fi
def wifi_setup(request): # Configure le Wi-Fi du dispositif
     # Si le formulaire est soumis
    if request.method == 'POST': # on traite le formulaire
        form = WifiConfigForm(request.POST) # on crée le formulaire avec les données POST
         # si le formulaire est valide
        if form.is_valid():
            request.session['wifi_ssid'] = form.cleaned_data['ssid'] # on stocke les données en session
            request.session['wifi_password'] = form.cleaned_data['password'] # on stocke les données en session
             # redirection vers la même page (GET)
            return redirect('dashboard:wifi_setup')
    else:
        form = WifiConfigForm(initial={
            'ssid': request.session.get('wifi_ssid', ''), # on pré-remplit avec les données en session
            'password': request.session.get('wifi_password', ''), # on pré-remplit avec les données en session
        })
    return render(request, 'dashboard/wifi_setup.html', {'form': form}) # on rend le template avec le formulaire

# fonctions de vue pour la configuration Wi-Fi avec sauvegarde en base de données
def wifi_setup(request): # Configure le Wi-Fi du dispositif
    wifi, _ = WifiConfig.objects.get_or_create(id=1)  # un seul enregistrement
    status, _ = DeviceStatus.objects.get_or_create(id=1) # un seul enregistrement

    if request.method == 'POST': # si le formulaire est soumis
        form = WifiConfigForm(request.POST, instance=wifi) # on stocke les données dans la base
         # si le formulaire est valide
        if form.is_valid():
            form.save() # on sauvegarde les modifications
             # redirection vers la même page (GET)
            return redirect('dashboard:wifi_setup')
    else:
        form = WifiConfigForm(instance=wifi) # sinon, on affiche le formulaire avec les données existantes

    return render(request, 'dashboard/wifi_setup.html', {
        'form': form,
        'status': status
    }) # on rend le template avec le formulaire

# fonctions de vue pour afficher les réseaux Wi-Fi scannés
def show_networks(request):
    networks = ScannedNetwork.objects.order_by('-timestamp')[:20] # derniers réseaux scannés

    if request.method == 'POST': # si le formulaire est soumis
         # on récupère le SSID et le mot de passe
        ssid = request.POST.get('ssid')
        password = request.POST.get('password', '') # mot de passe optionnel
         # on sauvegarde dans la configuration Wi-Fi
        wifi, _ = WifiConfig.objects.get_or_create(id=1) # un seul enregistrement
         # on met à jour les champs
        wifi.ssid = ssid # on sauvegarde le SSID
        wifi.password = password # on sauvegarde
         # on sauvegarde les modifications
        wifi.save()
        return redirect('dashboard:wifi_setup')  # ou 'dashboard:show_networks'

    return render(request, 'dashboard/networks.html', {'networks': networks}) # on rend le template avec les réseaux


# fonctions de vue pour recevoir les réseaux Wi-Fi scannés via une API
@csrf_exempt
def receive_networks(request): # Reçoit les réseaux Wi-Fi scannés via une API
    if request.method == 'POST': # si la méthode est POST
         # on parse le JSON
        data = json.loads(request.body)
        ScannedNetwork.objects.all().delete() # on supprime les anciens réseaux
         # on crée les nouveaux réseaux
        for net in data.get("networks", []): # on itère sur les réseaux
             # on crée une nouvelle entrée dans la base de données
            ScannedNetwork.objects.create(
                ssid=net["ssid"], # on sauvegarde le SSID
                 # on sauvegarde la puissance du signal
                rssi=net["rssi"], # on sauvegarde si le réseau est sécurisé
                 # on sauvegarde si le réseau est sécurisé
                secure=net["secure"] # on sauvegarde l'horodatage automatique
            ) 
        return JsonResponse({"status": "ok"}) # on renvoie un statut OK
    return JsonResponse({"error": "Invalid method"}, status=405) # on retourne une erreur si la méthode n'est pas POST


# dashboard/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SensorData

# api endpoint pour recevoir les données des capteurs
@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST': # si la méthode est POST
         # on parse le JSON
        try: # on parse le JSON
             # on crée une nouvelle entrée dans la base de données
            data = json.loads(request.body)
            SensorData.objects.create( # on crée une nouvelle entrée
                 # on sauvegarde le type de capteur
                sensor_type=data.get("sensor_type", "unknown"),
                value=data.get("value", 0), # on sauvegarde la valeur mesurée
                 # on sauvegarde l'unité de la mesure
                unit=data.get("unit", "")
            )
            return JsonResponse({"status": "ok"}) # on renvoie un statut OK
         # gestion des erreurs de parsing ou de création
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) # on retourne une erreur 500
     # si la méthode n'est pas POST
    return JsonResponse({"error": "Méthode non autorisée"}, status=405) # on retourne une erreur 405




# def show_sensor_data(request):
#     data = SensorData.objects.order_by('timestamp')[:50]

#     chart_data = {
#         "labels": [d.timestamp.strftime("%H:%M:%S") for d in data],
#         "values": [d.value for d in data],
#     }

#     return render(request, 'dashboard/sensor_data.html', {
#         'data': data,
#         'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder)
#     })

# def sensor_data_json(request):
#     data = SensorData.objects.order_by('timestamp')[:50]
#     chart_data = {
#         "labels": [d.timestamp.strftime("%H:%M:%S") for d in data],
#         "values": [d.value for d in data],
#     }
#     return JsonResponse(chart_data)

# api endpoint pour fournir les données des capteurs en JSON
def sensor_data_json(request):
    data = SensorData.objects.order_by('timestamp')  # toutes les données
    chart_data = { 
        "labels": [d.timestamp.strftime("%H:%M:%S") for d in data], # les horodatages formatés
        "values": [d.value for d in data], # les valeurs mesurées
         # les lignes de données détaillées
        "rows": [
            {
                "sensor_type": d.sensor_type, # le type de capteur
                "value": d.value, # la valeur mesurée
                "unit": d.unit, # l'unité de la mesure
                 # l'horodatage formaté
                "timestamp": d.timestamp.strftime("%H:%M:%S %d/%m/%Y")
            }
            for d in data # on crée une liste de dictionnaires pour chaque entrée
        ]
    }
    return JsonResponse(chart_data) # on renvoie les données en JSON


# def show_sensor_data(request):
#     data = SensorData.objects.order_by('timestamp')  # toutes les données

#     chart_data = {
#         "labels": [d.timestamp.strftime("%H:%M:%S") for d in data],
#         "values": [d.value for d in data],
#         "rows": [
#             {
#                 "sensor_type": d.sensor_type,
#                 "value": d.value,
#                 "unit": d.unit,
#                 "timestamp": d.timestamp.strftime("%H:%M:%S %d/%m/%Y")
#             }
#             for d in data
#         ]
#     }

#     return render(request, 'dashboard/sensor_data.html', {
#         'data': data,
#         'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder)
#     })

# fonctions de vue pour afficher les données des capteurs avec statistiques
def show_sensor_data(request):
    # On récupère uniquement les données de température
    data = SensorData.objects.filter(sensor_type='temperature').order_by('-timestamp')[:20]


    # Moyenne des températures
    avg_temp = SensorData.objects.filter(sensor_type='temperature').aggregate(Avg('value'))['value__avg']

    # Dernière mise à jour
    last_update = data.first().timestamp if data.exists() else None

    return render(request, 'dashboard/sensor_data.html', { 
        'data': data,
        'average': avg_temp,
        'last_update': last_update,
        'now': timezone.now()
    }) # on rend le template avec les données et statistiques


fan_speed = 0  # variable globale (0–100)
@csrf_exempt
def fan_speed_api(request):
    """Renvoie ou met à jour la vitesse du ventilateur."""
    from .models import Filter
    import json

    if request.method == "GET":
        f = Filter.objects.first()
        if not f:
            return JsonResponse({"fan_speed": 0})
        # Si c’est un champ du modèle :
        return JsonResponse({"fan_speed": int(f.fan_speed)})

    elif request.method == "POST":
        data = json.loads(request.body)
        new_speed = max(0, min(100, int(data.get("fan_speed", 0))))
        f = Filter.objects.first()
        if f:
            f.fan_speed = new_speed
            f.save()
            return JsonResponse({"status": "ok", "fan_speed": f.fan_speed})
        return JsonResponse({"error": "Aucun filtre trouvé"}, status=404)



@csrf_exempt
def fan_speed(request):
    """Renvoie la vitesse actuelle du ventilateur."""
    if request.method == "GET":
        f = Filter.objects.first()
        return JsonResponse({"fan_speed": f.fan_speed if f else 0})

    elif request.method == "POST":
        import json
        data = json.loads(request.body)
        f = Filter.objects.first()
        if f:
            f.fan_speed = max(0, min(100, data.get("fan_speed", 0)))
            f.save()
            return JsonResponse({"status": "ok", "fan_speed": f.fan_speed})
        return JsonResponse({"error": "Aucun filtre trouvé"}, status=404)


  

# === Connexion ===
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:index")  # ou ta page principale
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "dashboard/login.html")

# === Déconnexion ===
def user_logout(request):
    logout(request)
    return redirect("login")

# === Exemple de page protégée ===
@login_required
def dashboard_home(request):
    # ton code actuel pour afficher le dashboard
    filters = Filter.objects.all()
    return render(request, "dashboard/dashboard.html", {"filters": filters})
 
