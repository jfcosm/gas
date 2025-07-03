from django.contrib import admin

# Register your models here.
from .models import DistribuidorPrecio

@admin.register(DistribuidorPrecio)
class DistribuidorPrecioAdmin(admin.ModelAdmin):
    list_display = ('distribuidor', 'region', 'comuna', 'tamano_cilindro', 'precio_retiro', 'precio_despacho')
    list_filter = ('region', 'comuna', 'tamano_cilindro')
    search_fields = ('nombre', 'comuna', 'region')
