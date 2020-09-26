"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import os
import toxopy
import pandas as pd
from math import sqrt
from numpy import nan
from tqdm import tqdm
from rich.console import Console
from pathlib import Path
from glob import glob
from dirtyR import smooth
from shutil import move
from subprocess import Popen
from platform import platform


def improve_dlc_output(inDIR, outDIR, only_improve_csv=False):
    """
    inDIR is the directory with the original csv files
    outDIR is the output directory
    """

    console = Console()
    trls = toxopy.trials()

    def gg(i):
        return sorted(glob(inDIR + f'/*_{i}.csv'))

    chwo, oh, ch = gg('chwo'), gg('oh'), gg('ch')

    if len(chwo) != len(oh) != len(ch):
        raise ValueError('Some data are missing!')

    for cat_head, owner_hand, cat_alone in zip(chwo, oh, ch):

        cat = Path(cat_head).stem[:-5]

        console.print(f'\nCAT ==> {cat.upper()} :cat2:', style='bold red')

        def improve_dlc_csv(csv_file, trial_type, file_name):
            """Add time and trial type."""

            df = pd.read_csv(csv_file)

            df = df.iloc[2:, :3]

            if trial_type == 'owner':
                time = 1020
            elif trial_type == 'cat':
                time = 600

            f = len(df) / time

            time, tls = [], []

            for i in range(0, len(df)):
                time.append(i / f)

            tt = [180, 480, 660, 840, 1020]

            if trial_type == "owner":
                for i in time:
                    if i < 300:
                        tls.append('FT')
                    else:
                        for q, p in zip(range(0, 4), trls[2:][::2]):
                            if tt[q] <= i < tt[q + 1]:
                                tls.append(p)

            elif trial_type == "cat":
                t = 120
                for i in time:
                    if i < t:
                        tls.append('CA1')
                    else:
                        for q, p in zip(range(2, 6), trls[2:][1::2]):
                            if t * (q - 1) <= i < t * q:
                                tls.append(p)

            df['time'], df['trial'] = time, tls

            df.columns = ['indx', 'x', 'y', 'time', 'trial']

            df.to_csv(file_name, index=False, encoding='utf-8')

        for i, j in zip([cat_head, owner_hand, cat_alone],
                        ['owner', 'owner', 'cat']):
            file_name = f'{outDIR}/{Path(i).stem}_improved.csv'
            improve_dlc_csv(i, trial_type=j, file_name=file_name)

        if only_improve_csv is True:
            return None
        """Calculate the distance between cat and owner."""

        def dt(file_name):
            improved = f'{outDIR}/{Path(file_name).stem}_improved.csv'
            improved = pd.read_csv(improved, sep=",")
            return pd.DataFrame(improved, columns=improved.columns)

        df_cat, df_owner, df_CA = dt(cat_head), dt(owner_hand), dt(cat_alone)

        df_CA.rename(columns={'x': 'x_cat', 'y': 'y_cat'}, inplace=True)

        tls = df_CA['trial']

        ds = []

        console.print("\nCALCULATING THE DISTANCE BETWEEN CAT AND OWNER",
                      style="bold green")

        for i, j in tqdm(zip(df_cat['indx'], df_owner['indx'])):

            p1 = [df_cat['x'][i], df_cat['y'][i]]
            p2 = [df_owner['x'][j], df_owner['y'][j]]

            distance = sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))

            ds.append(distance)

        df_cat['distance'] = ds

        def renameCols(i, j):
            i.rename(columns={'x': f'x_{j}', 'y': f'y_{j}'}, inplace=True)

        renameCols(df_cat, 'cat'), renameCols(df_owner, 'owner')

        result = pd.concat([
            df_cat[{'indx', 'x_cat', 'y_cat', 'distance'}],
            df_owner[{'x_owner', 'y_owner', 'time', 'trial'}]
        ],
            axis=1)

        result = result[[
            'indx', 'time', 'trial', 'x_cat', 'y_cat', 'x_owner', 'y_owner',
            'distance'
        ]]

        cols = ["x_cat", "y_cat", "x_owner", "y_owner"]

        result[cols] = result[cols].replace({0: nan})

        dfs, dfs_names = [df_cat, df_CA], ['WO', 'CA']

        for df_alt, name in zip(dfs, dfs_names):

            if name == 'WO':
                console.print("\nW/ OWNER TRIALS", style="bold blue")

            elif name == 'CA':
                console.print("\nCAT ALONE TRIALS", style="bold blue")
            """Calculate the cat's traveled distance."""
            def calculateDistance(x1, y1, x2, y2):
                dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                return dist

            df_alt = df_alt.iloc[:, :4]

            cat_dst = []

            console.print("\nCALCULATING THE CAT'S TRAVELED DISTANCE",
                          style="bold green")

            def p(k, e):
                return df_alt.iloc[i - k][e]

            for i in tqdm(range(0, len(df_alt))):

                x1, x2 = p(0, 'x_cat'), p(1, 'x_cat')
                y1, y2 = p(0, 'y_cat'), p(1, 'y_cat')

                cat_dst.append(float(calculateDistance(x1, y1, x2, y2)))

            cat_dst[0] = nan

            fdf = pd.DataFrame(cat_dst, columns=['cat_distance'])
            """Calculate cat velocity."""

            def calculateVelocity(dist, time):
                return dist / time

            velocity_ls = []

            console.print("\nCALCULATING THE CAT'S VELOCITY",
                          style="bold green")

            for j in tqdm(range(0, len(df_alt))):

                if j == 0:
                    velocity_ls.append(nan)
                    continue

                d = cat_dst[j]

                velocity_ls.append(float(calculateVelocity(d, 0.033)))

            fdf['velocity'] = velocity_ls
            """Calculate the cat's movement state."""

            moving, notMoving = [], []

            console.print("\nESTIMATING THE CAT'S MOVEMENT STATE",
                          style="bold green")

            for z in tqdm(cat_dst):

                if str(z) == 'nan':
                    moving.append(nan)
                    notMoving.append(nan)
                elif z >= 0.07:
                    moving.append(1)
                    notMoving.append(0)
                else:
                    moving.append(0)
                    notMoving.append(1)

            fdf['moving'], fdf['not_moving'] = moving, notMoving
            """Calculate cat acceleration."""

            def calculateAcc(vi, vf, ti, tf):
                return (vi - vf) / (ti - tf)

            acc = []

            console.print("\nCALCULATING THE CAT'S ACCELERATION",
                          style="bold green")

            for q in tqdm(range(0, len(df_alt))):

                def a(u, v, d):
                    return d.iloc[q - u][v].astype('float')

                vi, vf = a(0, 'velocity', fdf), a(1, 'velocity', fdf)
                ti, tf = a(0, 'time', df_alt), a(1, 'time', df_alt)

                acc.append(float(calculateAcc(vi, vf, ti, tf)))

            fdf['acceleration'] = acc
            """Clean data."""

            if name == 'WO':
                df = pd.concat([result, fdf], axis=1)

            elif name == 'CA':
                df = pd.concat([df_CA, tls, fdf], axis=1)

            cols = ['cat_distance', 'velocity', 'acceleration']

            idx = df['indx'].tolist()

            console.print("\nCLEANING OUTPUT", style="bold green")

            for s, w in tqdm(zip(df['velocity'], idx)):
                if s > 100:
                    df = df.drop(w)

            df['cat'] = cat

            df = df.dropna()

            df.to_csv(f'{outDIR}/{cat}_{name}_improved.csv',
                      index=False,
                      encoding='utf-8')

        for i in ['ch', 'oh', 'chwo']:
            tbrm = glob(f'{outDIR}/*_{i}_improved.csv')
            [os.remove(x) for x in tbrm]

    for x in ['CA', 'WO']:
        op = f'{outDIR}/{x}'

        if not os.path.exists(op):
            os.makedirs(op)
        else:
            pass

        for file in glob(f'{outDIR}/*_{x}_*.csv'):
            move(file, op)

    ca_dir, wo_dir = f'{outDIR}/CA', f'{outDIR}/WO'

    smooth(ca_dir, wo_dir, outDIR)

    while True:

        if 'Darwin' in platform():
            p = Popen(['open', f'{outDIR}/smooth.r'])
        else:
            pass

        ans = input('Done smoothing? (y) ')
        if ans.lower() == "y":
            break
        continue

    for x in ['/*', '/.*']:
        [
            os.remove(x) for x in glob(f'{outDIR}/{x}')
            if os.path.isfile(x) is True
        ]

    def one_cat_one_file(ca_dir, wo_dir, outDIR):
        """
        'ca_dir' is the dir with cat_alone_improved csv files
        'wo_dir' is the dir with with_owner_improved csv files
        """

        cat_alone, with_owner = glob(f'{ca_dir}/*.csv'), glob(
            f'{wo_dir}/*.csv')

        console.print('\nCONCATENATING FILES...', style='bold blue')

        for f1, f2 in tqdm(zip(sorted(cat_alone), sorted(with_owner))):

            cat1, cat2 = Path(f1).stem[:-12], Path(f2).stem[:-12]
            files = []
            if cat1 == cat2:
                files.append(f1), files.append(f2)
            else:
                raise ValueError(f'Cannot find all required files for {cat1}!')

            combined_csv = pd.concat([pd.read_csv(f) for f in files])

            combined_csv.to_csv(f'{outDIR}/{cat1}.csv',
                                index=False,
                                encoding='utf-8-sig')

    one_cat_one_file(ca_dir, wo_dir, outDIR)

    def correct_times(outDIR):
        """'csv_dir' is the path to the folder containing the combined csv files"""

        files = glob(f'{outDIR}/*.csv')

        trials_times = [300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]
        additions = [0, 300, 120, 480, 240, 660, 360, 840, 480, 1020]

        console.print('\nCORRECTING TRIALS TIME...', style='bold blue')

        for file in tqdm(files):

            df = pd.read_csv(file, header=[0])

            cat = Path(file).stem

            for trial, ttime, ad in zip(trls, trials_times, additions):

                time = df.loc[(df['trial'] == trial)]['time']

                diff = max(time) - min(time)

                if diff > ttime:
                    raise ValueError(
                        f'Cannot correct time! Check {cat} data'
                        f' in {trial} (diff value: {diff})'
                    )

                if diff < ttime:

                    fdf = pd.DataFrame(df[df['trial'] == trial])

                    fdf['time'] = df[df['trial'] == trial]['time'] + ad

                    fdf.to_csv(f'{outDIR}/.{cat}_{trial}.csv',
                               index=False,
                               encoding='utf-8-sig')

            fs = glob(f'{outDIR}/.{cat}_*.csv')

            ccsv = pd.concat([pd.read_csv(i) for i in fs])
            ccsv = ccsv.sort_values(by=['time'])

            toxopy.set_status(cat, ccsv)
            ccsv = ccsv[toxopy.combined_behaviors()]

            ccsv.to_csv(f'{outDIR}/{cat}.csv',
                        index=False,
                        encoding='utf-8-sig')

            [os.remove(i) for i in fs]

    correct_times(outDIR)

    cp = f'{outDIR}/combined'
    if not os.path.exists(cp):
        os.makedirs(cp)
    for fi in glob(f'{outDIR}/*.csv'):
        move(fi, cp)

    console.print('\nDONE!', style='bold green')
