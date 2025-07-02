import csv
from django.core.management.base import BaseCommand
from core.models import DistribuidorPrecio

class Command(BaseCommand):
    help = 'Importa precios de distribuidores desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            total = 0
            for row in reader:
                obj, created = DistribuidorPrecio.objects.update_or_create(
                    nombre=row['nombre'],
                    comuna=row['comuna'],
                    tamano_cilindro=int(row['tamano_cilindro']),
                    defaults={
                        'region': row['region'],
                        'direccion': row['direccion'],
                        'latitud': float(row['latitud']) if row['latitud'] else None,
                        'longitud': float(row['longitud']) if row['longitud'] else None,
                        'url_mapa': row['url_mapa'],
                        'precio': int(row['precio']),
                    }
                )
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Se importaron o actualizaron {total} registros'))
