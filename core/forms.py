from django import forms
from django.contrib.auth.models import User
from .models import DistribuidorUsuario, DistribuidorPrecio

import json
import os
from django.conf import settings
from django.core.exceptions import ValidationError


# Función auxiliar
def cargar_regiones_comunas():
    json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'comunas_regiones.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    regiones = [(r['region'], r['region']) for r in data['regiones']]
    comunas = [(c, c) for r in data['regiones'] for c in r['comunas']]
    return regiones, comunas

class RegistroDistribuidorForm(forms.ModelForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    region = forms.ChoiceField(choices=[])
    comuna = forms.ChoiceField(choices=[])

    class Meta:
        model = DistribuidorUsuario
        fields = ['nombre_fantasia', 'region', 'comuna']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        regiones, comunas = cargar_regiones_comunas()
        self.fields['region'].choices = regiones

        # Si ya se seleccionó una región, ajustar las comunas dinámicamente
        if 'region' in self.data:
            region_seleccionada = self.data.get('region')
            json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'comunas_regiones.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            comunas_region = []
            for r in data['regiones']:
                if r['region'] == region_seleccionada:
                    comunas_region = [(c, c) for c in r['comunas']]
                    break
            self.fields['comuna'].choices = comunas_region
        else:
            self.fields['comuna'].choices = []


    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        distribuidor = super().save(commit=False)
        distribuidor.user = user
        if commit:
            distribuidor.save()
        return user

    # método nuevo
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ya existe un usuario con ese nombre de usuario.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe una cuenta registrada con este correo.")
        return email


class DistribuidorPrecioForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[])
    comuna = forms.ChoiceField(choices=[])

    class Meta:
        model = DistribuidorPrecio
        fields = ['nombre', 'region', 'comuna', 'tamano_cilindro', 'precio', 'direccion', 'url_mapa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'tamano_cilindro': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'url_mapa': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Carga regiones y comunas desde el JSON
        regiones, comunas = cargar_regiones_comunas()
        self.fields['region'].choices = regiones

        if 'region' in self.data:
            region_seleccionada = self.data.get('region')
            json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'comunas_regiones.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            comunas_region = []
            for r in data['regiones']:
                if r['region'] == region_seleccionada:
                    comunas_region = [(c, c) for c in r['comunas']]
                    break
            self.fields['comuna'].choices = comunas_region
        else:
            self.fields['comuna'].choices = []
