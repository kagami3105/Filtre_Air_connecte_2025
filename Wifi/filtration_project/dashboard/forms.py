# On importe le module 'forms' de Django
# Il permet de créer facilement des formulaires HTML liés à des modèles ou indépendants.
from django import forms

# On importe les modèles nécessaires : Filter et WifiConfig
# Ces modèles servent à lier les formulaires à la base de données.
from .models import Filter
from .models import WifiConfig

# Définition d’un formulaire basé sur le modèle Filter

class FilterForm(forms.ModelForm):
    # La classe interne Meta décrit la configuration du formulaire

    class Meta:
        # Le modèle sur lequel le formulaire est basé

        model = Filter
        # Liste des champs du modèle qui seront visibles dans le formulaire
        fields = ['name', 'location', 'status', 'fan_speed', 'last_maintenance', 'notes']
        # On personnalise ici l’apparence du champ "last_maintenance"
        # 'type': 'date' permet d’afficher un sélecteur de date dans le navigateur 
        widgets = {
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }

# Définition d’un formulaire indépendant (non lié à un modèle)
class WifiConfigForm(forms.Form):
    # Champ pour le SSID du réseau Wi‑Fi
    ssid = forms.CharField(max_length=64, label="Nom du réseau (SSID)")
    # Champ pour le mot de passe du réseau Wi‑Fi
    password = forms.CharField(max_length=64, label="Mot de passe", widget=forms.PasswordInput)

# Définition d’un formulaire basé sur le modèle WifiConfig

class WifiConfigForm(forms.ModelForm):
    # La classe interne Meta décrit la configuration du formulaire
    class Meta:
        # Le modèle sur lequel le formulaire est basé
        model = WifiConfig
        # Liste des champs du modèle qui seront visibles dans le formulaire
        fields = ['ssid', 'password']
        # Personnalisation du widget pour le champ "password" afin de masquer la saisie
        widgets = {
            'password': forms.PasswordInput(render_value=True), # Affiche des points au lieu du texte saisi
        }
