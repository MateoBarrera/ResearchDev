import pandas as pd
import matplotlib.pyplot as plt  # pylint: disable=import-error
import numpy as np
import seaborn as sns  # pylint: disable=import-error

# plt.style.use("seaborn-paper")
# plt.style.use('ggplot')

font = {
    "family": "serif",
    "color": "black",
    "weight": "bold",
    "size": 10,
}

###Local Method###
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


class Hydro:
    """Analysis of the water resource through the flow permanence curve, resource variability and calculation of autonomy from historical monthly average flow data.

    Returns:
        Object: Hydro object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data) -> None:
        self.data = data
        self.q_data = pd.DataFrame(data)["Valor"].to_list()
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
        ### Parameters ###
        e = 0.9  # Turbine efficiency
        n = 0.85  # Accessories efficiency
        H = 2  # Height
        ### End Parameters ###

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
            return (9.81 * (x["Qd"]) * H * e * n * 8 * x["days"]) if x["Qd"] > 0 else 0

        df["monthly energy"] = df.apply(power_gen, axis=1)

        def correction(x):
            return (
                installed_capacity * e * n * 8 * x["days"]
                if (x["monthly energy"] > installed_capacity * e * 24 * x["days"])
                else x["monthly energy"]
            )

        df["monthly energy"] = df.apply(correction, axis=1)
        power_generation = np.sum(df["monthly energy"].tolist()) / 365
        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        if show:
            capacity_factor = power_generation / (9.81 * 7 * H * e * n * 8760)
            print("\n:: Hydro ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor*100,2)}%"
            )
        return power_generation

    def flow_permanece_curve(self):
        """Evaluate the resource with the flow duration curve graph for the given data."""
        q_data_sort = np.sort(self.q_data)[::-1]
        q_frequency = (np.arange(1.0, len(q_data_sort) + 1) / len(q_data_sort)) * 100

        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot raw data
        self.data.plot(kind="line", x="Fecha", y="Valor", ax=ax1, label="Q")
        ax1.hlines(
            y=self.q_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="Average Q= {:.2f}".format(self.q_mean),
        )
        ax1.hlines(
            y=self.q_sr,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f}".format(self.q_sr),
        )

        ax1.set_title("Average monthly flow", fontdict=font)
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("Q [m^3/s]", fontdict=font)
        ax1.legend(loc="upper left")

        # Flow permanence curve
        ax2.plot(q_frequency, q_data_sort)

        ax2.fill_between(
            q_frequency[0 : self.q_sr_index],
            q_data_sort[0 : self.q_sr_index],
            self.q_sr,
            alpha=0.2,
            color="b",
        )
        ax2.fill_between(
            q_frequency[self.q_sr_index :],
            q_data_sort[self.q_sr_index :],
            self.q_sr,
            alpha=0.2,
            color="r",
        )
        ax2.hlines(
            y=self.q_sr,
            xmin=q_frequency[0],
            xmax=q_frequency[-1],
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f}".format(self.q_sr),
        )
        ax2.set_xlabel("Percentage of occurrence [%]", fontdict=font)
        ax2.set_ylabel("Flow rate [m^3/s]", fontdict=font)
        ax2.set_title("Flow permanence curve", fontdict=font)
        ax2.legend(loc="upper right")
        plt.subplots_adjust(hspace=0.3, bottom=0.1)

        return fig

    def graph_variability(self):
        # Prepare data
        data_month = self.data_month
        data_month_piv = self.data_month_piv

        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        data_month_piv.plot(kind="line", ax=ax1, alpha=0.4)

        # Mean chart
        data_month_piv["mean"] = data_month_piv.mean(axis=1)
        data_month_piv["std"] = data_month_piv.std(axis=1)
        data_month_piv.plot(kind="line", y="mean", ax=ax1, style="--k")
        ax1.fill_between(
            data_month_piv.index,
            data_month_piv["mean"] - data_month_piv["std"],
            data_month_piv["mean"] + data_month_piv["std"],
            alpha=0.15,
        )
        ax1.hlines(
            y=self.q_sr,
            xmin=data_month_piv.index.min(),
            xmax=data_month_piv.index.max(),
            colors="red",
            linestyles="--",
            label="Qsr = {:.2f}".format(self.q_sr),
        )
        ax1.set_title("River regime", fontdict=font)
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("Q [m^3/s]", fontdict=font)

        data_month["Mes"] = pd.to_datetime(
            data_month.index.month, format="%m"
        ).month_name()

        # Boxplot chart
        sns.boxplot(data=data_month, x="Mes", y="Valor", ax=ax2)
        ax2.set_title("Average monthly flow", fontdict=font)
        ax2.set_xlabel("Year", fontdict=font)
        ax2.set_ylabel("Q [m^3/s]", fontdict=font)

        plt.subplots_adjust(hspace=0.5, bottom=0.1)
        return fig

    def graph_pdc(self):
        y = 1000  #
        H = 2
        n = 0.85
        df = pd.DataFrame(index=self.data_month_piv.index)
        df["q"] = self.data_month_piv["mean"] - self.q_sr
        df[df < 0] = 0
        df["potencial"] = y * df["q"] * H * n / 1000

        q_data_sort = np.sort(self.q_data)[::-1]

        q_frequency = (np.arange(1.0, len(q_data_sort) + 1) / len(q_data_sort)) * 100
        q_data_p = q_frequency * q_data_sort * y * H * n / 1000
        # print(q_data_p)
        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot raw data
        ax1.plot(q_frequency, q_data_sort)

        ax1.fill_between(
            q_frequency[0 : self.q_sr_index],
            q_data_sort[0 : self.q_sr_index],
            self.q_sr,
            alpha=0.2,
            color="b",
        )
        ax1.fill_between(
            q_frequency[self.q_sr_index :],
            q_data_sort[self.q_sr_index :],
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
        ax1.set_xlabel("Percentage of occurrence [%]", fontdict=font)
        ax1.set_ylabel("Flow rate [m^3/s]", fontdict=font)
        ax1.set_title("Flow permanence curve", fontdict=font)
        ax1.legend(loc="upper right")
        plt.subplots_adjust(hspace=0.3, bottom=0.1)

        # Flow permanence curve
        q_sort = np.sort(df["q"])[::-1]
        q_power_sort = np.sort(df["potencial"])[::-1]
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
        ax2.set_xlabel("Flow rate [m^3/s]", fontdict=font)
        ax2.set_ylabel("Power generation [Wh]", fontdict=font)
        ax2.set_title("Power duration curve", fontdict=font)
        ax2.legend(loc="upper right")
        plt.subplots_adjust(hspace=0.3, bottom=0.1)
        plt.show()
        # return fig

    @property
    def viability_graph(self):
        return self.flow_permanece_curve()

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability Resource: {:.2f}% ::".format(self.__variability)

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def autonomy(self):
        print("Months higher than the ecological flow.")
        return ":: Autonomy Resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def all_graph(self):
        self.flow_permanece_curve()
        self.graph_variability()
        return


class Pv:
    """Analysis of the solar resource through the Peak Sun Hours, resource variability and calculation of autonomy from historical monthly average flow data.

    Returns:
        Object: Pv object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data, min_irr_pv) -> None:
        self.data = data
        self.min_irr_pv = min_irr_pv
        self.calculate_autonomy()

    def calculate_autonomy(self):
        # Prepare data
        self.irr_mean_month = self.data.groupby(
            pd.PeriodIndex(self.data["Fecha"], freq="M")
        )["Valor"].mean()
        self.irr_mean_month.sort_index()
        self.data_month, self.data_month_piv = get_data_month(self.data)
        self.__variability = calculate_variability(self.data_month_piv)
        self.__autonomy = calculate_autonomy(self.data_month_piv, self.min_irr_pv)

    def potential(self, show, installed_capacity=1000):
        pp = 0.200  # Peak power of the panel [kW year]
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
            capacity_factor = power_generation / (installed_capacity * 8760)
            print("\n:: Solar ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor*100,2)}%"
            )
        return power_generation

    def psh_graph(self):
        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot raw data
        self.data.plot(kind="line", x="Fecha", y="Valor", ax=ax1, label="GHI")

        self.irr_mean = self.data["Valor"].mean()
        ax1.hlines(
            y=self.irr_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="Average GHI= {:.2f}k".format(self.irr_mean),
        )
        ax1.set_title(
            "Total daily solar irradiance incident - Global Horizontal Irradiance",
            fontdict=font,
        )
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("Irradiance [kWh/m^2/day]", fontdict=font)
        ax1.legend(loc="upper left")

        # Plot month data
        self.irr_mean_month.plot(kind="line", x="Fecha", y="Valor", ax=ax2, label="PHS")

        self.irr_mean = self.data["Valor"].mean()
        ax2.hlines(
            y=self.irr_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="Average PHS= {:.2f}".format(self.irr_mean),
        )
        ax2.set_title("Monthly Peak Sun Hours", fontdict=font)
        ax2.set_xlabel("Year", fontdict=font)
        ax2.set_ylabel("PHS [h]", fontdict=font)
        ax2.legend(loc="upper left")

        return fig

    def graph_variability(self):
        # Prepare data
        data_month = self.data_month
        data_month_piv = self.data_month_piv

        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        data_month_piv.plot(kind="line", ax=ax1, alpha=0.4)

        # Mean chart
        data_month_piv["mean"] = data_month_piv.mean(axis=1)
        data_month_piv["std"] = data_month_piv.std(axis=1)
        data_month_piv.plot(kind="line", y="mean", ax=ax1, style="--k")
        ax1.fill_between(
            data_month_piv.index,
            data_month_piv["mean"] - data_month_piv["std"],
            data_month_piv["mean"] + data_month_piv["std"],
            alpha=0.15,
        )
        ax1.hlines(
            y=self.min_irr_pv,
            xmin=data_month_piv.index.min(),
            xmax=data_month_piv.index.max(),
            colors="red",
            linestyles="--",
            label="Min Irradiance = {:.2f}".format(self.min_irr_pv),
        )
        ax1.set_title("Monthly Peak Sun Hours", fontdict=font)
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("PHS [h]", fontdict=font)

        data_month["Mes"] = pd.to_datetime(
            data_month.index.month, format="%m"
        ).month_name()

        # Boxplot chart
        sns.boxplot(data=data_month, x="Mes", y="Valor", ax=ax2)
        ax2.set_title("Monthly Peak Sun Hours", fontdict=font)
        ax2.set_xlabel("Year", fontdict=font)
        ax2.set_ylabel("PHS [h]", fontdict=font)

        plt.subplots_adjust(hspace=0.5, bottom=0.1)
        return fig

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability Resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy Resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def viability_graph(self):
        return self.psh_graph()

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def all_graph(self):
        self.psh_graph()
        self.graph_variability()
        return


class Wind:
    """Analysis of the wind resource through the Peak Sun Hours, resource variability and calculation of autonomy from historical monthly average flow data.

    Returns:
        Object: Wind object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data, min_ws_wind) -> None:
        self.data = data
        self.min_ws_wind = min_ws_wind
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
        p = 100  # Prate kW
        vc = 2
        vr = 12
        vf = 27

        df = pd.DataFrame(index=self.data_month_piv.index)
        df["v"] = self.data_month_piv["mean"]
        df["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        def powe_gen_a(x):
            return (
                installed_capacity * x["days"] * (x["v"] - vc) / (vr - vc)
                if (vc < x["v"] and x["v"] < vr)
                else 0
            )

        def powe_gen_b(x):
            return (
                installed_capacity * x["days"]
                if (vr < x["v"] and x["v"] < vf)
                else x["monthly energy"]
            )

        df["monthly energy"] = df.apply(powe_gen_a, axis=1)
        df["monthly energy"] = df.apply(powe_gen_b, axis=1)

        power_generation = np.sum(df["monthly energy"].tolist()) / 365
        df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        if show:
            capacity_factor = power_generation / (installed_capacity * 8760)
            print("\n:: Wind ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kW year]; Capacity Factor {round(capacity_factor*100,2)}%"
            )
        return power_generation

    def wind_speed_graph(self):
        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

        # Plot raw data
        self.data.plot(kind="line", x="Fecha", y="Valor", ax=ax1, label="wind speed")

        self.wind_mean = self.data["Valor"].mean()
        ax1.hlines(
            y=self.wind_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="Average ws= {:.2f}".format(self.wind_mean),
        )
        ax1.hlines(
            y=self.min_ws_wind,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="red",
            linestyles="--",
            label="min ws= {:.2f}".format(self.min_ws_wind),
        )
        ax1.set_title("Monthly average wind speed", fontdict=font)
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("Wind speed [m/s]", fontdict=font)
        ax1.legend(loc="upper left")

        # Plot month data
        self.wind_mean_month.plot(kind="line", x="Fecha", y="Valor", ax=ax2, label="ws")

        self.wind_mean = self.data["Valor"].mean()
        ax2.hlines(
            y=self.wind_mean,
            xmin=self.data["Fecha"].min(),
            xmax=self.data["Fecha"].max(),
            colors="gray",
            linestyles="--",
            label="Average ws= {:.2f}".format(self.wind_mean),
        )
        ax2.set_title("Monthly average wind speed", fontdict=font)
        ax2.set_xlabel("Year", fontdict=font)
        ax2.set_ylabel("Wind speed [m/s]", fontdict=font)
        ax2.legend(loc="upper left")

        return fig

    def graph_variability(self):
        # Prepare data
        data_month = self.data_month
        data_month_piv = self.data_month_piv

        # Plot figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        data_month_piv.plot(kind="line", ax=ax1, alpha=0.4)

        # Mean chart
        data_month_piv["mean"] = data_month_piv.mean(axis=1)
        data_month_piv["std"] = data_month_piv.std(axis=1)
        data_month_piv.plot(kind="line", y="mean", ax=ax1, style="--k")
        ax1.fill_between(
            data_month_piv.index,
            data_month_piv["mean"] - data_month_piv["std"],
            data_month_piv["mean"] + data_month_piv["std"],
            alpha=0.15,
        )
        ax1.hlines(
            y=self.min_ws_wind,
            xmin=data_month_piv.index.min(),
            xmax=data_month_piv.index.max(),
            colors="red",
            linestyles="--",
            label="Min wind speed = {:.2f}".format(self.min_ws_wind),
        )
        ax1.set_title("Monthly average wind speed", fontdict=font)
        ax1.set_xlabel("Year", fontdict=font)
        ax1.set_ylabel("Wind speed [m/s]", fontdict=font)

        data_month["Mes"] = pd.to_datetime(
            data_month.index.month, format="%m"
        ).month_name()

        # Boxplot chart
        sns.boxplot(data=data_month, x="Mes", y="Valor", ax=ax2)
        ax2.set_title("Monthly average wind speed", fontdict=font)
        ax2.set_xlabel("Year", fontdict=font)
        ax2.set_ylabel("Wind speed [m/s]", fontdict=font)

        plt.subplots_adjust(hspace=0.5, bottom=0.1)
        return fig

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability Resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy Resource: {:.2f}% ::".format(self.__autonomy * 100)

    @property
    def viability_graph(self):
        return self.wind_speed_graph()

    @property
    def variability_graph(self):
        return self.graph_variability()

    @property
    def all_graph(self):
        self.wind_speed_graph()
        self.graph_variability()
        return


class Biomass:
    """Analysis of the solar resource through the Peak Sun Hours, resource variability and calculation of autonomy from historical monthly average flow data.

    Returns:
        Object: PV object
    """

    __is_viability: bool = False
    __variability: float = None
    __autonomy: float = None

    def __init__(self, data) -> None:
        self.data = data
        self.q_data = pd.DataFrame(data)["Valor"].to_list()
        self.calculate_autonomy()

    @property
    def is_viability(self):
        return self.__is_viability

    @property
    def variability(self):
        return ":: Variability Resource: {:.2f}% ::".format(self.__variability)

    @property
    def autonomy(self):
        return ":: Autonomy Resource: {:.2f}% ::".format(self.__autonomy * 100)

    def calculate_autonomy(self):
        # df = df.rename(index=lambda x: x.strftime("%B"))
        df = df.drop(columns=["days"])
        pass