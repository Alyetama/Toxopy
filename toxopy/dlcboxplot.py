"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from toxopy import fwarnings
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def dlcboxplot(file,
               variable,
               ylab,
               jitter=False,
               colors=False,
               title=False,
               save=False,
               output_dir=False):

    df = pd.read_csv(file)
    df = df[df['var'] == variable]

    sns.set(style="ticks", font_scale=1)

    plt.figure(figsize=(13, 5), dpi=100)

    if colors is False:
        my_pal = {"Negative": "#00FFFF", "Positive": "#E60E3C"}
    else:
        my_pal = {"Negative": colors[0], "Positive": colors[1]}

    ax = sns.boxplot(x='trial',
                     y='value',
                     data=df,
                     hue='status',
                     palette=my_pal)

    if jitter is True:

        sns.stripplot(x='trial',
                      y='value',
                      data=df,
                      color='black',
                      size=3,
                      jitter=1)
    '''add vertical lines to seperate boxplots pairs (style)'''
    for i in range(len(df['trial'].unique()) - 1):
        if variable == 'vel':
            plt.vlines(i + .5,
                       10,
                       45,
                       linestyles='solid',
                       colors='black',
                       alpha=0.2)
        elif variable == 'cat_distance':
            plt.vlines(i + .5,
                       0,
                       1.3,
                       linestyles='solid',
                       colors='black',
                       alpha=0.2)

    if title is not False:
        plt.title(title, fontsize=14)
    else:
        pass

    ax.set(xlabel='Trial', ylabel=ylab)

    plt.legend(title='Infection Status')
    '''add significance bars and asterisks between boxes'''
    # [first pair, second pair], ..., [|, –], ...
    if variable == 'vel':
        l = [[7.75, 5.75], [8.25, 6.25], [26, 28], [31, 33]]
    elif variable == 'cat_distance':
        l = [[7.75, 5.75], [8.25, 6.25], [0.85, 0.9], [0.95, 1]]

    for x1, x2, y1, y2 in zip(l[0], l[1], l[2], l[3]):
        sig = plt.plot([x1, x1, x2, x2], [y1, y2, y2, y1],
                       linewidth=1,
                       color='k')
        plt.text((x1 + x2) * .5, y2 + 0, "*", ha='center', va='bottom')

    plt.show()

    if save is True:
        fig = ax.get_figure()
        if output_dir is not False:
            fig.savefig(f'{output_dir}/{variable}.png',
                        bbox_inches="tight",
                        dpi=100,
                        pad_inches=0.1)
        else:
            fig.savefig(f'{variable}.png',
                        bbox_inches="tight",
                        dpi=100,
                        pad_inches=0.1)
