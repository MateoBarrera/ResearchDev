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
BIOMASS_COLUMNS = ["Fuente", "Recomendado", "Factor", "Total"]


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


def process_biomass_data(file):
    resource = {
        "name": "Biogas",
        "type_resource": "Biomass",
        "source": "ICA",
        "unit": "m³/day",
        "frequency": "Monthly",
    }
    print(file)
    file["result"] = file[0.1] * file["Factor"]
    file = file.filter(items=["Fuente", "result"]).set_index("Fuente")
    resource["data"] = file["result"].to_dict()
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


def load_excel(file_path):
    df = pd.read_excel(file_path, sheet_name="Recursos")
    columns_extracted = df.columns.to_list()
    if set(BIOMASS_COLUMNS).issubset(set(columns_extracted)):
        return process_biomass_data(df)
    else:
        raise ValueError("Invalid CSV file format")


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
