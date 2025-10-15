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
import json
from .models import SensorData



def dashboard_view(request):
    filters = Filter.objects.prefetch_related('data').all()
    return render(request, 'dashboard/dashboard.html', {'filters': filters})

def filter_create(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    else:
        form = FilterForm()
    return render(request, 'dashboard/filter_form.html', {'form': form, 'title': 'Créer un filtre'})

def filter_update(request, pk):
    filter_obj = get_object_or_404(Filter, pk=pk)
    if request.method == 'POST':
        form = FilterForm(request.POST, instance=filter_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:filter_detail', pk=pk)
    else:
        form = FilterForm(instance=filter_obj)
    return render(request, 'dashboard/filter_form.html', {'form': form, 'title': 'Modifier le filtre'})

def filter_delete(request, pk):
    filter_obj = get_object_or_404(Filter, pk=pk)
    if request.method == 'POST':
        filter_obj.delete()
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/filter_detail.html', {'filter': filter_obj, 'delete_mode': True})

def filter_detail(request, pk):
    filter_obj = get_object_or_404(Filter, pk=pk)
    return render(request, 'dashboard/filter_detail.html', {'filter': filter_obj})

@require_POST
def toggle_filter(request, pk):
    f = get_object_or_404(Filter, pk=pk)
    f.status = not f.status
    f.save()
    return JsonResponse({'status': f.status})

@require_POST
def set_speed(request, pk):
    f = get_object_or_404(Filter, pk=pk)
    try:
        speed = int(request.POST.get('fan_speed', f.fan_speed))
    except ValueError:
        return HttpResponseBadRequest('Invalid speed')
    f.fan_speed = max(0, min(speed, 100))  # clamp
    f.save()
    return JsonResponse({'fan_speed': f.fan_speed})

def data_list(request):
    data = MicrocontrollerData.objects.select_related('filter').order_by('-timestamp')[:50]
    return render(request, 'dashboard/data_list.html', {'data': data})

def wifi_setup(request):
    if request.method == 'POST':
        form = WifiConfigForm(request.POST)
        if form.is_valid():
            request.session['wifi_ssid'] = form.cleaned_data['ssid']
            request.session['wifi_password'] = form.cleaned_data['password']
            return redirect('dashboard:wifi_setup')
    else:
        form = WifiConfigForm(initial={
            'ssid': request.session.get('wifi_ssid', ''),
            'password': request.session.get('wifi_password', ''),
        })
    return render(request, 'dashboard/wifi_setup.html', {'form': form})


def wifi_setup(request):
    wifi, _ = WifiConfig.objects.get_or_create(id=1)  # un seul enregistrement
    status, _ = DeviceStatus.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = WifiConfigForm(request.POST, instance=wifi)
        if form.is_valid():
            form.save()
            return redirect('dashboard:wifi_setup')
    else:
        form = WifiConfigForm(instance=wifi)

    return render(request, 'dashboard/wifi_setup.html', {
        'form': form,
        'status': status
    })

def show_networks(request):
    networks = ScannedNetwork.objects.order_by('-timestamp')[:20]

    if request.method == 'POST':
        ssid = request.POST.get('ssid')
        password = request.POST.get('password', '')
        wifi, _ = WifiConfig.objects.get_or_create(id=1)
        wifi.ssid = ssid
        wifi.password = password
        wifi.save()
        return redirect('dashboard:wifi_setup')  # ou 'dashboard:show_networks'

    return render(request, 'dashboard/networks.html', {'networks': networks})


@csrf_exempt
def receive_networks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ScannedNetwork.objects.all().delete()
        for net in data.get("networks", []):
            ScannedNetwork.objects.create(
                ssid=net["ssid"],
                rssi=net["rssi"],
                secure=net["secure"]
            )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid method"}, status=405)


# dashboard/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SensorData

@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            SensorData.objects.create(
                sensor_type=data.get("sensor_type", "unknown"),
                value=data.get("value", 0),
                unit=data.get("unit", "")
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def show_sensor_data(request):
    data = SensorData.objects.order_by('timestamp')[:50]

    chart_data = {
        "labels": [d.timestamp.strftime("%H:%M:%S") for d in data],
        "values": [d.value for d in data],
    }

    return render(request, 'dashboard/sensor_data.html', {
        'data': data,
        'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder)
    })

def sensor_data_json(request):
    data = SensorData.objects.order_by('timestamp')[:50]
    chart_data = {
        "labels": [d.timestamp.strftime("%H:%M:%S") for d in data],
        "values": [d.value for d in data],
    }
    return JsonResponse(chart_data)


