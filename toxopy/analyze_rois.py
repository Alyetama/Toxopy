import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from pathlib import Path
import numpy as np
import json
import matplotlib.pyplot as plt
from dlcu import PlottingResults, time_in_each_roi
from collections import namedtuple
import matplotlib.patches as patches
import glob
import os
# %matplotlib inline


def analyze_rois(file, room_layout, output_dir, trial_type):

    if output_dir.endswith('/') == False:

        raise ValueError(
            'Output directory does not end with a trailing slash "/"!')

    else:
        pass

    # Load dataset

    df = pd.read_csv(file)
    df = df.dropna()

    if trial_type == 'with_owner':

        t1 = df.loc[df['trial'] == 'No treatment']
        t3 = df.loc[df['trial'] == 'First Saline']
        t5 = df.loc[df['trial'] == 'First Urine']
        t7 = df.loc[df['trial'] == 'Second Saline']
        t9 = df.loc[df['trial'] == 'Second Urine']

        cat = str(Path(file).stem)[:-11]

        trials = [t1, t3, t5, t7, t9]

        trials_names = [
            'No treatment', 'First Saline', 'First Urine', 'Second Saline',
            'Second Urine'
        ]

    elif trial_type == 'cat_alone':

        t2 = df.loc[df['trial'] == 'Cat alone (1)']
        t4 = df.loc[df['trial'] == 'Cat alone (2)']
        t6 = df.loc[df['trial'] == 'Cat alone (3)']
        t8 = df.loc[df['trial'] == 'Cat alone (4)']
        t10 = df.loc[df['trial'] == 'Cat alone (5)']

        cat = str(Path(file).stem)[:-10]

        trials = [t2, t4, t6, t8, t10]

        trials_names = [
            'Cat alone (1)', 'Cat alone (2)', 'Cat alone (3)', 'Cat alone (4)',
            'Cat alone (5)'
        ]

    # Create variable names

    for trial, trial_name in zip(trials, trials_names):

        time = trial['time']
        velocity = trial['velocity_loess']

        if trial_type == 'with_owner':

            x_cat = trial['x_cat_loess']
            y_cat = trial['y_cat_loess']

        elif trial_type == 'cat_alone':

            x_cat = trial['x_loess']
            y_cat = trial['y_loess']

        # Calculate and plot rois

        def rois_gen(i):
            def getList(dict):
                list = []
                for key in dict.keys():
                    list.append(key)

                return list

            with open(room_layout) as json_file:
                p = json.load(json_file)

            catslist = getList(p)

            positions = [
                'middle', 'rightside', 'leftside', 'topside', 'bottomside'
            ]

            colors = ['orange', 'purple', 'red', 'blue', 'green']

            position = namedtuple('position', ['topleft', 'bottomright'])

            #two points defining each roi: topleft(X,Y) and bottomright(X,Y).

            return {
                'middle':
                position((p[i]['middle_tl'][0], p[i]['middle_tl'][1]),
                         (p[i]['middle_br'][0], p[i]['middle_br'][1])),
                'rightside':
                position((p[i]['right_tl'][0], p[i]['right_tl'][1]),
                         (p[i]['right_br'][0], p[i]['right_br'][1])),
                'leftside':
                position((p[i]['left_tl'][0], p[i]['left_tl'][1]),
                         (p[i]['left_br'][0], p[i]['left_br'][1])),
                'topside':
                position((p[i]['top_tl'][0], p[i]['top_tl'][1]),
                         (p[i]['top_br'][0], p[i]['top_br'][1])),
                'bottomside':
                position((p[i]['bottom_tl'][0], p[i]['bottom_tl'][1]),
                         (p[i]['bottom_br'][0], p[i]['bottom_br'][1]))
            }

        bp_tracking = np.array((x_cat, y_cat, velocity))

        rois = rois_gen(cat)

        fig, ax = plt.subplots(1)

        plt.plot(x_cat, y_cat, '.-')

        positions = [
            'middle', 'rightside', 'leftside', 'topside', 'bottomside'
        ]
        colors = ['orange', 'purple', 'red', 'blue', 'green']

        for position, color in zip(positions, colors):

            rect = patches.Rectangle(
                rois[position].topleft,
                rois[position].bottomright[0] - rois[position].topleft[0],
                rois[position].bottomright[1] - rois[position].topleft[1],
                linewidth=1,
                edgecolor=color,
                facecolor='none')
            ax.add_patch(rect)

        plt.ylim(-100, 600)
        # plt.show()
        plt.close()

        res = time_in_each_roi.get_timeinrois_stats(bp_tracking.T,
                                                    rois,
                                                    fps=30,
                                                    returndf=True,
                                                    check_inroi=True)

        current_trial = []

        for x in range(0, len(res)):

            current_trial.append(trial_name)

        res['trial'] = current_trial

        walls = res.loc[(res['ROI_name'] == 'rightside') |
                        (res['ROI_name'] == 'leftside') |
                        (res['ROI_name'] == 'topside') |
                        (res['ROI_name'] == 'bottomside')]

        middle = res.loc[res['ROI_name'] == 'middle']

        df_walls = walls.sum(axis=0)
        df_walls['ROI_name'] = 'walls'
        df_walls['trial'] = trial_name
        df_walls = df_walls.T

        df_middle = middle.sum(axis=0)
        df_middle['ROI_name'] = 'middle'
        df_middle['trial'] = trial_name
        df_middle = df_middle.T

        df_final = pd.concat([df_walls, df_middle], axis=1, sort=False)
        df_final = df_final.T

        df_final.to_csv(output_dir + cat + trial_name + '_deleteme' + '.csv',
                        index=False,
                        sep=',',
                        encoding='utf-8')

    files = glob.glob(output_dir + '*_deleteme.csv')

    for file in files:

        df2 = pd.read_csv(file)

        df2 = df2[[
            'ROI_name', 'transitions_per_roi', 'cumulative_time_in_roi_sec',
            'avg_time_in_roi_sec', 'avg_vel_in_roi', 'trial'
        ]]

        df2.to_csv(file, index=False)

    combined_csv = pd.concat([pd.read_csv(f) for f in files])

    if trial_type == 'with_owner':

        sort_by_trial = {
            'No treatment': 0,
            'First Saline': 1,
            'First Urine': 3,
            'Second Saline': 4,
            'Second Urine': 5
        }

    elif trial_type == 'cat_alone':

        sort_by_trial = {
            'Cat alone (1)': 0,
            'Cat alone (2)': 1,
            'Cat alone (3)': 3,
            'Cat alone (4)': 4,
            'Cat alone (5)': 5
        }

    combined_csv = combined_csv.iloc[combined_csv['trial'].map(
        sort_by_trial).argsort()]

    if trial_type == 'with_owner':

        combined_csv.to_csv(output_dir + cat + "_with_owner_rois.csv",
                            index=False,
                            encoding='utf-8-sig')

    elif trial_type == 'cat_alone':

        combined_csv.to_csv(output_dir + cat + "_cat_alone_rois.csv",
                            index=False,
                            encoding='utf-8-sig')

    [os.remove(f) for f in files]
