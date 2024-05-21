"""Save file

This module include the methods for saving the results of the evaluation models

Autor: Mateo Barrera
Date: 13-03-2023
"""
import pandas as pd
from datetime import datetime


def save(save_as, model, fuzzy=None, test=None):
    info = {
        "name": save_as,
        "date": datetime.now().strftime("%D"),
        "fuzzy": str(fuzzy),
        "test_data": f" {test} // 0 - expertos; 1 - Igual importancia; 2 - Enfoque Ambiental; 3 - Enfoque "
                     f"Económico; 4 - Enfoque Técnico"
    }
    model["info"] = pd.DataFrame(info, index=[0])
    save_model(save_as, model=model)
    pass


def save_model(name, model):
    model["info"].to_excel(f"./Repo/Articulo1/output/{name}.xlsx",  sheet_name="info")
    model.pop("info", None)
    for element in model:
        save_xlsx(name_file=name, element_name=element, element=model[element])
    pass


def save_xlsx(name_file, element_name, element):
    with pd.ExcelWriter(f"./Repo/Articulo1/output/{name_file}.xlsx", mode="a") as writer:
        element.to_excel(writer, sheet_name=element_name)