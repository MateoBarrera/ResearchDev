from multiprocessing import process
from django.urls import include
import pandas as pd

IDEAM_COLUMNS = [
    "CodigoEstacion",
    "NombreEstacion",
    "Latitud",
    "Longitud",
    "Altitud",
    "Categoria",
    "Entidad",
    "AreaOperativa",
    "Departamento",
    "Municipio",
    "FechaInstalacion",
    "FechaSuspension",
    "IdParametro",
    "Etiqueta",
    "DescripcionSerie",
    "Frecuencia",
    "Fecha",
    "Valor",
    "Grado",
    "Calificador",
    "NivelAprobacion",
]
NASA_COLUMNS = [
    "YEAR",
    "MO",
    "DY",
]


def __transform_frequency(frequency):

    if frequency == "Horaria":
        return "Hourly"
    elif frequency == "Diaria":
        return "Daily"
    elif frequency == "Mensual":
        return "Monthly"
    elif frequency == "Anual":
        return "annual"
    else:
        raise ValueError("Invalid frequency value")


def process_csv_nasa(file):
    # Leer el archivo CSV en un DataFrame
    resource = {}
    if "ALLSKY_SFC_SW_DWN" in file.columns:

        resource = {
            "name": "Solar irradiance",
            "type_resource": "Solar",
            "source": "NASA",
            "unit": "kW-hr/m^2/day",
            "frequency": "Daily",  # Asumiendo que los datos de la NASA son diarios
        }
        # Construir la columna de fecha a partir de las columnas 'YEAR', 'MO' y 'DY'
        file = file.rename(columns={"YEAR": "year", "MO": "month", "DY": "day"})
        file["Fecha"] = pd.to_datetime(file[["year", "month", "day"]])
        file["Fecha"] = file["Fecha"].dt.strftime("%Y-%m-%d")
        file = file.filter(items=["Fecha", "ALLSKY_SFC_SW_DWN"]).set_index("Fecha")
        resource["data"] = file["ALLSKY_SFC_SW_DWN"].to_dict()

    # Devolver los datos en el formato necesario
    return resource


def process_csv_ideam(file):
    # Leer el archivo CSV en un DataFrame
    resource = {}
    if file["IdParametro"].unique() == "CAUDAL":

        resource = {
            "name": "Flow river",
            "type_resource": "Hydro",
            "source": "IDEAM",
            "unit": "m³/s",
            "frequency": __transform_frequency(file.iloc[0]["Frecuencia"]),
        }
        file = file.filter(items=["Fecha", "Valor"]).set_index("Fecha")
        resource["data"] = file["Valor"].to_dict()

    # Devolver los datos en el formato necesario
    return resource


def load_csv(file_path):
    df = pd.read_csv(file_path)
    columns_extracted = df.columns.to_list()
    if columns_extracted == IDEAM_COLUMNS:
        return process_csv_ideam(df)
    elif set(NASA_COLUMNS).issubset(set(columns_extracted)):
        return process_csv_nasa(df)
    else:
        raise ValueError("Invalid CSV file format")
