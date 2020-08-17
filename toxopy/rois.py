import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from pathlib import Path
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from dlcu import PlottingResults, time_in_each_roi
from collections import namedtuple
import matplotlib.patches as patches



def rois(cat, improved_file):
# Load dataset

    Dataframe = pd.read_csv(improved_file)
    df = Dataframe.dropna()

    # Create variable names

    time = df['time']
    x_cat = df['x_cat_loess']
    y_cat = df['y_cat_loess']
    velocity = df['velocity_loess']

    # Plot velocity

    plt.plot(time, velocity)
    plt.xlabel('Time in seconds')
    plt.ylabel('Speed in pixels per second')
    plt.savefig(cat + '_velocity.png')
    plt.close()

    # Calculate and plot rois


    def rois_gen(i):
        def getList(dict):
            list = []
            for key in dict.keys():
                list.append(key)

            return list

        with open('room_layout.json') as json_file:
            p = json.load(json_file)

        catslist = getList(p)

        positions = ['middle', 'rightside', 'leftside', 'topside', 'bottomside']

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

    positions = ['middle', 'rightside', 'leftside', 'topside', 'bottomside']
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
    plt.savefig(cat + '_rois.png')
    plt.close()

    res = time_in_each_roi.get_timeinrois_stats(bp_tracking.T,
                                                rois,
                                                fps=30,
                                                returndf=True,
                                                check_inroi=True)

    res.to_csv(improved_file[:-4] + '_rois.csv',
              index=False,
              sep=',',
              encoding='utf-8')
