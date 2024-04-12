import csv
import json
from django.core.management.base import BaseCommand
from api.models import ResourceVariable
from api.schemas import TimeSerieItem
from api.enums import Frequency
from datetime import datetime


class Command(BaseCommand):
    help = "Ingest resources from CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_files", nargs="+", type=str, help="CSV files to ingest"
        )

    def handle(self, *args, **options):
        csv_files = options["csv_files"]
        for csv_file in csv_files:
            with open(csv_file, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la cabecera del CSV
                time_series = []
                for row in reader:
                    # Crear un diccionario para almacenar la serie de tiempo
                    time_series.append({"time_stamp": row[16], "value": row[17]})

                resource_variable = ResourceVariable(
                    name=row[1],  # NombreEstacion
                    unit="m^3/s",  # IdParametro
                    source="IDEAM",  # Fuente fija
                    frequency="Monthly",  # Frecuencia
                    time_series=time_series,  # Serie de tiempo
                )
                resource_variable.save()
