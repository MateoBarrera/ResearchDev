import math
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt  # pylint: disable=import-error
import numpy as np
import seaborn as sns  # pylint: disable=import-error

plt.style.use('seaborn-v0_8-colorblind')
# plt.style.use('evaluation/resource/graph.mplstyle')
fsize = 18
tsize = 10
tdir = 'in'
major = 5.0
minor = 3.0
lwidth = 0.8
lhandle = 2.0
plt.style.use('default')
plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = fsize
plt.rcParams['legend.fontsize'] = tsize
plt.rcParams['xtick.direction'] = tdir
plt.rcParams['ytick.direction'] = tdir
plt.rcParams['xtick.major.size'] = major
plt.rcParams['xtick.minor.size'] = minor
plt.rcParams['ytick.major.size'] = 5.0
plt.rcParams['ytick.minor.size'] = 3.0
plt.rcParams['axes.linewidth'] = lwidth
plt.rcParams['legend.handlelength'] = lhandle
plt.rcParams['font.family'] = "serif"


def graph_resource():
    pass
