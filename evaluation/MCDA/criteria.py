"""Criteria file

This module includes the loads data from an .xlsx file and allows expert evaluation reading.

Autor: Mateo Barrera
Date: 11-03-2023
"""
import numpy as np
import pandas as pd  # pylint: disable=import-error
from prettytable import PrettyTable  # pylint: disable=import-error
from statistics import geometric_mean
import matplotlib.pyplot as plt


def open_excel(path, sheet_name="Form Responses 1"):
    """_summary_

    Args:
        path (_type_): _description_
        sheet_name (str, optional): _description_. Defaults to "Form Responses 1".

    Returns:
        _type_: _description_
    """
    result = pd.read_excel(path, sheet_name=sheet_name)
    result = result.dropna(axis=1, how="all")
    return result


def print_table(title, series):
    """_summary_

    Args:
        title (_type_): _description_
        series (_type_): _description_
    """
    table = PrettyTable()
    table.title = title
    table.field_names = series.columns.tolist()
    for row in series.itertuples():
        table.add_row([row.Experto, np.around(row[2], decimals=4)])
    print(table)


def print_evaluation(name_matrix, matrix, wj_array, fuzzy=False):
    """_summary_

    Args:
        name_matrix (_type_): _description_
        matrix (_type_): _description_
        wj_array (_type_): _description_
    """
    table = PrettyTable()
    table.title = name_matrix
    consistency = "OK"
    if not fuzzy:
        matrix = np.round_(matrix, decimals=2)
        if wj_array.any() == None:
            consistency = "NO"
        else:
            wj_array = np.round_(wj_array, decimals=2)
    table.field_names = ["Matriz", "Consistencia", "Vector de pesos"]
    table.add_row([matrix, consistency, wj_array])
    print(table)


def graph_weighs(criteria):
    print(criteria)
    data = {'Ambiental': criteria['Ambiental'],
            'Económico': criteria['Económico'],
            'Técnico': criteria['Técnico'],
            }

    df = pd.DataFrame(data, columns=['Ambiental', 'Económico', 'Técnico'],
                      index=['Fluidez', '% Savings', 'Escalabilidad'])
    df_dummy = df.copy()
    df_dummy = df_dummy * 100
    percentage_values = [str(round(item, 1)) for item in df_dummy.values.flatten().tolist()]
    group_names = df.columns
    # group_size = [100 / len(group_names)] * len(group_names)
    group_size = criteria['weights']
    subgroup_names = ['C1.1.', 'C1.2.', 'C1.3.', 'C2.1.', 'C2.2.', 'C2.3.', 'C3.1.', 'C3.2.', 'C3.3.']

    # Make data: I have 4 groups and 12 subgroups - 3 for each group
    subgroup_size = []
    for group, size in zip(df.columns, group_size):
        subgroup_sum = df[group].sum()
        subgroup_size += [subgr / subgroup_sum * size for subgr in df[group]]
    # Create colors
    a, b, c, d = [plt.cm.Greens, plt.cm.Reds, plt.cm.Blues, plt.cm.Greys]
    subgroup_names = [x + '\n ' + y + '\%' for x, y in zip(subgroup_names, percentage_values)]
    group_size_str = [str(round(item * 100, 1)) for item in criteria['weights']]
    group_names = [x + '\n' + y + '\%' for x, y in zip(group_names, group_size_str)]
    # First Ring (outside)
    fig, ax = plt.subplots()
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.25 - 0.2, labels=group_names, labeldistance=0.38,
                      colors=[a(0.6), b(0.6), c(0.6), d(0.6)])
    plt.setp(mypie, width=0.8, edgecolor='white')

    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius=1.25, labels=subgroup_names, labeldistance=1.1,
                       colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), b(0.3), c(0.6), c(0.5), c(0.4), d(0.3),
                               d(0.2),
                               d(0.4)])
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0, 0)

    plt.show()


class Criteria:
    """This class criteria class allows the loading of peer evaluations generated by experts,
    constructing the matrix of weights per criterion used in the MCDA method.
    
    Include:
        Evaluation reading

        Consistency check

        Normalization

        Fuzzy number integration

        Weighted weights

        Visualization for evaluations
    """

    def __init__(self, fuzzy=False) -> None:
        """Constructor for a criteria object

        Args:
            fuzzy (bool, optional): initialization object with fuzzy components. Defaults to False.
        """
        self.__show = False
        self.__show_result_matrix = False
        self.matrix_criteria = None
        self.info_evaluation = None
        self.weight_criteria = dict()
        self.fuzzy_weight_criteria = dict()
        self.fuzzy_treatment = fuzzy

    @property
    def show_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__show

    @show_all.setter
    def show_all(self, value):
        """_summary_

        Args:
            value (_type_): _description_
        """
        if isinstance(value, bool):
            self.__show = value

    @property
    def show_result_matrix(self):
        return self.__show_result_matrix

    @show_result_matrix.setter
    def show_result_matrix(self, value):
        if isinstance(value, bool):
            self.__show_result_matrix = value

    @property
    def fuzzy(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.fuzzy_treatment

    @fuzzy.setter
    def fuzzy(self, value):
        """_summary_

        Args:
            value (_type_): _description_
        """
        if isinstance(value, bool):
            self.fuzzy_treatment = value

    # *To Check
    def get_weighting_array(self):
        """Returns an array with the weights for weighting each alternative

        Returns:
            np.array: 1xn array with weighting values
        """
        if self.fuzzy_treatment:
            criteria = self.fuzzy_weight_criteria
        else:
            criteria = self.weight_criteria
        weights = criteria["weights"]
        array_criteria = list()
        del criteria["weights"]
        for index, item in enumerate(criteria):
            array_criteria += list(weights[index] * np.array(criteria[item]))
        return np.array(array_criteria)

    def from_excel(self, path):
        """Extracts the pairwise comparison information contained in an Excel workbook
        in Google Forms results format.

        Args:
            path (str): relative path of the Excel file.
        """
        __file = open_excel(path=path)
        self.__expert_mail(__file)
        self.__criteria(__file)
        self.__subcriteria(__file)
        if self.__show_result_matrix:
            self.show_weighs()

    def show_weighs(self):
        """Returns dic with the expert aggregated weights in str format

        Returns:
            str: dic to print
        """
        if self.fuzzy_treatment:
            criteria = self.fuzzy_weight_criteria
        else:
            criteria = self.weight_criteria
        str_dic = pd.DataFrame(criteria).to_markdown(floatfmt=".4f")
        print("\n:: Criteria weights ::")
        print(str_dic)  # self.show_info()
        graph_weighs(criteria)

    def show_info(self):
        """_summary_"""
        print("\n:: Expert evaluations ::")
        series = {
            "Experto": self.info_evaluation.index,
            "[C1:Ambiental  C2:Económico C3:Técnico]": self.info_evaluation[
                "weights"
            ].tolist(),
        }

        df_2print = pd.DataFrame(series)
        print_table("Criterios", df_2print)
        series = {
            "Experto": self.info_evaluation.index,
            "[C1.1:Emisión  C1.2:Suelo C1.3:Impacto]": self.info_evaluation[
                "Ambiental"
            ].tolist(),
        }

        df_2print = pd.DataFrame(series)
        print_table("Subcriterios Ambientales", df_2print)
        series = {
            "Experto": self.info_evaluation.index,
            "[C2.1:LCOE     C2.2:CAPEX    C2.3:OPEX]": self.info_evaluation[
                "Económico"
            ].tolist(),
        }

        df_2print = pd.DataFrame(series)
        print_table("Subcriterios Económicos", df_2print)
        series = {
            "Experto": self.info_evaluation.index,
            "[C3.1:Eficiencia C3.2:Despachabilidad C3.3:Autonomía]": self.info_evaluation[
                "Técnico"
            ].tolist(),
        }

        df_2print = pd.DataFrame(series)
        print_table("Subcriterios Técnicos", df_2print)
        series = {
            "Experto": self.info_evaluation.index,
            "[CI Criterios]": self.info_evaluation["CI_weights"].tolist(),
        }

        df_2print = pd.DataFrame(series)
        print_table("Consistencia", df_2print)

    # *DONE: Remover wight_criteria
    def __expert_mail(self, df_experts):
        """_summary_

        Args:
            df_experts (_type_): _description_
        """
        self.info_evaluation = df_experts[df_experts.columns[-1:]]

    def __consistency_index(self, n_criteria, lmax):
        """_summary_

        Args:
            n_criteria (_type_): _description_
            lmax (_type_): _description_

        Returns:
            _type_: _description_
        """
        if n_criteria == 2:
            ci_index = 0
            cr_index = 0
        else:
            ri_array = {
                3: 0.5247,
                4: 0.8816,
                5: 1.1086,
                6: 1.2479,
                7: 1.3417,
                8: 1.4057,
                9: 1.4499,
                10: 1.4854,
            }
            ci_index = (lmax - n_criteria) / (n_criteria - 1)
            cr_index = ci_index / ri_array[n_criteria]
        return ci_index, cr_index

    def __consistency_check(self, matrix, name_matrix):
        """_summary_

        Args:
            matrix (_type_): _description_
            name_matrix (_type_): _description_

        Returns:
            _type_: _description_
        """
        sum_rows = np.sum(matrix, 0)
        normalized_matrix = matrix / sum_rows
        wj_array = np.mean(normalized_matrix, 1)

        criteria_sum = np.sum(matrix * wj_array, 1)
        dj_value = criteria_sum / wj_array
        lmax = np.mean(dj_value)

        ci_index, cr_index = self.__consistency_index(len(matrix), lmax)
        if cr_index > 0.10:
            wj_array = None
            matrix = None
        if self.__show:
            print_evaluation(name_matrix, matrix, wj_array)
        return wj_array, ci_index, matrix

    def __criteria_matriz_by_expert(self, df_file, name_matrix):
        """_summary_

        Args:
            df_file (_type_): _description_
            name_matrix (_type_): _description_

        Returns:
            _type_: _description_
        """
        """[ambiental económico técnico]"""

        def cx_extract(text):
            return (
                int(list(str(text).split()[0])[-2])
                if (str(text)[0] == "C")
                else int(str(text).split(".", maxsplit=1)[0])
            )

        df_file = df_file.apply(cx_extract)
        dim = list()
        value = list()
        for index, item in enumerate(df_file):
            if index % 2 == 0:
                dim.append(item)
            else:
                value.append(item)
                index += index
        size_matrix = int(len(df_file) / 2)
        matrix = np.ones([size_matrix, size_matrix])
        expected = [1, 1, 2]

        for row_index in range(size_matrix):
            for column_index in range(size_matrix):
                if row_index < column_index:
                    aux = row_index + column_index - 1
                    if dim[aux] == expected[aux]:
                        matrix[row_index, column_index] = float(value[aux])
                        matrix[column_index, row_index] = 1 / float(value[aux])
                    else:
                        matrix[row_index, column_index] = 1 / float(value[aux])
                        matrix[column_index, row_index] = float(value[aux])
        return self.__consistency_check(matrix, name_matrix)

    # *Done: weight_criteria solo queda como list_wc eliminar CI
    def __criteria(self, df_file):
        """_summary_

        Args:
            df_file (_type_): _description_
        """
        df_file = df_file[df_file.columns[1:7]]
        list_wc = list()
        list_matrix = list()
        list_ci = list()

        for evaluation in range(len(df_file)):
            name_matrix = f"Criterios experto {evaluation + 1}"
            weights, ci_index, matrix = self.__criteria_matriz_by_expert(
                df_file.iloc[evaluation], name_matrix=name_matrix
            )
            list_wc.append(weights)
            list_ci.append(ci_index)
            list_matrix.append(matrix)

        self.info_evaluation = self.info_evaluation.assign(
            weights=list_wc, CI_weights=list_ci
        )
        self.weight_criteria['weights'] = self.__aggregation(list_matrix)
        if self.fuzzy_treatment:
            result = self.__fuzzy_conversion(list_matrix)
            self.fuzzy_weight_criteria['weights'] = result

    def __subcriteria(self, df_file):
        """_summary_

        Args:
            df_file (_type_): _description_
        """
        df_file = df_file[df_file.columns[7:25]]
        list_wsubs = list()
        list_matrix_sub = list()

        wsubs_keys = [
            "Ambiental",
            "Económico",
            "Técnico",
            "CI_Ambiental",
            "CI_Económico",
            "CI_Técnico",
        ]
        for evaluation in range(len(df_file)):
            wsubs = {
                "Ambiental": None,
                "Económico": None,
                "Técnico": None,
                "CI_Ambiental": None,
                "CI_Económico": None,
                "CI_Técnico": None,
            }
            matrix_subs = {
                "Ambiental": None,
                "Económico": None,
                "Técnico": None,
            }

            df_subs = df_file.iloc[evaluation]
            i = 0
            for batch in range(0, len(df_subs), 6):
                name_matrix = f"Subcriterios {wsubs_keys[i]} - experto {evaluation + 1}"
                weights, ci_index, matrix = self.__criteria_matriz_by_expert(
                    df_subs.iloc[batch: batch + 6], name_matrix=name_matrix
                )
                wsubs[wsubs_keys[i]] = weights
                wsubs[wsubs_keys[i + 3]] = ci_index
                matrix_subs[wsubs_keys[i]] = matrix
                i += 1
            list_wsubs.append(wsubs)
            list_matrix_sub.append(matrix_subs)

        df_wsubs = pd.DataFrame.from_dict(list_wsubs)
        self.info_evaluation = pd.concat([self.info_evaluation, df_wsubs], axis=1)

        df_matrix_subs = pd.DataFrame.from_dict(list_matrix_sub)
        for column in df_matrix_subs:
            self.weight_criteria[column] = self.__aggregation(df_matrix_subs[column].to_list())

        if self.fuzzy_treatment:
            for column in df_matrix_subs:
                self.fuzzy_weight_criteria[column] = self.__fuzzy_conversion(df_matrix_subs[column].to_list())

    def __aggregation(self, df_file, method=0):
        df_file = np.array(df_file)
        if len(df_file) == 1:
            return self.__weights(df_file[0])

        if method != 0:
            return self.__weights_through_ci(df_file)

        rows, columns = df_file[0].shape
        agg_df_file = list()
        for row in range(rows):
            new_row = list()
            for column in range(columns):
                result = geometric_mean(df_file[:, row, column])
                new_row.append(result)
            agg_df_file.append(new_row)
        return self.__weights(agg_df_file)

    def __weights(self, matrix):
        sum_rows = np.sum(matrix, 0)
        normalized_matrix = matrix / sum_rows
        wj_array = np.mean(normalized_matrix, 1)
        return wj_array

    def __weights_through_ci(self, matrix):
        pass

    def __fuzzy_conversion(self, df_file):
        fuzzy_scale = {
            1: [1, 1, 1],
            3: [2, 3, 4],
            5: [4, 5, 6],
            7: [6, 7, 8],
            9: [8, 9, 10],
            1 / 3: [1 / 4, 1 / 3, 1 / 2],
            1 / 5: [1 / 6, 1 / 5, 1 / 4],
            1 / 7: [1 / 8, 1 / 7, 1 / 6],
            1 / 9: [1 / 10, 1 / 9, 1 / 8],
        }
        fuzzification = lambda x: fuzzy_scale[x]
        matrix_fuzzy = list()
        for index, item in enumerate(df_file):
            data_frame = pd.DataFrame(item)
            data_frame = data_frame.applymap(fuzzification)

            if False:
                print_evaluation(f"Evaluación (fuzzy) {index}", data_frame.to_numpy(), ["NA"], fuzzy=True)
            matrix_fuzzy.append(data_frame.to_numpy())
        defuzzy_weights = self.__fuzzy_aggregation(matrix_fuzzy)
        return defuzzy_weights

    def __fuzzy_aggregation(self, df_file):
        df_file = np.array(df_file)
        rows, columns = df_file[0].shape
        agg_df_file = list()
        # agg_defuzzy_df_file = list()
        for row in range(rows):
            new_row = list()
            # new_row_defuzzy = list()
            for column in range(columns):
                result = self.__fuzzy_mean_geometric([x for x in df_file[:, row, column]])
                # defuzzy_result = self.__defuzzification(result)
                new_row.append(result)
                # new_row_defuzzy.append(defuzzy_result)
            agg_df_file.append(new_row)
            # agg_defuzzy_df_file.append(new_row_defuzzy)
        return self.__fuzzy_weight(agg_df_file)

    def __fuzzy_mean_geometric(self, items):
        items = np.array(items)
        agg_items = np.ones(3)
        for index in range(3):
            agg_items[index] = geometric_mean(items[:, index])
        return agg_items

    def __fuzzy_weight(self, matrix_fuzzy):
        geo_mean_fuzzy = list()
        for row in matrix_fuzzy:
            geo_mean_fuzzy.append(self.__fuzzy_mean_geometric(row))
        fuzzy_weights = [element / sum(geo_mean_fuzzy) for element in geo_mean_fuzzy]
        return self.__defuzzification(fuzzy_weights)

    def __defuzzification(self, fuzzy_weights):
        """
        Methods

        Center of Sums (COS)
        Center of Gravity (COG)
        Centroid of Area (COA)
        Bisector of Area (BOA)
        Weighted Average
        Maxima

        """
        defuzzy_weights = fuzzy_weights
        for index, number_fuzzy in enumerate(fuzzy_weights):
            defuzzy_weights[index] = (number_fuzzy[0] + 4 * number_fuzzy[1] + number_fuzzy[2]) / 6
        return defuzzy_weights


if __name__ == "__main__":
    test_obj = Criteria()
    test_obj.show_all = True
    test_obj.fuzzy = True
    test_obj.from_excel(path="../../Repo/Articulo1/Encuesta/Resultados-9-02-2023.xlsx")
    # print(test_obj.get_weighting_array)
    # test_obj.from_excel(path="./Repo/Articulo1/Test/test2.xlsx")
    test_obj.show_weighs()

    ## new case
    {'weights': [0.4327147065974068, 0.15410955720571176, 0.4131757361968815],
     'Ambiental': [0.6405797246488998, 0.18386737702830666, 0.17555289832279353],
     'Económico': [0.5759505100494177, 0.1884448752001129, 0.23560461475046943],
     'Técnico': [0.2616101934821296, 0.1277811007366131, 0.6106087057812574],
     'Social': [0.2616101934821296, 0.1277811007366131, 0.6106087057812574]}
