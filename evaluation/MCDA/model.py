"""Model file
This module include MCDA methods AHP and TOPSIS

Autor: Mateo Barrera
Date: 11-03-2023
"""
import numpy as np
import pandas as pd  # pylint: disable=import-error
import matplotlib.pyplot as plt
from .criteria import Criteria  # pylint: disable=import-error
from ..save import save

plt.style.use(['seaborn-v0_8-colorblind', 'evaluation/resource/graph.mplstyle'])
months_ticks_labels = pd.date_range('2014-01-01', '2014-12-31', freq='MS').strftime("%b").tolist()


def normalize_criteria(array: list, normalize_type: int):
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
        0: "./Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx",
        1: "./Repo/Articulo1/Test/test1.xlsx",
        2: "./Repo/Articulo1/Test/test2.xlsx",
        3: "./Repo/Articulo1/Test/test3.xlsx",
        4: "./Repo/Articulo1/Test/test4.xlsx",
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
        save_as=None,
        alt_info=None
):
    """
    The ahp function is the main function of this module. It takes in a matrix
    of alternatives and returns an evaluation of each alternative based on the
    criteria defined by experts. The criteria are stored in excel files, which
    are loaded from a folder called 'evaluation'. This function also allows to save
    the model used for evaluation as well as some information about it.

    :param alternative_matrix: Pass the matrix of alternatives
    :param show_criteria_matrix: Show the criteria matrix
    :param show_expert_matrix: Show the expert matrix in the console
    :param test: Load the criteria matrix from a test file
    :param fuzzy: Determine if the evaluation will be fuzzy or not
    :param save_as: Save the model in a file with the name specified
    :param alt_info: Show the alternatives in a more friendly way
    :return: A dictionary with the following keys:
    :doc-author: Trelent
    """
    print("\n:: AHP ::")
    ahp_criteria_obj = Criteria()
    ahp_criteria_obj.show_result_matrix = show_criteria_matrix
    ahp_criteria_obj.show_all = show_expert_matrix
    ahp_criteria_obj.fuzzy = fuzzy

    ahp_criteria_obj.from_excel(path=load_path_evaluation(test))

    ahp_criteria_aggregation = ahp_criteria_obj.get_weighting_array()
    alternative_matrix_norm = normalize_alternatives(alternative_matrix)
    alternative_array = alternative_matrix_norm.to_numpy()
    ahp_result = np.matmul(alternative_array, np.transpose(ahp_criteria_aggregation))
    ahp_result_df = pd.DataFrame({"Evaluation": ahp_result})
    show_evaluation(ahp_result_df, alternative_kw=alt_info)
    if save_as is not None:
        model = {
            "info": None,
            "alternative_info": alt_info,
            "alternatives_norm": alternative_matrix_norm,
            "criteria": pd.DataFrame(data=ahp_criteria_aggregation),
            "result": ahp_result_df.sort_values(by="Evaluation", ascending=False),
        }
        save(save_as, model, fuzzy=str(fuzzy), test=test)


def __topsis_normalize(alternatives):
    alternatives_norm = np.zeros(alternatives.shape)
    mean_array = np.sqrt(np.sum(alternatives ** 2, 1))
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
    # save_xls("TOP-Criteria N", alternatives)


def __topsis_ideal_solution(
        alternatives_array, type_indicator=(1, 0, 0, 0, 0, 0, 1, 1, 1)
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
        save_as=None,
        alt_info=None
):
    """
    The topsis function takes in a matrix of alternatives and criteria,
        normalizes the data, calculates the weighted sum for each alternative,
        finds the ideal positive and negative solutions (based on whether
        a criterion is beneficial or detrimental), calculates distance from these
        ideal solutions for each alternative, then returns an array of similarity
        indices.

    :param alternative_matrix: Pass the dataframe with the alternatives and their respective values
    :param show_criteria_matrix: Show the criteria matrix
    :param show_expert_matrix: Show the matrix of experts
    :param test: Select the data to be used in the evaluation
    :param fuzzy: Determine if the evaluation is fuzzy or not
    :param save_as: Save the model in a file called &quot;save&quot;
    :param alt_info: Save the information of the alternatives in a dataframe
    :return: A dataframe with the similarity index
    :doc-author: Trelent
    """
    print(alt_info)
    print("\n:: TOPSIS ::")
    topsis_criteria_obj = Criteria()
    topsis_criteria_obj.show_result_matrix = show_criteria_matrix
    topsis_criteria_obj.show_all = show_expert_matrix
    topsis_criteria_obj.fuzzy = fuzzy

    topsis_criteria_obj.from_excel(path=load_path_evaluation(test))
    topsis_criteria_aggregation = topsis_criteria_obj.get_weighting_array()
    print(topsis_criteria_aggregation)
    topsis_alternatives_array = __topsis_normalize(np.transpose(alternative_matrix.to_numpy()))
    topsis_alternatives_array = np.where(np.isnan(topsis_alternatives_array), 0, topsis_alternatives_array)
    topsis_alternatives_norm = __topsis_print_norm(topsis_alternatives_array, alternative_matrix)

    topsis_weighted_alternatives = topsis_alternatives_array * np.transpose([topsis_criteria_aggregation])

    ideal_positive, ideal_negative = __topsis_ideal_solution(topsis_weighted_alternatives)
    positive_distance, negative_distance, similarity_index = __topsis_distance(
        topsis_weighted_alternatives, ideal_positive, ideal_negative
    )
    topsis_result_df = pd.DataFrame({"Evaluation": similarity_index})
    show_evaluation(topsis_result_df, alternative_kw=alt_info)
    if save_as is not None:
        model = {
            "info": None,
            "alternative_info": alt_info,
            "alternatives_norm": topsis_alternatives_norm,
            "criteria": pd.DataFrame(data=topsis_criteria_aggregation),
            "result": topsis_result_df.sort_values(by="Evaluation", ascending=False),
        }
        save(save_as, model, fuzzy=str(fuzzy), test=test)


def show_evaluation(result_df, alternative_kw=None, graph=True):
    """
    The show_evaluation function is used to display the results of the evaluation process.
    It prints a table with all alternatives and their respective evaluations, and it also plots a bar graph showing how
    each alternative is composed in terms of resource participation.


    :param result_df: Store the results of the evaluation
    :param alternative_kw: Plot the graph
    :param graph: Show the graph of the alternatives
    :return: The ranking of alternatives
    :doc-author: Trelent
    """
    print("\n:: Ranking of alternatives ::")
    print(result_df.sort_values(by="Evaluation", ascending=False).to_markdown(
        floatfmt=".3f"
    ))

    if graph:
        alternative_kw = alternative_kw.filter(["solar", "wind", "hydro", "biomass"], axis=1)
        target_capacity = alternative_kw["solar"].max()
        def to_percentage(x): return (x / target_capacity) * 100

        alternative_kw = alternative_kw.apply(to_percentage, axis=1)
        result_df["Alternatives"] = ["$A_{"+'{:0>2}'.format(index)+"}$" for index in result_df.index.values]
        alternative_kw = alternative_kw.join(result_df)

        fig = plt.figure(layout="constrained")
        ax = fig.add_subplot()

        alternative_ordered = alternative_kw.sort_values(by="Evaluation", ascending=False).reset_index(drop=True)

        if alternative_ordered.shape[0] > 30:
            alternative_ordered = alternative_ordered.iloc[:20]

        alternative_ordered.plot.bar(stacked=True, ax=ax, y=["solar", "wind", "hydro", "biomass"], x="Alternatives",
                                     width=0.45, linewidth=0.5, edgecolor="black", legend=False)
        ax.set_xlabel("Alternative")
        ax.tick_params(axis='x', labelsize=14, rotation=45)
        ax.set_ylabel("Resource participation \%")
        ax_twin = ax.twinx()

        ax.legend(loc="lower left", bbox_to_anchor=(-0.12, -0.28), ncol=4, frameon=False)
        ax = alternative_ordered["Evaluation"].plot(ax=ax_twin, secondary_y=True, color="k", marker="D", linestyle='--',
                                                    label="$C_j$", legend=False)
        bottom, top = ax.get_ylim()
        ax.set_ylim([0, top*1.15])
        ax.legend(loc="lower left", bbox_to_anchor=(0.81, -0.29), ncol=1, frameon=False)
        ax.set_title("Evaluation result")
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=100, ha='right')

        plt.savefig("result.png", format="png", metadata=None,
                    bbox_inches=None, pad_inches=0.1)
        plt.show()

