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


def analyze_rois(file, room_layout, output_dir):

    if output_dir.endswith('/') == False:

        raise ValueError(
            'Output directory does not end with a trailing slash "/"!')

    # Load dataset

    df = pd.read_csv(file)
    df = df.dropna()

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

    ult_df = pd.DataFrame(data=[])

    # Create variable names

    for trial, trial_name in zip(trials, trials_names):

        time = trial['time']
        x_cat = trial['x_cat_loess']
        y_cat = trial['y_cat_loess']
        velocity = trial['velocity_loess']

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

        res.to_csv(output_dir + cat + trial_name + '_deleteme' + '.csv',
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

    sort_by_trial = {
        'No treatment': 0,
        'First Saline': 1,
        'First Urine': 3,
        'Second Saline': 4,
        'Second Urine': 5
    }

    combined_csv = combined_csv.iloc[combined_csv['trial'].map(
        sort_by_trial).argsort()]


    combined_csv.to_csv(output_dir + cat + "_rois.csv",
                        index=False,
                        encoding='utf-8-sig')


    [os.remove(f) for f in files]
