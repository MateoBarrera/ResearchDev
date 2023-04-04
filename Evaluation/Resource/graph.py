import numpy as np
import matplotlib.pyplot as plt

# plt.style.use("seaborn-paper")
# plt.style.use('ggplot')

font = {
    "family": "serif",
    "color": "black",
    "weight": "bold",
    "size": 10,
}


def flow_permanece_curve(cls):
    """Evaluate the resource with the flow duration curve graph for the given data."""
    q_data_sort = np.sort(cls.q_data)[::-1]
    q_frequency = (np.arange(1.0, len(q_data_sort) + 1) / len(q_data_sort)) * 100

    # Plot figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # Plot raw data
    cls.data.plot(kind="line", x="Fecha", y="Valor", ax=ax1, label="Q")
    ax1.hlines(
        y=cls.q_mean,
        xmin=cls.data["Fecha"].min(),
        xmax=cls.data["Fecha"].max(),
        colors="gray",
        linestyles="--",
        label="Average Q= {:.2f}".format(cls.q_mean),
    )
    ax1.hlines(
        y=cls.q_sr,
        xmin=cls.data["Fecha"].min(),
        xmax=cls.data["Fecha"].max(),
        colors="red",
        linestyles="--",
        label="Qsr = {:.2f}".format(cls.q_sr),
    )

    ax1.set_title("Average monthly flow", fontdict=font)
    ax1.set_xlabel("Year", fontdict=font)
    ax1.set_ylabel("Q [m^3/s]", fontdict=font)
    ax1.legend(loc="upper left")

    # Flow permanence curve
    ax2.plot(q_frequency, q_data_sort)

    ax2.fill_between(
        q_frequency[0 : cls.q_sr_index],
        q_data_sort[0 : cls.q_sr_index],
        cls.q_sr,
        alpha=0.2,
        color="b",
    )
    ax2.fill_between(
        q_frequency[cls.q_sr_index :],
        q_data_sort[cls.q_sr_index :],
        cls.q_sr,
        alpha=0.2,
        color="r",
    )
    ax2.hlines(
        y=cls.q_sr,
        xmin=q_frequency[0],
        xmax=q_frequency[-1],
        colors="red",
        linestyles="--",
        label="Qsr = {:.2f}".format(cls.q_sr),
    )
    ax2.set_xlabel("Percentage of occurrence [%]", fontdict=font)
    ax2.set_ylabel("Flow rate [m^3/s]", fontdict=font)
    ax2.set_title("Flow permanence curve", fontdict=font)
    ax2.legend(loc="upper right")
    plt.subplots_adjust(hspace=0.3, bottom=0.1)

    return fig
