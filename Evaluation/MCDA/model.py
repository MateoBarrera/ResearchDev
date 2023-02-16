"""_summary_

Returns:
    _type_: _description_
"""
from statistics import geometric_mean
import numpy as np
from criteria import Criteria  # pylint: disable=import-error

from prettytable import PrettyTable  # pylint: disable=import-error


def normalice_criteria(array: list, normalice_type: str):
    """Normaliza el arreglo recibido teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        normalice_type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar)

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if normalice_type == 0:
        min_array = min(array) / array
        return list(min_array / sum(min_array))
    elif normalice_type == 1:
        max_array = array / max(array)
        return list(max_array / sum(max_array))


def normalice(array: list, normalice_type: str):
    """Normaliza el arreglo recibido teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        normalice_type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar)

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if normalice_type == 0:
        min_array = [(x - min(array)) / (max(array) - min(array)) for x in array]
        return list(min_array / sum(min_array))
    elif normalice_type == 1:
        max_array = [(max(array) - x) / (max(array) - min(array)) for x in array]
        return list(max_array / sum(max_array))


def criteria_aggregation(df_citeria, method=0):
    """_summary_

    Args:
        df_citeria (_type_): _description_
        method (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    geo_mean = ["geometric_mean", 0, "geo"]
    columns = df_citeria.columns.tolist()
    criteria_agg = dict()
    columns.pop(0)
    columns.pop(1)
    columns.pop()
    columns.pop()
    columns.pop()
    if method in geo_mean:
        for column in columns:
            aux_0, aux_1, aux_2 = list(), list(), list()
            values = df_citeria[column].tolist()
            for value in values:
                aux_0.append(value[0])
                aux_1.append(value[1])
                aux_2.append(value[2])
            criteria_agg[column] = [
                geometric_mean(aux_0),
                geometric_mean(aux_1),
                geometric_mean(aux_2),
            ]
    else:
        for column in columns:
            aux_0, aux_1, aux_2 = list(), list(), list()
            values = df_citeria[column].tolist()
            ci_index = df_citeria["CI_" + column].tolist()
            ci_index = [x if x != 0 else 1e-3 for x in ci_index]
            ci_norm = normalice_criteria(ci_index, normalice_type=0)
            i = 0
            for value in values:
                aux_0.append(value[0] * ci_norm[i])
                aux_1.append(value[1] * ci_norm[i])
                aux_2.append(value[2] * ci_norm[i])
                i += 1
            criteria_agg[column] = [sum(aux_0), sum(aux_1), sum(aux_2)]
    return criteria_agg


if __name__ == "__main__":
    test_obj = Criteria()
    test_obj.show_all = False
    test_obj.from_excel(path="../Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx")
    result = criteria_aggregation(test_obj.weight_criteria, method=0)
    table = PrettyTable()
    table.title = "Resultado pesos agregados - media geométrica"
    table.field_names = ["Criterio(s)", "Vector de pesos"]
    for key in result.items():
        table.add_row([key[0], key[1]])
    print(table)

    result = criteria_aggregation(test_obj.weight_criteria, method=1)
    table = PrettyTable()
    table.title = "Resultado pesos agregados - ponderación por criterios"
    table.field_names = ["Criterio(s)", "Vector de pesos"]
    for key in result.items():
        table.add_row([key[0], key[1]])
    print(table)
    # test_obj.show_info()
