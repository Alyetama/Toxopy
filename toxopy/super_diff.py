"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from toxopy import trials, concat_csv, set_status
import glob
from pathlib import Path


def super_diff(csv_dir, variable, output_dir):
    """
    'csv_dir' is 'turnpoints_super_improved' dir
    'variable' can either take 'time_diff' or 'velocity_value'
    """

    files = glob.glob(f'{csv_dir}/*.csv')

    tls = trials()

    for file in files:

        df = pd.read_csv(file)

        if variable == 'time_diff':
            firstispeak = str(df['firstispeak'][0])

        cat = Path(file).stem[:-13]

        def altE(l):
            if firstispeak == 'False':
                return l[::2]

            elif firstispeak == 'True':
                return l[1::2]

        ls = df[variable].tolist()

        diff, trial, diff_calc = [], [], []

        if variable == 'time_diff':
            n = len(altE(ls))

        elif variable == 'velocity_value':
            n = len(ls[::2])

        for i in range(0, n):

            if i == n - 1:
                break

            else:
                if variable == 'time_diff':
                    diff.append(altE(ls)[i + 1] - altE(ls)[i])
                    trial.append(altE(df['trial'].tolist()))
                    diff_calc.append(f'({altE(ls)[i + 1]}) - ({altE(ls)[i]})')

                elif variable == 'velocity_value':
                    diff.append(ls[1::2][i] - ls[::2][i])
                    tl = df['trial'].tolist()
                    trial.append(tl[::2])
                    diff_calc.append(
                        f'({round(ls[1::2][i], 4)}) - ({round(ls[::2][i], 4)})')

        diff = [round(x, 4) for x in diff]

        df = pd.DataFrame()

        if variable == 'time_diff':
            df['time_diff'] = diff
            df['time_diff'] = df['time_diff'].abs()

        elif variable == 'velocity_value':
            df['vel_diff'] = diff
            df['vel_diff'] = df['vel_diff'].abs()

        df['cat'] = ca
        set_status(cat, df)
        df['trial'] = trial[0][0:len(diff)]
        df['diff_calc'] = diff_calc

        df = df.reset_index()

        for i, j, z in zip(df['trial'], df['trial'][1:], df['index']):
            if i != j:
                df.drop(z, inplace=True)

        df.to_csv(f'{output_dir}/{cat}.csv', index=False, encoding='utf-8-sig')

    if variable == 'velocity_value':
        concat_csv(output_dir, "all_vel_super_diff")

    elif variable == 'time_diff':
        concat_csv(output_dir, "all_time_super_diff")
