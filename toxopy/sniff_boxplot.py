from toxopy import fwarnings, trials
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import repeat
from itertools import chain


def sniff_boxplot(csv_file, colors=False, jitter=False, title=False, save=False, output_dir=False):
    """
    'csv_file' is the files with the vial sniff data,
        (here: 'bin_data_all_behaviors____frequency.csv').
    'colors' is a list of two colors in the order: [negative, positive].
    'jitter' is a boolean variable to display jitter or not, default is False.
    'title' is the title of the plot, default is False.
    'save' is a boolean variable to save thhe figure (True),
        or just show it (False: default).
    'output_dir' is the path to the location of the saved plot
        (default is False: the plot will be saved in the current working dir).
    """

    df0 = pd.read_csv(csv_file)

    cols = ['cat', 'infection_status', 't3_sniffsaline',
            't5_sniffurine', 't7_sniffsaline', 't9_sniffurine']

    df = df0[cols].copy()
    tls = trials()

    Negative, Positive = {}, {}
    dcts, strs = [Negative, Positive], ['Negative', 'Positive']

    for s, r in zip(dcts, strs):
        for i, j, in zip(tls[2::2], range(2, 6)):
            s[i] = df[df['infection_status'] == r][cols[j]]

    def itrchain(ls):
        return list(chain.from_iterable(ls))

    def achain(ls, x):
        return ls.append(list(repeat(x, len(i[j]))))

    df2 = pd.DataFrame()

    s, v, t = [], [], []

    for i, z in zip(dcts, strs):
        for j in tls[2::2]:
            achain(s, z), v.append(list(i[j])), achain(t, j)

    df2['status'], df2['value'], df2['trial'] = itrchain(
        s), itrchain(v), itrchain(t)

    sns.set(style="ticks", font_scale=1)

    plt.figure(figsize=(13, 5), dpi=100)

    if colors is False:
        my_pal = {"Negative": "#00FFFF", "Positive": "#E60E3C"}
    else:
        my_pal = {"Negative": colors[0], "Positive": colors[1]}

    ax = sns.boxplot(x='trial',
                     y='value',
                     data=df2,
                     hue='status',
                     palette=my_pal)

    if jitter is True:

        sns.stripplot(x='trial',
                      y='value',
                      data=df2,
                      color='black',
                      size=3,
                      jitter=1)

    '''add vertical lines to seperate boxplots pairs (style)'''
    for i in range(3):
        plt.vlines(i + .5,
                   1,
                   20,
                   linestyles='solid',
                   colors='black',
                   alpha=0.2)

    ax.set(xlabel='Trial', ylabel='Vial Sniff Duration')

    plt.legend(title='Infection Status')

    if title is not False:
        plt.title(title, fontsize=14)
    else:
        pass

    fig = ax.get_figure()

    if save is True:
        if output_dir is not False:
            name = f'{output_dir}/sniff_boxplot.png'
        else:
            name = 'sniff_boxplot.png'
        fig.savefig(name, bbox_inches="tight", dpi=100, pad_inches=0.1)

    plt.show()
