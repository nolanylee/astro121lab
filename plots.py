import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('qt4agg')
import matplotlib.pyplot as plt
#if using ipython/jupyter can use format statements below
#%matplotlib inline 
#config InlineBackend.figure_format = 'jpeg'
import seaborn as sns

test_data = pd.read_csv("~/radiolab/test_data_012222") #file path dependent on local machine, change as necessary

#pull dataframe series into numpy arrays
fgen_100_sample_230 = np.array(test_data['fgen_100_sample_230'])
fgen_100_sample_250 = np.array(test_data['fgen_100_sample_250'])
fgen_100_sample_300 = np.array(test_data['fgen_100_sample_300'])
fgen_100_sample_1000 = np.array(test_data['fgen_100_sample_1000'])
fgen_100_sample_1600 = np.array(test_data['fgen_100_sample_1600'])
fgen_100_sample_2200 = np.array(test_data['fgen_100_sample_2200'])
fgen_50_sample_250 = np.array(test_data['fgen_50_sample_250'])
fgen_125_sample_250 = np.array(test_data['fgen_125_sample_250'])
fgen_250_sample_250 = np.array(test_data['fgen_250_sample_250'])
fgen_300_sample_250 = np.array(test_data['fgen_300_sample_250'])

times = np.array(range(len(fgen_100_sample_230))) #initialize arbitrary numpy array to make up x-axis for plots

plt.plot(times, fgen_100_sample_1600)

def axes_settings(fig, ax, title, ymax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, ymax+1)
    ax.set_title(title)
#%%
