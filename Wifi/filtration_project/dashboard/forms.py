from django import forms
from .models import Filter
from .models import WifiConfig

class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['name', 'location', 'status', 'fan_speed', 'last_maintenance', 'notes'] 
        widgets = {
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }

class WifiConfigForm(forms.Form):
    ssid = forms.CharField(max_length=64, label="Nom du réseau (SSID)")
    password = forms.CharField(max_length=64, label="Mot de passe", widget=forms.PasswordInput)


class WifiConfigForm(forms.ModelForm):
    class Meta:
        model = WifiConfig
        fields = ['ssid', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
