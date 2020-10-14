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
    """
  file is typically 'dlc_all_avgs_updated.csv'
  variable is either 'cat_ditance' or 'vel'
  ylab is the y-axis label
  colors is a list of two colors (e.g., ["#0062FF", "#DB62FF"])
  output_dir to ave the plot in a specific dir when save is True
  """

    df = pd.read_csv(file)
    df = df[df['var'] == variable]

    sns.set(style='ticks', font_scale=1)

    plt.figure(figsize=(13, 5), dpi=100)

    if colors is False:
        my_pal = {'Control': '#00FFFF', 'Infected': '#E60E3C'}
    else:
        my_pal = {'Control': colors[0], 'Infected': colors[1]}

    ax = sns.boxplot(x='trial',
                     y='value',
                     data=df,
                     hue='infection_status',
                     palette=my_pal)

    if jitter is True:
        sns.stripplot(x='trial',
                      y='value',
                      data=df,
                      color='black',
                      size=3,
                      jitter=1)

    for i in range(len(df['trial'].unique()) - 1):

        def vLines(i, j):
            '''add vertical lines to seperate boxplots pairs (style)'''
            return plt.vlines(i + .5,
                              i,
                              j,
                              linestyles='solid',
                              colors='black',
                              alpha=0.2)
            if variable == 'vel':
                vLines(10, 45)
            elif variable == 'cat_distance':
                vLines(0, 1.3)

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

    fig = ax.get_figure()

    if save is True:

        def sav(myString):
            return fig.savefig(myString,
                               bbox_inches='tight',
                               dpi=100,
                               pad_inches=0.1)
            if output_dir is not False:
                sav(f'{output_dir}/{variable}.png')
            else:
                sav(f'{variable}.png')
