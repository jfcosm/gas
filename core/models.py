from django.db import models
from django.contrib.auth.models import User

TAMANOS_CILINDRO = [
    (5, '5 kilos'),
    (15, '15 kilos'),
    (45, '45 kilos'),
]

class DistribuidorUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_fantasia = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_fantasia


class DistribuidorPrecio(models.Model):
    distribuidor = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text="Nombre o alias visible del local")
    region = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    url_mapa = models.URLField(blank=True)
    tamano_cilindro = models.IntegerField(choices=TAMANOS_CILINDRO)
    precio = models.PositiveIntegerField()
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.comuna} - {self.tamano_cilindro}kg - ${self.precio}"
