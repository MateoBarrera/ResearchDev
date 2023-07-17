import math
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt  # pylint: disable=import-error
import numpy as np
import seaborn as sns  # pylint: disable=import-error
import squarify

plt.style.use(['seaborn-v0_8-colorblind', 'evaluation/resource/graph.mplstyle'])
# plt.style.use(['seaborn-v0_8-colorblind', '../graph.mplstyle'])
months_ticks_labels = pd.date_range('2014-01-01', '2014-12-31', freq='MS').strftime("%b").tolist()

# Local Method #
"""
* Importante
! deprecated
TODO: por hacer
@param Parámetro

"""


def get_data_month(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    data_month = df.set_index("Fecha")
    data_month = data_month.asfreq("M", method="ffill")
    data_month["Año"] = data_month.index.year
    data_month["Mes"] = pd.to_datetime(data_month.index.month, format="%m")

    data_month_piv = pd.pivot_table(
        data_month, index=["Mes"], columns=["Año"], values=["Valor"]
    )
    data_month_piv["mean"] = data_month_piv.mean(axis=1)
    data_month_piv.sort_index()
    return data_month, data_month_piv


def calculate_autonomy(df, minimum_required):
    autonomy = 0
    month_mean = df["mean"].to_list()
    for month_item in month_mean:
        if month_item > minimum_required:
            autonomy += 1
    return autonomy / 12


def calculate_variability(df):
    def cv(x):
        return np.std(x, ddof=1) / np.mean(x) * 100

    return df.apply(cv).mean()


def graph_raw_data_resource(resource: str, dataframe, y_axis=None, label="None"):
    fig = plt.figure()
    ax = fig.add_subplot()
    dataframe.plot(kind="line", x="Fecha", y="Valor", ax=ax, label=label)
    ax.hlines(
        y=dataframe["Valor"].mean(),
        xmin=dataframe["Fecha"].min(),
        xmax=dataframe["Fecha"].max(),
        colors="black",
        linestyles="--",
        label=label + "$_{avg}$" + " = {:.2f} ".format(dataframe["Valor"].mean()) + y_axis,
    )
    ax.set_title(resource)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_axis)
    ax.legend(loc="upper right")


def graph_variability_resource(ax, dataframe, title="None", y_label="None", label="None",
                               min_viability=0, viability_label="None"):
    dataframe["mean"] = dataframe.mean(axis=1)
    dataframe["std"] = dataframe.std(axis=1)
    dataframe.plot(kind="line", y="mean", label=label, ax=ax, style="--k")
    ax.fill_between(
        dataframe.index,
        dataframe["mean"] - dataframe["std"],
        dataframe["mean"] + dataframe["std"],
        alpha=0.15,
    )
    ax.hlines(
        y=min_viability,
        xmin=dataframe.index.min(),
        xmax=dataframe.index.max(),
        colors="red",
        linestyles="--",
        label=viability_label + " = {:.2f} ".format(min_viability) + y_label,
    )
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    ax.legend(loc="upper right")
    dataframe.plot(kind="line", ax=ax, alpha=0.15, legend=None)
    ax.xaxis.set_ticks(list(ax.get_xticks()) + list(ax.get_xticks(minor=True)))
    ax.set_xticklabels(months_ticks_labels)


def grap_boxplot_resource(ax, dataframe, title="None", y_label="None"):
    dataframe["Mes"] = pd.to_datetime(
        dataframe.index.month, format="%m"
    ).month_name()

    # Boxplot chart
    hydro_boxplot = sns.boxplot(data=dataframe, x="Mes", y="Valor", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    plt.subplots_adjust(hspace=0.5, bottom=0.1)
    hydro_boxplot.set_xticklabels(months_ticks_labels)


class Hydro:
    """Analysis of water resource through the flow permanence curve, resource variability and calculation of \
    autonomy from historical monthly average flow data.

    Returns:
        Object: Hydro object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data) -> None:
        self.data_month_piv = None
        self.data_month = None
        self.q_mean = None
        self.q_sr = None
        self.q_sr_index = None
        self.data = data
        self.q_data = pd.DataFrame(data)["Valor"].to_list()
        self.raw = False
        self.qd = None
        self.calculate_autonomy()

    def calculate_autonomy(self):
        # Q parameters calculation
        q_data_sort = np.sort(self.q_data)[::-1]
        self.q_sr_index = int(len(q_data_sort) * 0.7)
        self.q_sr = q_data_sort[self.q_sr_index]
        # q_max = q_data_sort[int(len(q_data_sort)*0.024)]
        self.q_mean = q_data_sort[int(len(q_data_sort) * 0.5)]

        # Prepare data
        self.data_month, self.data_month_piv = get_data_month(self.data)
        self.__variability = calculate_variability(self.data_month_piv)
        self.__autonomy = calculate_autonomy(self.data_month_piv, self.q_sr)

    def potential(self, show, installed_capacity=1000):
        # Parameters #
        pt = 100
        e = 0.9  # Turbine efficiency
        n = 0.85  # Accessories efficiency
        h = 2  # Height
        operation_regime = 8
        # End Parameters #
        nt = math.ceil(installed_capacity / pt)
        df = pd.DataFrame(index=self.data_month_piv.index)

        df["Q"] = self.data_month_piv["mean"]
        df["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        qd = 3

        def qd_calc(x):
            return qd if (x["Q"] - self.q_sr) > qd else x["Q"] - self.q_sr

        df["Qd"] = df.apply(qd_calc, axis=1)
        df[df["Qd"] < 0] = 0
        df.set_index = df.index.month

        def power_gen(x):
            return (nt * (0.98 / 1.3) * 9.81 * (x["Qd"]) * h * e * n * operation_regime * x["days"]) \
                if x["Qd"] > 0 else 0

        # qd_mean = df["Qd"].mean()
        df["monthly energy"] = df.apply(power_gen, axis=1)

        def correction(x):
            return (
                nt * x["monthly energy"] * (0.98 / 1.3)
                if (x["monthly energy"] > installed_capacity * e * n * operation_regime * x["days"])
                else x["monthly energy"]
            )

        # df["monthly energy"] = df.apply(correction, axis=1)
        power_generation = np.sum(df["monthly energy"].tolist()) / 365
        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        if show:
            capacity_factor = power_generation / (9.81 * 7 * h * e * n * 24)
            print("\n:: Hydro ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation

    def flow_permanence_curve(self) -> object:
        """Evaluate the resource with the flow duration curve graph for the given data.

        Returns:
            object: matplotlib.pyplot.figure corresponding to the flow  permanent graph
        """
        q_data_sort = np.sort(self.q_data)[::-1]
        q_frequency = (np.arange(1.0, len(q_data_sort) + 1) / len(q_data_sort)) * 100
        # Plot figure
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(q_frequency, q_data_sort)
        ax.fill_between(
            q_frequency[0: self.q_sr_index],
            q_data_sort[0: self.q_sr_index],
            self.q_sr,
            alpha=0.2,
            color="b",
        )
        ax.fill_between(
            q_frequency[self.q_sr_index:],
            q_data_sort[self.q_sr_index:],
            self.q_sr,
            alpha=0.2,
            color="r",
        )
        ax.hlines(
            y=self.q_sr,
            xmin=q_frequency[0],
            xmax=q_frequency[-1],
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f} $m^3/s$".format(self.q_sr),
        )
        ax.set_xlabel("Percentage of occurrence \%")
        ax.set_ylabel("Flow rate $m^3/s$")
        ax.set_title("Flow permanence curve")
        ax.legend(loc="upper right")
        return fig

    def graph_variability(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
        graph_variability_resource(ax1, dataframe=self.data_month_piv, title="Monthly Average Flow Rate",
                                   y_label="$m^3/s$", label="$Q_{avg}$", min_viability=self.q_sr,
                                   viability_label="$Q_{sr}$")

        grap_boxplot_resource(ax2, dataframe=self.data_month, title="Monthly Average Flow Rate", y_label="$m^3/s$")
        return fig

    def graph_pdc(self):
        y = 1000  #
        h = 2
        n = 0.85
        df = pd.DataFrame(index=self.data_month_piv.index)
        df["q"] = self.data_month_piv["mean"] - self.q_sr
        df[df < 0] = 0
        df["potencial"] = y * df["q"] * h * n / 1000

        q_data_sort = np.sort(self.q_data)[::-1]

        q_frequency = (np.arange(1.0, len(q_data_sort) + 1) / len(q_data_sort)) * 100
        q_data_p = q_frequency * q_data_sort * y * h * n / 1000
        # print(q_data_p)
        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot raw data
        ax1.plot(q_frequency, q_data_sort)

        ax1.fill_between(
            q_frequency[0: self.q_sr_index],
            q_data_sort[0: self.q_sr_index],
            self.q_sr,
            alpha=0.2,
            color="b",
        )
        ax1.fill_between(
            q_frequency[self.q_sr_index:],
            q_data_sort[self.q_sr_index:],
            self.q_sr,
            alpha=0.2,
            color="r",
        )
        ax1.hlines(
            y=self.q_sr,
            xmin=q_frequency[0],
            xmax=q_frequency[-1],
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f}".format(self.q_sr),
        )
        ax1.set_xlabel("Percentage of occurrence [%]")
        ax1.set_ylabel("Flow rate [m^3/s]")
        ax1.set_title("Flow permanence curve")
        ax1.legend(loc="upper right")
        plt.subplots_adjust(hspace=0.3, bottom=0.1)

        # Flow permanence curve
        # q_sort = np.sort(df["q"])[::-1]
        # q_power_sort = np.sort(df["potencial"])[::-1]
        ax2.plot(q_data_sort, q_data_p)

        """ ax2.fill_between(q_frequency[0:self.q_sr_index],
                         q_data_sort[0:self.q_sr_index], self.q_sr, alpha=0.2, color='b')
        ax2.fill_between(q_frequency[self.q_sr_index:],
                         q_data_sort[self.q_sr_index:], self.q_sr, alpha=0.2, color='r') """
        ax2.vlines(
            x=self.q_sr,
            ymin=0,
            ymax=max(q_data_p),
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f}".format(self.q_sr),
        )
        ax2.vlines(
            x=self.q_mean,
            ymin=0,
            ymax=max(q_data_p),
            colors="grey",
            linestyles="--",
            label="Average Q = {:.2f}".format(self.q_mean),
        )
        ax2.set_xlabel("Flow rate [m^3/s]")
        ax2.set_ylabel("Power generation [Wh]")
        ax2.set_title("Power duration curve")
        ax2.legend(loc="upper right")
        plt.subplots_adjust(hspace=0.3, bottom=0.1)
        plt.show()
        # return fig

    @property
    def viability_graph(self):
        return self.flow_permanence_curve()

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability resource: {:.2f}% ::".format(self.__variability)

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def autonomy(self):
        print("Months higher than the ecological flow.")
        return ":: Autonomy resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def all_graph(self):
        if self.raw:
            graph_raw_data_resource("Average Monthly Flow Rate", self.data, "$m^3/s$", "Q")
        self.flow_permanence_curve()
        self.graph_variability()
        return


class Pv:
    """Analysis of the solar resource through the Peak Sun Hours, resource variability and calculation of autonomy
    from historical monthly average flow data.

    Returns:
        Object: Pv object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data, min_irr_pv) -> None:
        self.data_month_piv = None
        self.data_month = None
        self.irr_mean_month = None
        self.irr_mean = None
        self.data = data
        self.min_irr_pv = min_irr_pv
        self.raw = False
        self.calculate_autonomy()

    def calculate_autonomy(self):
        self.irr_mean_month = self.data.groupby(
            pd.PeriodIndex(self.data["Fecha"], freq="M")
        )["Valor"].mean()
        self.irr_mean_month.sort_index()
        self.data_month, self.data_month_piv = get_data_month(self.data)
        self.__variability = calculate_variability(self.data_month_piv)
        self.__autonomy = calculate_autonomy(self.data_month_piv, self.min_irr_pv)

    def potential(self, show, installed_capacity=1000):
        # pp = 0.200  # Peak power of the panel [kW year]
        n = 0.90  # Typical conditions
        df = pd.DataFrame(index=self.data_month_piv.index)
        df["PSH"] = self.data_month_piv["mean"]
        df["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        def nt_calc(x):
            return x["PSH"] * installed_capacity * n * x["days"]

        df["monthly energy"] = df.apply(nt_calc, axis=1)

        power_generation = np.mean(df["PSH"].tolist()) * installed_capacity * n
        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        if show:
            capacity_factor = power_generation / (installed_capacity * 24)
            print("\n:: Solar ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation

    def psh_graph(self):
        """Evaluate the resource with the flow duration curve graph for the given data.

        Returns:
            object: matplotlib.pyplot.figure corresponding to the flow  permanent graph
        """
        # Plot figure
        fig = plt.figure()
        ax = fig.add_subplot()
        # Plot month data
        self.irr_mean_month.plot(kind="line", x="Fecha", y="Valor", ax=ax, label="$PSH$")

        self.irr_mean = self.data["Valor"].mean()
        ax.hlines(
            y=self.irr_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="$PSH_{avg}$" + " = {:.2f} $h$".format(self.irr_mean),
        )
        ax.hlines(
            y=self.min_irr_pv,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="red",
            linestyles="--",
            label="$PSH_{min}$" + "= {:.2f} $h$".format(self.min_irr_pv),
        )
        ax.set_title("Monthly Average PSH")
        ax.set_xlabel("Year")
        ax.set_ylabel("$h$")
        ax.legend(loc="upper right")

        return fig

    def graph_variability(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
        graph_variability_resource(ax1, dataframe=self.data_month_piv, title="Monthly Average GHI",
                                   y_label="$kWh/m^2/day$", label="$GHI_{avg}$", min_viability=self.min_irr_pv,
                                   viability_label="$GHI_{min}$")

        grap_boxplot_resource(ax2, dataframe=self.data_month, title="Monthly Average GHI", y_label="$kWh/m^2/day$")
        return fig

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def viability_graph(self):
        return self.psh_graph()

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def all_graph(self):
        if self.raw:
            graph_raw_data_resource('Global Horizontal Irradiance (GHI)', self.data, "$kWh/m^2/day$", "GHI")
        self.psh_graph()
        self.graph_variability()
        return


class Wind:
    """Analysis of the wind resource through the Peak Sun Hours, resource variability and calculation of autonomy
    from historical monthly average flow data.

    Returns:
        Object: Wind object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data, min_ws_wind) -> None:
        self.data_month = None
        self.wind_mean_month = None
        self.data_month_piv = None
        self.wind_mean = None
        self.data = data
        self.min_ws_wind = min_ws_wind
        self.raw = False
        self.calculate_autonomy()

    def calculate_autonomy(self):
        # Prepare data
        self.wind_mean_month = self.data.groupby(
            pd.PeriodIndex(self.data["Fecha"], freq="M")
        )["Valor"].mean()
        self.wind_mean_month.sort_index()
        self.data_month, self.data_month_piv = get_data_month(self.data)
        self.__variability = calculate_variability(self.data_month_piv)
        self.__autonomy = calculate_autonomy(self.data_month_piv, self.min_ws_wind)

    def potential(self, show, installed_capacity=1000):
        # p = 100  # Prate kW
        vc = 2
        vr = 12
        vf = 27

        df = pd.DataFrame(index=self.data_month_piv.index)
        df["v"] = self.data_month_piv["mean"]
        df["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        def powe_gen_a(x):
            return (
                installed_capacity * x["days"] * (x["v"] - vc) / (vr - vc)
                if (vc < x["v"] < vr)
                else 0
            )

        def powe_gen_b(x):
            return (
                installed_capacity * x["days"]
                if (vr < x["v"] < vf)
                else x["monthly energy"]
            )

        df["monthly energy"] = df.apply(powe_gen_a, axis=1)
        df["monthly energy"] = df.apply(powe_gen_b, axis=1)

        power_generation = np.sum(df["monthly energy"].tolist()) / 365
        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        if show:
            capacity_factor = power_generation / (installed_capacity * 24)
            print("\n:: Wind ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation

    def wind_speed_graph(self):
        # Plot figure
        fig = plt.figure()
        ax = fig.add_subplot()
        # Plot month data
        self.wind_mean_month.plot(kind="line", x="Fecha", y="Valor", ax=ax, label="V")

        self.wind_mean = self.data["Valor"].mean()
        ax.hlines(
            y=self.wind_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="$V_{avg}$" + " = {:.2f}".format(self.wind_mean),
        )
        ax.set_title("Monthly Average Wind Speed")
        ax.set_xlabel("Year")
        ax.set_ylabel("$m/s$")
        ax.legend(loc="upper right")

        return fig

    def graph_variability(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
        graph_variability_resource(ax1, dataframe=self.data_month_piv, title="Monthly Average Wind Speed",
                                   y_label="$m/s$", label="$V_{avg}$", min_viability=self.min_ws_wind,
                                   viability_label="$V_{min}$")

        grap_boxplot_resource(ax2, dataframe=self.data_month, title="Monthly Average Wind Speed", y_label="$m/s$")
        return fig

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def viability_graph(self):
        return self.wind_speed_graph()

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def all_graph(self):
        if self.raw:
            graph_raw_data_resource('Wind Speed', self.data, "$m/s$", "V")
        self.wind_speed_graph()
        self.graph_variability()
        return


class Biomass:
    """Analysis of the biomass resource through the biogas, resource variability and calculation of autonomy from 
    historical monthly average flow data.

    Returns:
        Object: Biomass object
    """

    __is_viability: bool = True
    __variability: float = 0.0
    __autonomy: float = None

    def __init__(self, data, collection_regime) -> None:
        self.data, self.raw_data = self.transform_data(data, collection_regime)
        self.raw = False
        # Porcine or Swine or Pig Slurry
        # Cattle Slurry
        # poultry manure
        # print(self.raw_data)
        self.raw_data.insert(0, "Source", ["Bovine", "Porcine", "Poultry", "Equine", "Goats", "Sheep",
                                           "Sugar Cane Bagasse"])
        self.raw_data = self.raw_data.set_index("Source")
        self.calculate_autonomy()
        # print(data)
        # print(self.raw_data)

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def all_graph(self):
        fig, ax1 = plt.subplots(1, 1, figsize=(8, 6))
        ax1_twin = ax1.twinx()
        data = self.raw_data[self.raw_data.Biogas != 0]
        """
        print(data.to_markdown())
        data.Biogas.plot.bar(ax=ax1, width=0.3)

        ax1.set_title("Available resource")
        ax1.set_ylabel("$\%$ used of available resource")
        ax1_twin.set_ylabel("$m^3/day$")
        ax1.legend(loc="upper center")
        bottom, top = ax1.get_ylim()
        ax1.set_ylim([0, top * 1.15])
        ax1.bar_label(ax1.containers[0], fmt='%d')

        # for p in ax1.patches:
        #    ax1.annotate(str(round(p.get_height()))+"\%", (p.get_x() * 1.005, p.get_height() * 1.005), )
        plt.scatter(x=data.index.values, y=data["Percentage"], color="k", marker="D")

        bottom, top = ax1_twin.get_ylim()
        ax1_twin.set_ylim([0, top * 1.5])
        """
        fig = plt.figure()
        # Sample data
        values = data["Biogas"]
        labels = [f"{value}\n{int(data['Biogas'][value])}"
                  + " $m^3/day$"
                  + f"\n{round(float(data['Percentage'][value]), 1)}"
                  + "\% of total available"
                  for value in data.index.values]

        # Treemap
        squarify.plot(sizes=values, label=labels, alpha=0.7, pad=0.01)

        # Remove the axis:
        plt.axis("off")
        return

    @staticmethod
    def transform_data(data, collection_regime):
        factor = list(data["Factor"])
        if collection_regime == 1:
            regime_selected = 0.1

        elif collection_regime == 2:
            regime_selected = 0.2

        elif collection_regime == 3:
            regime_selected = 0.3

        else:
            regime_selected = "Recomendado"

        result = np.array(list(data[regime_selected])) * np.array(factor)
        raw_data = data[[regime_selected, "Factor"]]
        raw_data.insert(0, "Biogas", list(result))
        raw_data = raw_data.rename(columns={regime_selected: 'Availability'})
        raw_data.insert(0, "Percentage", list(np.array(list(raw_data['Availability'])) /
                                              np.array(list(data['Total'])) * 100))
        return np.sum(result), raw_data

    def calculate_autonomy(self):
        self.__autonomy = 1

    def potential(self, show, installed_capacity=1000):
        pci = 4.77  # Lower caloric potential[kW/h/m^3]
        n = 0.32  # Typical condition
        n_turbine = math.ceil(installed_capacity / 100)
        operation_regime = 8
        q_turbine = 85

        if n_turbine * q_turbine > self.data / 24:
            q_design = self.data / 24
        else:
            q_design = n_turbine * q_turbine

        power_generation = pci * n * q_design * operation_regime
        """ Llevas a dataframe y al cálculo por meses
        df["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        def nt_calc(x):
            return x["PSH"] * installed_capacity * n * x["days"]

        df["monthly energy"] = df.apply(nt_calc, axis=1) 

        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])"""
        if show:
            capacity_factor = power_generation / (pci * n * q_design * 24)
            print("\n:: Biomass - Biogas ::")
            # print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW month]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation
