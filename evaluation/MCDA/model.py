"""Model file

This module include MCDA methods AHP and TOPSIS

Autor: Mateo Barrera
Date: 11-03-2023
"""
from datetime import datetime
import numpy as np
import pandas as pd  # pylint: disable=import-error
from .criteria import Criteria  # pylint: disable=import-error
from ..save import save_model

from prettytable import PrettyTable  # pylint: disable=import-error


def normalize_criteria(array: list, normalize_type: str):
    """Normaliza el arreglo recibido teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        normalize_type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar)

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if sum(array) == 0:
        return list(array)
    if normalize_type == 0:
        min_array = min(array) / array
        return list(min_array / sum(min_array))
    elif normalize_type == 1:
        max_array = array / max(array)
        return list(max_array / sum(max_array))


def load_path_evaluation(test=0):
    dict_paths = {
        0 : "./Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx",
        1 : "./Repo/Articulo1/Test/test1.xlsx",
        2 : "./Repo/Articulo1/Test/test2.xlsx",
        3 : "./Repo/Articulo1/Test/test3.xlsx",
        4 : "./Repo/Articulo1/Test/test4.xlsx",
    }
    return dict_paths[test]

def normalize_alternatives(alternative_matrix):
    type_indicator = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    for column in alternative_matrix:
        alternative_matrix[column] = normalize_criteria(
            alternative_matrix[column], normalize_type=type_indicator[0]
        )
        type_indicator.pop(0)
    print("\n:: Criteria Normalized  ::")
    print(alternative_matrix.to_markdown(floatfmt=".4f"))
    return alternative_matrix

def ahp(
    alternative_matrix,
    show_criteria_matrix=False,
    show_expert_matrix=False,
    test=False,
    fuzzy=False,
    save=None,
    alt_info=None
):
    """_summary_

    Args:
        alternative_matrix (_type_): _description_
        show_criteria_matrix (bool, optional): _description_. Defaults to False.
        show_expert_matrix (bool, optional): _description_. Defaults to False.
    """
    print("\n:: AHP ::")
    criteria_obj = Criteria()
    criteria_obj.show_result_matrix = show_criteria_matrix
    criteria_obj.show_all = show_expert_matrix
    criteria_obj.fuzzy = fuzzy

    criteria_obj.from_excel(path=load_path_evaluation(test))

    criteria_aggregation = criteria_obj.get_weighting_array()
    alternative_matrix_norm = normalize_alternatives(alternative_matrix)
    alternative_array = alternative_matrix_norm.to_numpy()
    result = np.matmul(alternative_array, np.transpose(criteria_aggregation))
    result_df = pd.DataFrame({"Evaluation": result})
    show_evaluation(result_df)
    if save is not None:
        info = {
            "name": save,
            "date": datetime.now().strftime("%D"),
            "fuzzy": str(fuzzy),
            "test_data": f" {test} // 0 - expertos; 1 - Igual importancia; 2 - Enfoque Ambiental; 3 - Enfoque Económico; 4 - Enfoque Técnico"
        }

        model = {
            "info": pd.DataFrame(info, index=[0]),
            "alternative_info":alt_info,
            "alternatives_norm": alternative_matrix_norm,            
            "criteria":pd.DataFrame(data=criteria_aggregation),
            "result": result_df.sort_values(by="Evaluation", ascending=False),
        }

        save_model(save, model)


def __topsis_normalize(alternatives):
    alternatives_norm = np.zeros(alternatives.shape)
    mean_array = np.sqrt(np.sum(alternatives**2, 1))
    np.seterr(all="ignore")
    alternatives_norm = alternatives / np.transpose([mean_array])
    np.seterr()
    return alternatives_norm


def __topsis_print_norm(alternatives, info):
    alternatives = pd.DataFrame(
        data=np.transpose(alternatives), columns=list(info.columns)
    )
    print("\n:: Criteria Normalized  ::")
    print(alternatives.to_markdown(floatfmt=".4f"))
    return alternatives
    #save_xls("TOP-Criteria N", alternatives)


def __topsis_ideal_solution(
    alternatives_array, type_indicator=[1, 0, 0, 0, 0, 0, 1, 1, 1]
):
    ideal_positive = np.zeros(len(type_indicator))
    ideal_negative = np.zeros(len(type_indicator))

    for i in range(len(type_indicator)):
        if type_indicator[i] == 0:  # Criterio de costo
            ideal_positive[i] = np.min(alternatives_array[i, :])
            ideal_negative[i] = np.max(alternatives_array[i, :])
        elif type_indicator[i] == 1:  # Criterio de beneficio
            ideal_positive[i] = np.max(alternatives_array[i, :])
            ideal_negative[i] = np.min(alternatives_array[i, :])

    return ideal_positive, ideal_negative


def __topsis_distance(alternatives_array, ideal_positive, ideal_negative):
    positive_distance = np.sqrt(
        np.sum((alternatives_array - np.transpose([ideal_positive])) ** 2, 0)
    )
    negative_distance = np.sqrt(
        np.sum((alternatives_array - np.transpose([ideal_negative])) ** 2, 0)
    )

    similarity_index = negative_distance / (positive_distance + negative_distance)

    return positive_distance, negative_distance, similarity_index


def topsis(
    alternative_matrix,
    show_criteria_matrix=False,
    show_expert_matrix=False,
    test=False,
    fuzzy=False,
    save=None,
    alt_info=None
):
    """_summary_

    Args:
        alternative_matrix (_type_): _description_
        show_criteria_matrix (bool, optional): _description_. Defaults to False.
        show_expert_matrix (bool, optional): _description_. Defaults to False.
        test (bool, optional): _description_. Defaults to False.
    """
    print("\n:: TOPSIS ::")
    criteria_obj = Criteria()
    criteria_obj.show_result_matrix = show_criteria_matrix
    criteria_obj.show_all = show_expert_matrix
    criteria_obj.fuzzy = fuzzy

    criteria_obj.from_excel(path=load_path_evaluation(test))
    criteria_aggregation = criteria_obj.get_weighting_array()
    print("SHSISHHSHSHHSHSHHS")
    print(criteria_aggregation)
    alternatives_array = __topsis_normalize(np.transpose(alternative_matrix.to_numpy()))
    alternatives_array = np.where(np.isnan(alternatives_array), 0, alternatives_array)
    alternatives_norm = __topsis_print_norm(alternatives_array, alternative_matrix)

    weighted_alternatives = alternatives_array * np.transpose([criteria_aggregation])

    ideal_positive, ideal_negative = __topsis_ideal_solution(weighted_alternatives)
    positive_distance, negative_distance, similarity_index = __topsis_distance(
        weighted_alternatives, ideal_positive, ideal_negative
    )
    result_df = pd.DataFrame({"Evaluation": similarity_index})
    #save_xls("TOP-Ranking", result_df.sort_values(by="Evaluation", ascending=False))
    show_evaluation(result_df)
    if save is not None:
        info = {
            "name": save,
            "date": datetime.now().strftime("%D"),
            "fuzzy": str(fuzzy),
            "test_data": f" {test} // 0 - expertos; 1 - Igual importancia; 2 - Enfoque Ambiental; 3 - Enfoque Económico; 4 - Enfoque Técnico"
        }
        
        model = {
            "info": pd.DataFrame(info, index=[0]),
            "alternative_info":alt_info,
            "alternatives_norm": alternatives_norm,            
            "criteria":pd.DataFrame(data=criteria_aggregation),
            "result": result_df.sort_values(by="Evaluation", ascending=False),
        }

        save_model(save, model)


def show_evaluation(result_df):
    print("\n:: Ranking of alternatives ::")
    print(
        result_df.sort_values(by="Evaluation", ascending=False).to_markdown(
            floatfmt=".3f"
        )
    )

