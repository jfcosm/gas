import json
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import DistribuidorPrecio
from .forms import RegistroDistribuidorForm, DistribuidorPrecioForm

# Precios simulados como fallback
PRECIOS_BASE = {
    "5": 11000,
    "15": 27000,
    "45": 69000,
}

def home(request):
    json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'comunas_regiones.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    regiones = [item["region"] for item in data["regiones"]]
    comunas_por_region = {item["region"]: item["comunas"] for item in data["regiones"]}

    region = request.GET.get("region")
    comuna = request.GET.get("comuna")
    tamano = request.GET.get("tamano")

    resultados = []
    resultado_simulado = None

    if region and comuna and tamano:
        resultados = DistribuidorPrecio.objects.filter(
            region=region,
            comuna=comuna,
            tamano_cilindro=int(tamano)
        ).order_by('precio')

        if not resultados.exists():
            precio_base = PRECIOS_BASE.get(tamano, 99999)
            resultado_simulado = {
                "comuna": comuna,
                "tamano": tamano,
                "precio": f"${precio_base:,}".replace(",", "."),
                "distribuidor": f"Distribuidora Gas {comuna} (simulado)",
            }

    return render(request, 'core/home.html', {
        'regiones': regiones,
        'comunas_por_region': comunas_por_region,
        'resultados': resultados,
        'resultado_simulado': resultado_simulado,
    })


def registro_distribuidor(request):
    if request.method == 'POST':
        form = RegistroDistribuidorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Ya puedes comenzar a publicar tus precios.')
            return redirect('panel_distribuidor')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroDistribuidorForm()
    return render(request, 'core/registro_distribuidor.html', {'form': form})


@login_required
def panel_distribuidor(request):
    precios = DistribuidorPrecio.objects.filter(distribuidor=request.user)
    return render(request, 'core/panel_distribuidor.html', {'precios': precios})


@login_required
def agregar_precio(request):
    if request.method == 'POST':
        form = DistribuidorPrecioForm(request.POST)
        if form.is_valid():
            precio = form.save(commit=False)
            precio.distribuidor = request.user
            precio.save()
            messages.success(request, 'Precio agregado correctamente.')
            return redirect('panel_distribuidor')
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = DistribuidorPrecioForm()
    return render(request, 'core/agregar_precio.html', {'form': form})


@login_required
def editar_precio(request, pk):
    precio = get_object_or_404(DistribuidorPrecio, pk=pk, distribuidor=request.user)
    
    if request.method == 'POST':
        form = DistribuidorPrecioForm(request.POST, instance=precio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Precio actualizado correctamente.')
            return redirect('panel_distribuidor')
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = DistribuidorPrecioForm(instance=precio)

    return render(request, 'core/editar_precio.html', {'form': form})
