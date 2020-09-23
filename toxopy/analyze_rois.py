import os
import json
import numpy as np
from glob import glob
import pandas as pd
from toxopy import fwarnings, trials
import matplotlib.patches as patches
from collections import namedtuple
from dlcu import time_in_each_roi
import matplotlib.pyplot as plt
from pathlib import Path


def analyze_rois(input_dir, room_layout, output_dir, show_plot=False):

    files = glob(f'{input_dir}/*.csv')

    for file in files:

        cat = Path(file).stem

        for trial in trials():

            df = pd.read_csv(file)
            df = df.dropna()
            df = df[(df['trial'] == trial)]

            with open(room_layout) as json_file:
                p = json.load(json_file)

            velocity = df['velocity_loess05']
            x_cat, y_cat = df['x_cat_loess05'], df['y_cat_loess05']

            def posi(cat):
                position = namedtuple('position', ['topleft', 'bottomright'])
                d = {}
                for dr in ['middle', 'right', 'left', 'top', 'bottom']:
                    t = []
                    for x, r in zip(['tl', 'br', 'tl', 'br'], [0, 1, 0, 1]):
                        t.append(p[cat][f'{dr}_{x}'][r])
                    d[str(dr)] = position((t[0], t[1]), (t[2], t[3]))
                return d

            rois = posi(cat)

            bp_tracking = np.array((x_cat, y_cat, velocity))

            if show_plot is True:
                fig, ax = plt.subplots(1)

                plt.plot(x_cat, y_cat, '.-')

                positions = ['middle', 'right', 'left', 'top', 'bottom']
                colors = ['orange', 'purple', 'red', 'blue', 'green']

                for a, color in zip(positions, colors):
                    rect = patches.Rectangle(
                        rois[a].topleft,
                        rois[a].bottomright[0] - rois[a].topleft[0],
                        rois[a].bottomright[1] - rois[a].topleft[1],
                        linewidth=1,
                        edgecolor=color,
                        facecolor='none')
                    ax.add_patch(rect)

                plt.ylim(-100, 600)
                plt.show()

            res = time_in_each_roi.get_timeinrois_stats(bp_tracking.T,
                                                        rois,
                                                        fps=30,
                                                        returndf=True,
                                                        check_inroi=True)

            res['trial'] = trial

            def rT(p):
                return (res['ROI_name'] == p)

            walls = res.loc[rT('right') | rT('left') | rT('top') | rT('bottom')]
            middle = res.loc[res['ROI_name'] == 'middle']

            def sumUP(rpos, name):
                dfx = rpos.sum(axis=0)
                dfx['ROI_name'], dfx['trial'] = name, trial
                return dfx.T

            dfW, dfM = sumUP(walls, 'walls'), sumUP(middle, 'middle')

            dfF = pd.concat([dfW, dfM], axis=1, sort=False).T

            dfF.to_csv(f'{output_dir}/.{cat}_{trial}_del.csv',
                            index=False,
                            encoding='utf-8')

        files = glob(f'{output_dir}/.*_deleteme.csv')

        for file in files:

            df2 = pd.read_csv(file)

            df2 = df2[[
                'ROI_name', 'transitions_per_roi', 'cumulative_time_in_roi_sec',
                'avg_time_in_roi_sec', 'avg_vel_in_roi', 'trial'
            ]]

            df2.to_csv(file, index=False)

        combined_csv = pd.concat([pd.read_csv(f) for f in files])
        combined_csv.to_csv(f'{output_dir}/{cat}.csv', index=False, encoding='utf-8-sig')

        [os.remove(f) for f in files]
