"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import os
import json
import numpy as np
from glob import glob
import pandas as pd
from toxopy import fwarnings, trials, concat_csv
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from collections import namedtuple
from dlcu.time_in_each_roi import get_timeinrois_stats as gts
from pathlib import Path
from rich.console import Console
from tqdm import tqdm
from shutil import move
# %matplotlib inline


def analyze_rois(input_dir, room_layout, output_dir, plot=False):

    console = Console()

    files = glob(f'{input_dir}/*.csv')

    for file, it in zip(tqdm(files), range(0, len(files))):

        cat = Path(file).stem

        if it != 0:
            tqdm.status_printer(console.print(
                f'{" " * it * 2}{cat.upper()} :cat2:', style='bold blue'))

        for trial in trials():

            df = pd.read_csv(file)
            df = df.dropna()
            df = df[(df['trial'] == trial)]
            infection_status = df.reset_index()['infection_status'][0]

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

            bpT = np.array((x_cat, y_cat, velocity))

            if plot is True:
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

            res = gts(bpT.T, rois, fps=30, returndf=True, check_inroi=True)

            res['trial'] = trial

            def rT(p):
                return (res['ROI_name'] == p)

            walls = res.loc[rT('right') | rT('left') |
                            rT('top') | rT('bottom')]
            middle = res.loc[res['ROI_name'] == 'middle']

            def sumUP(rpos, name):
                dfx = rpos.sum(axis=0)
                dfx['ROI_name'], dfx['trial'] = name, trial
                dfx['cat'], dfx['infection_status'] = cat, infection_status
                return dfx.T

            dfW, dfM = sumUP(walls, 'walls'), sumUP(middle, 'middle')

            dfF = pd.concat([dfW, dfM], axis=1, sort=False).T

            dfF.to_csv(f'{output_dir}/.{cat}_{trial}_del.csv',
                       index=False,
                       encoding='utf-8')

        files = glob(f'{output_dir}/.*_del.csv')

        for f in files:

            df2 = pd.read_csv(f)

            df2 = df2[[
                'ROI_name', 'transitions_per_roi', 'cumulative_time_in_roi_sec',
                'avg_time_in_roi_sec', 'avg_vel_in_roi', 'trial', 'cat', 'infection_status'
            ]]

            df2.to_csv(f, index=False)

        combined_csv = pd.concat([pd.read_csv(f) for f in files])
        combined_csv.to_csv(f'{output_dir}/{cat}.csv',
                            index=False, encoding='utf-8-sig')

        [os.remove(f) for f in files]

    concat_csv(output_dir, 'rois_all')

    sF = f'{output_dir}/single_files'
    if not os.path.exists(sF):
        os.makedirs(sF)
    else:
        pass
    for fl in glob(f'{output_dir}/*.csv'):
        if 'all' not in fl:
            move(fl, sF)

    console.print('\nDone!', style='bold green')
