import re
from matplotlib import axis
import pandas as pd

from evaluation.MCDA.criteria import print_table

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
BIOMASS_COLUMNS = {
    "harvest": [
        "year",
        "resource",
        "production",
        "yield_per_ha",
        "planted_area",
        "harvested_area",
    ],
    "livestock": [
        "year",
        "resource",
        "population",
        "small_farms",
        "medium_farms",
        "large_farms",
        "total_farms",
    ],
}


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
    file = file.rename(columns={"YEAR": "year", "MO": "month", "DY": "day"})
    file["Fecha"] = pd.to_datetime(file[["year", "month", "day"]])
    file["Fecha"] = file["Fecha"].dt.strftime("%Y-%m-%d")
    resource = {}
    if "ALLSKY_SFC_SW_DWN" in file.columns:

        resource = {
            "name": "Solar irradiance",
            "type_resource": "Solar",
            "source": "NASA",
            "unit": "kW-hr/m^2/day",
            "frequency": "Daily",
        }
        file = file.filter(items=["Fecha", "ALLSKY_SFC_SW_DWN"]).set_index("Fecha")
        resource["data"] = file["ALLSKY_SFC_SW_DWN"].to_dict()

    if "WS10M" in file.columns:

        resource = {
            "name": "Wind speed",
            "type_resource": "Wind",
            "source": "NASA",
            "unit": "m/s",
            "frequency": "Daily",
        }
        # Construir la columna de fecha a partir de las columnas 'YEAR', 'MO' y 'DY'
        file = file.filter(items=["Fecha", "WS10M"]).set_index("Fecha")
        resource["data"] = file["WS10M"].to_dict()

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


def process_data_ideam(file):
    # Leer el archivo data en un DataFrame
    resource = {
        "name": "Flow river",
        "type_resource": "Hydro",
        "source": "IDEAM",
        "unit": "m³/s",
        "frequency": "Daily",
    }
    file = file.filter(items=["Fecha", "Valor"]).set_index("Fecha")
    resource["data"] = file["Valor"].to_dict()
    # Devolver los datos en el formato necesario
    return resource


def process_biomass_data(file, data):
    resource = {
        "name": "Biogas",
        "type_resource": "Biomass",
        "source": "ICA",
        "unit": "m³/day",
        "frequency": "Monthly",
    }
    print(file)
    """ file["result"] = file[0.1] * file["Factor"]
    file = file.filter(items=["Fuente", "result"]).set_index("Fuente")
    resource["data"] = file["result"].to_dict() """
    return resource


def process_harvest_biomass(file):
    harvest_data = []
    resource = {
        "name": "Biogas",
        "type_resource": "Biomass",
        "source": "ICA",
        "unit": "ha",
        "frequency": "Yearly",
    }
    file = file.drop(columns=["year"])
    file = file.groupby(["resource"]).mean().reset_index()
    file = file.fillna(0, axis=1)
    for index, row in file.iterrows():
        row_data = resource.copy()
        row_data["name"] = row["resource"]
        data = {
            "production": row["production"],
            "yield_per_ha": row["yield_per_ha"],
            "planted_area": row["planted_area"],
            "harvested_area": row["harvested_area"],
        }
        row_data["data"] = data
        harvest_data.append(row_data)
    return harvest_data


def process_livestock_biomass(file):
    livestock_data = []
    resource = {
        "name": "Biogas",
        "type_resource": "Biomass",
        "source": "ICA",
        "unit": "population",
        "frequency": "Yearly",
    }
    file = file.drop(columns=["year"])
    file = file.groupby(["resource"]).mean().reset_index()
    file = file.fillna(0, axis=1)
    for index, row in file.iterrows():
        row_data = resource.copy()
        row_data["name"] = row["resource"]
        data = {
            "population": row["population"],
            "small_farms": row["small_farms"],
            "medium_farms": row["medium_farms"],
            "large_farms": row["large_farms"],
            "total_farms": row["total_farms"],
        }
        row_data["data"] = data
        livestock_data.append(row_data)
    return livestock_data


def load_csv(file_path):
    df = pd.read_csv(file_path)
    columns_extracted = df.columns.to_list()
    if columns_extracted == IDEAM_COLUMNS:
        return process_csv_ideam(df)
    elif set(NASA_COLUMNS).issubset(set(columns_extracted)):
        return process_csv_nasa(df)
    else:
        raise ValueError("Invalid CSV file format")


def load_excel(file_path):
    if file_path.endswith("biomasa.xlsx"):
        try:
            df_harvest = pd.read_excel(file_path, sheet_name="Historico Cultivos")
            df_livestock = pd.read_excel(file_path, sheet_name="Historico Pecuario")
            columns_extracted_hv = df_harvest.columns.to_list()
            columns_extracted_lv = df_livestock.columns.to_list()
            if not set(BIOMASS_COLUMNS["harvest"]).issubset(set(columns_extracted_hv)):
                raise ValueError("Invalid Excel file format for harvest data")
            if not set(BIOMASS_COLUMNS["livestock"]).issubset(
                set(columns_extracted_lv)
            ):
                raise ValueError("Invalid Excel file format for livestock data")
        except Exception as e:
            raise ValueError("Invalid Excel file format")

        data = process_harvest_biomass(df_harvest)
        data.extend(process_livestock_biomass(df_livestock))
        return data
    else:
        raise NotImplementedError("Excel file format not implemented")


def load_data(file_path):
    df = pd.read_csv(file_path, sep="|")
    columns_extracted = df.columns.to_list()
    if columns_extracted == ["Fecha", "Valor"]:
        return process_data_ideam(df)
    else:
        raise ValueError("Invalid data file format")


def format_values(data):
    df = pd.DataFrame(list(data.items()), columns=["date", "value"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    data_month = df.asfreq("ME", method="ffill")
    data_month["year"] = data_month.index.year
    data_month["month"] = pd.to_datetime(data_month.index.month, format="%m")
    data_month_piv = pd.pivot_table(
        data_month, index=["month"], columns=["year"], values=["value"]
    )
    data_month_piv = data_month_piv.sort_index()
    data_month_piv.index = data_month_piv.index.month_name()
    data_month["month"] = data_month["month"].dt.month_name()
    data_month_piv = data_month_piv.dropna(axis=1)
    return data_month, data_month_piv
