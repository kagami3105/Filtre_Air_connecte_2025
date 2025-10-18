# from django.contrib import admin

# from .models import Filter, MicrocontrollerData

# @admin.register(Filter)
# class FilterAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location', 'status', 'fan_speed', 'last_maintenance') 
#     search_fields = ('name', 'location')

# @admin.register(MicrocontrollerData)
# class MicrocontrollerDataAdmin(admin.ModelAdmin):
#     list_display = ('filter', 'temperature', 'humidity', 'timestamp')
#     list_filter = ('filter',)


# On importe le module admin de Django, qui permet de gérer les modèles depuis l’interface d’administration
from django.contrib import admin

# On importe les modèles que l’on souhaite enregistrer dans l’interface admin
from .models import Filter, MicrocontrollerData

# Configuration de l’affichage du modèle Filter dans l’interface d’administration
@admin.register(Filter)  # Décorateur : enregistre automatiquement le modèle Filter dans l’admin
class FilterAdmin(admin.ModelAdmin):  # On crée une classe d’administration spécifique à Filter
    # Définit les colonnes à afficher dans la liste des filtres (page principale du modèle)
    list_display = ('name', 'location', 'status', 'fan_speed', 'last_maintenance') 
    
    # Permet de rechercher un filtre selon son nom ou sa localisation dans la barre de recherche
    search_fields = ('name', 'location')


# Configuration de l’affichage du modèle MicrocontrollerData dans l’interface d’administration
@admin.register(MicrocontrollerData)  # Décorateur : enregistre automatiquement le modèle MicrocontrollerData dans l’admin
class MicrocontrollerDataAdmin(admin.ModelAdmin):  # Classe d’administration pour le modèle MicrocontrollerData
    # Définit les colonnes affichées dans la liste des données envoyées par les microcontrôleurs
    list_display = ('filter', 'temperature', 'humidity', 'timestamp')
    
    # Permet de filtrer les données affichées par filtre associé (utile s’il y a plusieurs filtres)
    list_filter = ('filter',)
