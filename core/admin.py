from django.contrib import admin

# Register your models here.
from .models import DistribuidorPrecio

@admin.register(DistribuidorPrecio)
class DistribuidorPrecioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comuna', 'region', 'tamano_cilindro', 'precio', 'actualizado')
    list_filter = ('region', 'comuna', 'tamano_cilindro')
    search_fields = ('nombre', 'comuna', 'region')
