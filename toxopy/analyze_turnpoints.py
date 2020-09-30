"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
from glob import glob
import os
import dirtyR
from toxopy import trials, concat_csv, set_status
from platform import platform
from subprocess import Popen
from tqdm import tqdm
from rich.console import Console
from shutil import move


def analyze_turnpoints(improved_dlc_dir, output_dir):
    """
    'improved_dlc_dir' the path to improved_dlc files (timed & combined)
    'output_dir' is the dir in which the output files will be saved
    """

    console = Console()

    def mkD(name):
        return f'{output_dir}/{name}'

    for x in [mkD('plots'), mkD('diff'), mkD('single_files')]:
        if not os.path.exists(x):
            os.makedirs(x)

    dirtyR.turnpoints(improved_dlc_dir, 'velocity_loess05', output_dir)

    while True:

        if 'Darwin' in platform():
            Popen(['open', f'{output_dir}/plot_turnpoints.r'])
        else:
            pass

        ans = input('Done? (y) ')
        if ans.lower() == "y":
            break
        continue

    for x in ['/*.r', '/.*']:
        [
            os.remove(x) for x in glob(f'{output_dir}/{x}')
            if os.path.isfile(x) is True
        ]

    for plot in glob(f'{output_dir}/*.png'):
        move(plot, mkD('plots'))

    def improve_turnpoints(output_dir):
        """
        'output_dir' is the initial turnpoints csv files dir,
        and also the dir in which the output files will be saved
        """

        tt = [300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]

        files = glob(f'{output_dir}/*.csv')

        console.print('\nIMPROVING TURNPOINTS FILES...', style='bold blue')

        for file in tqdm(files):

            df = pd.read_csv(file)

            tls, times, proba = [], [], []

            trls = trials()

            for x in df['tppos']:
                times.append(round(x / 30, 4))
            for y in df['proba']:
                proba.append(format(y, '.8f'))

            df = df.drop(columns=['proba'])

            for i in times:
                if i < tt[0]:
                    tls.append('FT')
                else:
                    for q, p in zip(range(0, 10), trls[1:]):
                        if tt[q] < i < tt[q+1]:
                            tls.append(p)

            df['proba'], df['trial'], df['time'] = proba, tls, times

            df.to_csv(f'{output_dir}/{Path(file).stem}.csv',
                      index=False,
                      sep=',',
                      encoding='utf-8')

    improve_turnpoints(output_dir)

    def find_tps_velocity_values(improved_dlc_dir, output_dir, super_output_dir):
        """
        'improved_dlc_dir' is the directory with the 'improved_dlc' files
        'output_dir' is the directory with the improved turning points csv files
        'super_output_dir' is the directory where output files will be save
        """
        def tp_csv_file(cat):

            fs = glob(f'{output_dir}/{cat}.csv')

            for f in fs:
                return pd.read_csv(f)

        files = glob(f'{improved_dlc_dir}/*.csv')

        console.print('\nFINDING VELOCITY VALUES...', style='bold blue')

        for file in tqdm(files):

            df = pd.read_csv(file)

            cat = Path(file).stem

            df2 = tp_csv_file(cat)

            velocity_value = []

            for i in df2['tppos']:
                velocity_value.append(df['velocity_loess05'][i])

            df2['velocity_value'] = velocity_value

            df2.to_csv(f'{super_output_dir}/{Path(file).stem}.csv',
                       index=False,
                       encoding='utf-8-sig')

    find_tps_velocity_values(improved_dlc_dir, output_dir, output_dir)

    for f in glob(f'{output_dir}/*.csv'):
        move(f, mkD('single_files'))

    diff_output_dir = mkD('diff')

    def find_turnpoints_diff(output_dir_super, diff_output_dir):
        """
        'output_dir_super' is 'turnpoints_super_improved' dir
        'output_dir_diff' is the directory in which the output files will be saved
        """

        console.print('\nFINDING TURNPOINTS DIFFERENCE...', style='bold blue')

        output_dir_super = mkD('single_files')

        for variable in tqdm(['time', 'velocity_value']):

            files = glob(f'{output_dir_super}/*.csv')

            for file in files:

                df = pd.read_csv(file)

                if variable == 'time':
                    firstispeak = str(df['firstispeak'][0])

                cat = Path(file).stem

                def altE(l):
                    if firstispeak == 'False':
                        return l[::2]
                    if firstispeak == 'True':
                        return l[1::2]
                    return None

                ls = df[variable].tolist()

                diff, trial, diff_calc = [], [], []

                if variable == 'time':
                    n = len(altE(ls))

                elif variable == 'velocity_value':
                    n = len(ls[::2])

                for i in range(0, n):

                    if i == n - 1:
                        break
                    if variable == 'time':
                        diff.append(altE(ls)[i + 1] - altE(ls)[i])
                        trial.append(altE(df['trial'].tolist()))
                        diff_calc.append(
                            f'({altE(ls)[i + 1]}) - ({altE(ls)[i]})')

                    elif variable == 'velocity_value':
                        diff.append(ls[1::2][i] - ls[::2][i])
                        tl = df['trial'].tolist()
                        trial.append(tl[::2])
                        diff_calc.append(
                            f'({round(ls[1::2][i], 4)}) - ({round(ls[::2][i], 4)})')

                diff = [round(x, 4) for x in diff]

                df = pd.DataFrame()

                if variable == 'time':
                    df['time_diff'] = diff
                    df['time_diff'] = df['time_diff'].abs()

                elif variable == 'velocity_value':
                    df['vel_diff'] = diff
                    df['vel_diff'] = df['vel_diff'].abs()

                df['cat'] = cat
                set_status(cat, df)
                df['trial'] = trial[0][0:len(diff)]
                df['diff_calc'] = diff_calc

                df = df.reset_index()

                for i, j, z in zip(df['trial'], df['trial'][1:], df['index']):
                    if i != j:
                        df.drop(z, inplace=True)

                df.to_csv(f'{diff_output_dir}/{cat}.csv',
                          index=False, encoding='utf-8-sig')

            if variable == 'velocity_value':
                concat_csv(diff_output_dir, "all_vel_diff")

            elif variable == 'time':
                concat_csv(diff_output_dir, "all_time_diff")

    find_turnpoints_diff(output_dir, diff_output_dir)

    console.print('\nDONE!', style='bold green')
