from django.db import models

class Filter(models.Model):
    # Nom du filtre (ex: "Salle serveurs")
    name = models.CharField(max_length=100)
    # Emplacement physique du filtre
    location = models.CharField(max_length=100)
    # Etat marche/arrêt
    status = models.BooleanField(default=False)   # On/Off
    # Vitesse du ventilateur (0-100)
    fan_speed = models.IntegerField(default=0)    # 0-100
    # Date de la dernière maintenance (obligatoire dans ce modèle)
    last_maintenance = models.DateField()
    # Notes libres (peut être vide)
    notes = models.TextField(blank=True)

    def __str__(self):
        # Représentation lisible dans l'admin et les logs
        return self.name

class MicrocontrollerData(models.Model):
    # Relation many-to-one vers Filter :
    # plusieurs MicrocontrollerData peuvent référencer le même Filter.
    # on_delete=models.CASCADE : si le Filter est supprimé, les données liées sont aussi supprimées.
    # related_name='data' : accès inverse depuis un Filter via filter.data.all()
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, related_name='data')
    # Mesures prises par le microcontrôleur
    temperature = models.FloatField()
    humidity = models.FloatField()
    # Horodatage automatique à la création
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche "NomDuFilter @ timestamp"
        return f"{self.filter.name} @ {self.timestamp}"
    
class WifiConfig(models.Model):
    # SSID et mot de passe (ici stockés en clair — voir remarque sécurité)
    ssid = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=64, blank=True)
    # Mise à jour automatique quand l'objet est sauvegardé
    last_updated = models.DateTimeField(auto_now=True)

class DeviceStatus(models.Model):
    # Indique si le dispositif est connecté (ex: l'ESP)
    connected = models.BooleanField(default=False)
    # IP du device (texte; max 64 pour laisser de la marge)
    ip_address = models.CharField(max_length=64, blank=True)
    # Dernière fois où le device a checké le statut
    last_checkin = models.DateTimeField(auto_now=True)
    # Message libre (ex: "Connecté" / "Échec Wi‑Fi")
    message = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"Connected: {self.connected} IP: {self.ip_address}"

class ScannedNetwork(models.Model):
    # Réseaux Wi‑Fi scannés par un device (ex: SSID trouvé)
    ssid = models.CharField(max_length=64)
    rssi = models.IntegerField()      # puissance du signal
    secure = models.BooleanField()    # vrai si le réseau est chiffré (WPA/WEP/etc.)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ssid


class SensorData(models.Model):
    sensor_type = models.CharField(max_length=50)
    value = models.FloatField()
    unit = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
