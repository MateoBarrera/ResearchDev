"""_summary_

Returns:
    _type_: _description_
"""
from datetime import datetime
from locale import normalize
from statistics import geometric_mean
import numpy as np
import pandas as pd  # pylint: disable=import-error
from .criteria import Criteria  # pylint: disable=import-error

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


def normalize(array: list, normalize_type: str):
    """Normaliza el arreglo recibido teniendo en cuenta su característica de tipo costo o beneficio.

    Args:
        array (list): arreglo que se desea normalizar.
        normalize_type (str): tipo de criterio: 0 -> Costo (Minimizar); 1 -> Beneficio (Maximizar)

    Returns:
        list: arreglo normalizado
    """
    array = np.array(array)
    if normalize_type == 0:
        min_array = [(x - min(array)) / (max(array) - min(array)) for x in array]
        return list(min_array / sum(min_array))
    elif normalize_type == 1:
        max_array = [(max(array) - x) / (max(array) - min(array)) for x in array]
        return list(max_array / sum(max_array))


def criteria_aggregation(df_criteria, method):
    """_summary_

    Args:
        df_criteria (_type_): _description_
        method (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    geo_mean = ["geometric_mean", 0, "geo"]
    columns = df_criteria.columns.tolist()
    criteria_agg = dict()
    columns.pop(0)
    columns.pop(1)
    columns.pop()
    columns.pop()
    columns.pop()
    if method in geo_mean:
        method_str = "Resultado pesos agregados - media geométrica"
        for column in columns:
            aux_0, aux_1, aux_2 = list(), list(), list()
            values = df_criteria[column].tolist()
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
        method_str = "Resultado pesos agregados - ponderación por criterios"
        for column in columns:
            aux_0, aux_1, aux_2 = list(), list(), list()
            values = df_criteria[column].tolist()
            ci_index = df_criteria["CI_" + column].tolist()
            # ci_index = [x if x != 0 else 1e-5 for x in ci_index]
            ci_norm = normalize(ci_index, normalize_type=0)
            i = 0
            for value in values:
                aux_0.append(value[0] * ci_norm[i])
                aux_1.append(value[1] * ci_norm[i])
                aux_2.append(value[2] * ci_norm[i])
                i += 1
            criteria_agg[column] = [sum(aux_0), sum(aux_1), sum(aux_2)]
    return criteria_agg, method_str


def load_criteria_weight(
    show_criteria_matrix, show_expert_matrix, method_aggregation=0, test=0
):
    test_obj = Criteria()
    test_obj.show_all = show_expert_matrix
    if test == 1:
        test_obj.from_excel(path="../Repo/Articulo1/Test/test1.xlsx")
    elif test == 2:
        test_obj.from_excel(path="../Repo/Articulo1/Test/test2.xlsx")
    elif test == 3:
        test_obj.from_excel(path="../Repo/Articulo1/Test/test3.xlsx")
    elif test == 4:
        test_obj.from_excel(path="../Repo/Articulo1/Test/test4.xlsx")
    else:
        test_obj.from_excel(path="../Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx")
    result, method_str = criteria_aggregation(
        test_obj.weight_criteria, method=method_aggregation
    )

    if show_criteria_matrix:
        table = PrettyTable()
        table.title = method_str
        table.field_names = ["Criterio(s)", "Vector de pesos"]
        for key in result.items():
            table.add_row([key[0], key[1]])
        print(table)
    return result


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


def weighting_subcriteria(criteria: dict):
    weights = criteria["weights"]
    array_criteria = list()
    del criteria["weights"]
    for index, item in enumerate(criteria):
        array_criteria += list(weights[index] * np.array(criteria[item]))
    return np.array(array_criteria)


def ahp(
    alternative_matrix,
    show_criteria_matrix=False,
    show_expert_matrix=False,
    method_aggregation=0,
    test=False,
):
    """_summary_

    Args:
        alternative_matrix (_type_): _description_
        show_criteria_matrix (bool, optional): _description_. Defaults to False.
        show_expert_matrix (bool, optional): _description_. Defaults to False.
    """
    print("\n:: AHP ::")
    criteria_aggregation = load_criteria_weight(
        show_criteria_matrix,
        show_expert_matrix,
        method_aggregation=method_aggregation,
        test=test,
    )
    #save_xls("Criteria", pd.DataFrame(criteria_aggregation))
    criteria_aggregation = weighting_subcriteria(criteria_aggregation)
    #save_xls("Criteria N", pd.DataFrame(criteria_aggregation))
    #save_xls("Alternatives", alternative_matrix)
    alternative_matrix_norm = normalize_alternatives(alternative_matrix)
    #save_xls("AHP-Criteria N", alternative_matrix_norm)
    alternative_array = alternative_matrix_norm.to_numpy()
    result = np.matmul(alternative_array, np.transpose(criteria_aggregation))
    result_df = pd.DataFrame({"Evaluation": result})
    #save_xls("AHP-Ranking", result_df.sort_values(by="Evaluation", ascending=False))
    show_evaluation(result_df)


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
    method_aggregation=0,
    test=False,
):
    """_summary_

    Args:
        alternative_matrix (_type_): _description_
        show_criteria_matrix (bool, optional): _description_. Defaults to False.
        show_expert_matrix (bool, optional): _description_. Defaults to False.
        test (bool, optional): _description_. Defaults to False.
    """
    print("\n:: TOPSIS ::")
    criteria_aggregation = load_criteria_weight(
        show_criteria_matrix,
        show_expert_matrix,
        method_aggregation=method_aggregation,
        test=test,
    )
    criteria_aggregation = weighting_subcriteria(criteria_aggregation)

    alternatives_array = __topsis_normalize(np.transpose(alternative_matrix.to_numpy()))
    alternatives_array = np.where(np.isnan(alternatives_array), 0, alternatives_array)
    __topsis_print_norm(alternatives_array, alternative_matrix)

    weighted_alternatives = alternatives_array * np.transpose([criteria_aggregation])

    ideal_positive, ideal_negative = __topsis_ideal_solution(weighted_alternatives)
    positive_distance, negative_distance, similarity_index = __topsis_distance(
        weighted_alternatives, ideal_positive, ideal_negative
    )
    result_df = pd.DataFrame({"Evaluation": similarity_index})
    #save_xls("TOP-Ranking", result_df.sort_values(by="Evaluation", ascending=False))
    show_evaluation(result_df)


def show_evaluation(result_df):
    print("\n:: Ranking of alternatives ::")
    print(
        result_df.sort_values(by="Evaluation", ascending=False).to_markdown(
            floatfmt=".3f"
        )
    )


def save_xls(df_name, dframe: pd.DataFrame):
    pass
    time = datetime.now().strftime("%H.%M")
    with pd.ExcelWriter("../Repo/Articulo1/output/result.xlsx", mode="a") as writer:
        dframe.to_excel(writer, sheet_name=df_name +"-"+ str(time))


if __name__ == "__main__":
    """test_obj = Criteria()
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
    print(table)"""
    # test_obj.show_info()
    ahp()
