"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import os
from rdp import rdp
import pandas as pd
import numpy as np
from toxopy import fwarnings
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
from pathlib import Path
# %matplotlib inline


def PlotTurnPoints(csv_file, turnpoints_dir, save=False, path=os.getcwd()):

    cats = sorted(list(pd.read_csv(csv_file).cat.unique()))
    positions = range(221, 225)

    DIR = sorted(glob(f'{turnpoints_dir}/*.csv'))

    files = []
    for i in sorted(DIR):
        if Path(i).stem in cats:
            files.append(i)

    def PlotCat(file, cat, pos):

        df = pd.read_csv(csv_file)
        tp = pd.read_csv(file)

        def slct(cat, coord):
            return df.loc[(df['cat'] == cat)][coord].to_numpy()

        df = df.loc[(df['cat'] == cat)]

        x, y = slct(cat, 'time'), slct(cat, 'velocity_loess05')

        def alt(firstispeak):
            if firstispeak == 'True':
                return ['bo', 'ro']
            if firstispeak == 'False':
                return ['ro', 'bo']
            return None

        firstispeak = str(tp['firstispeak'][0])
        P = alt(firstispeak)

        trajectory = pd.DataFrame([x, y])
        trajectory = trajectory.to_numpy().reshape(len(x), 2)

        idx = tp['tppos'].to_numpy()

        sns.set(style='ticks', font_scale=1)
        fig = plt.gcf()
        fig.set_size_inches(20, 12)

        ax = fig.add_subplot(pos)
        ax.plot(x, y, 'k-', label='Trajectory', alpha=0.8)

        for i, j, k in zip([0, 1], [P[0], P[1]], ['Maximum', 'Minimum']):
            ax.plot(x[idx][i::2],
                    y[idx][i::2],
                    j,
                    mfc='none',
                    label=f'Local {k}',
                    alpha=0.9)

        times = [0, 300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]

        for i in times:
            plt.axvline(x=i,
                        linestyle='--',
                        color='gray',
                        label='Trial Boundary',
                        alpha=0.4)

        handles, labels = plt.gca().get_legend_handles_labels()
        order = [3, 0, 1, 2]
        labels_handles = {
            label: handle
            for ax in fig.axes
            for handle, label in zip(*ax.get_legend_handles_labels())
        }
        ax.legend(
            [handles[q] for q in order],
            [labels[q] for q in order],
            loc="upper right",
            bbox_to_anchor=(1, 0.88),
            bbox_transform=plt.gcf().transFigure,
        )

#     fig, ax = plt.subplots(nrows=2,
#                            ncols=2,
#                            sharex=True,
#                            sharey=True,
#                            figsize=(6, 6))

        font = {'family': 'DejaVu Sans', 'weight': 'regular', 'size': 18}

        plt.rc('font', **font)

        fig.text(0.5, 0.05, 'Time', ha='center')
        fig.text(0.07,
                 0.5,
                 'Velocity in Pixels per Second',
                 va='center',
                 rotation='vertical')

    for file, cat, pos in zip(files, cats, positions):
        PlotCat(file, cat, pos)

    if save is True:
        plt.savefig(f'{path}/TurnPoints.png',
                    bbox_inches='tight', dpi=100, pad_inches=0.1)
