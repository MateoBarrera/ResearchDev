"""Save file

This module include the methods for saving the results of the evaluation models

Autor: Mateo Barrera
Date: 13-03-2023
"""
import pandas as pd
from datetime import datetime

def save_model(name, info):
    print(name)
    info["info"].to_excel(f"./Repo/Articulo1/output/{name}.xlsx",  sheet_name="info")
    info.pop("info", None)
    for element in info:
        save_xlsx(name_file=name, element_name=element, element=info[element])
    pass

def save_xlsx(name_file, element_name, element):
    with pd.ExcelWriter(f"./Repo/Articulo1/output/{name_file}.xlsx", mode="a") as writer:
        element.to_excel(writer, sheet_name=element_name)