"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from math import sqrt
from numpy import nan
from os import remove
from tqdm import tqdm
from rich.console import Console


def improve_dlc_output(cat, owner):

    console = Console()

    def improve_dlc_csv(csv_file, trial_type):
        """Add time and trial type."""

        df = pd.read_csv(csv_file)
        df = df.iloc[:, :3]

        n = len(df)

        if trial_type == 'owner':
            time = 1020

        elif trial_type == 'cat':
            time = 600

        f = n / time

        indx = []

        for i in range(0, n):
            i = i / f
            indx.append(i)

        result = pd.DataFrame(indx, columns=['time'])

        trials = []

        if trial_type == "owner":

            for i in indx:
                k = 300
                j = 180
                if i < k:
                    trials.append('FT')
                elif k < i < k + j:
                    trials.append('ST1')
                elif k + j < i < k + j * 2:
                    trials.append('UT1')
                elif k + j * 2 < i < k + j * 3:
                    trials.append('ST2')
                elif k + j * 3 < i <= k + j * 4:
                    trials.append('UT2')

        elif trial_type == "cat":
            t = 120
            for i in indx:
                if i < t:
                    trials.append('CA1')
                elif t < i < t * 2:
                    trials.append('CA2')
                elif t * 2 < i < t * 3:
                    trials.append('CA3')
                elif t * 3 < i < t * 4:
                    trials.append('CA4')
                elif t * 4 < i <= t * 5:
                    trials.append('CA5')

        tl = pd.DataFrame(trials, columns=['trial'])

        result = pd.concat([df, result, tl], axis=1)
        result = result.iloc[2:, :]

        result.columns = ['indx', 'x', 'y', 'time', 'trial']

        result.to_csv(csv_file.strip('.csv') + '_improved.csv',
                      index=False,
                      sep=',',
                      encoding='utf-8')

    improve_dlc_csv(cat, trial_type='owner')
    improve_dlc_csv(owner, trial_type='owner')
    """Calculate distance between cat and owner."""

    cat_improved = cat.strip('.csv') + '_improved.csv'
    df_cat = pd.read_csv(cat_improved, sep=",")
    df_cat = pd.DataFrame(df_cat, columns=df_cat.columns)

    owner_improved = owner.strip('.csv') + '_improved.csv'
    df_owner = pd.read_csv(owner_improved, sep=",")
    df_owner = pd.DataFrame(df_owner, columns=df_owner.columns)

    ds = []

    console.print(
        "\nCALCULATING THE DISTANCE BETWEEN CAT AND OWNER", style="bold green")

    for i, j in tqdm(zip(df_cat['indx'], df_owner['indx'])):

        p1 = [df_cat['x'][i], df_cat['y'][i]]
        p2 = [df_owner['x'][j], df_owner['y'][j]]

        distance = sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))

        ds.append(distance)

    ds = pd.DataFrame(ds, columns=['distance'])

    df_cat.rename(columns={'x': 'x_cat', 'y': 'y_cat'}, inplace=True)
    df_owner.rename(columns={'x': 'x_owner', 'y': 'y_owner'}, inplace=True)

    result = pd.concat([
        df_cat[{'indx', 'x_cat', 'y_cat'}],
        df_owner[{'x_owner', 'y_owner', 'time', 'trial'}], ds
    ],
        axis=1)

    result = result[[
        'indx', 'time', 'trial', 'x_cat', 'y_cat', 'x_owner', 'y_owner',
        'distance'
    ]]

    cols = ["x_cat", "y_cat", "x_owner", "y_owner"]

    result[cols] = result[cols].replace({0: nan})
    """Calculate cat traveled distance."""

    def calculateDistance(x1, y1, x2, y2):
        dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    df_cat = df_cat.iloc[:, :4]

    cat_dst = []

    n = len(df_cat)

    i = 0

    console.print("\nCALCULATING THE CAT'S TRAVELED DISTANCE",
                  style="bold green")

    for i in tqdm(range(0, n)):

        x1 = df_cat.iloc[i]['x_cat']
        x2 = df_cat.iloc[i - 1]['x_cat']
        y1 = df_cat.iloc[i]['y_cat']
        y2 = df_cat.iloc[i - 1]['y_cat']

        cat_dst.append(float(calculateDistance(x1, y1, x2, y2)))

    cat_dst[0] = nan

    cat_dst = pd.DataFrame(cat_dst, columns=['cat_distance'])
    """Calculate cat velocity."""

    def calculateVelocity(dist, time):
        return dist / time

    velocity_ls = []

    console.print("\nCALCULATING THE CAT'S VELOCITY", style="bold green")

    for j in tqdm(range(0, n)):

        if j == 0:
            velocity_ls.append(nan)
            continue

        d = cat_dst.iloc[j]['cat_distance']

        # t = df_cat.iloc[j]['time'] - df_cat.iloc[j - 1]['time']

        velocity_ls.append(float(calculateVelocity(d, 0.033)))

    velocity = pd.DataFrame(velocity_ls, columns=['velocity'])
    """Calculate cat movement state."""

    moving = []
    notMoving = []

    console.print("\nESTIMATING THE CAT'S MOVEMENT STATE", style="bold green")

    for z in tqdm(cat_dst['cat_distance']):

        if str(z) == 'nan':
            moving.append(nan)
            notMoving.append(nan)
        elif z >= 0.07:
            moving.append(1)
            notMoving.append(0)
        else:
            moving.append(0)
            notMoving.append(1)

    moving = pd.DataFrame(moving, columns=['moving'])
    notMoving = pd.DataFrame(notMoving, columns=['not_moving'])
    """Calculate cat acceleration."""

    def calculateAcc(vi, vf, ti, tf):
        return (vi - vf) / (ti - tf)

    acc = []

    console.print("\nCALCULATING THE CAT'S ACCELERATION", style="bold green")

    for q in tqdm(range(0, n)):

        velocity['velocity'].astype('float')

        vi = velocity.iloc[q]['velocity'].astype('float')
        vf = velocity.iloc[q - 1]['velocity'].astype('float')
        ti = df_cat.iloc[q]['time']
        tf = df_cat.iloc[q - 1]['time']

        acc.append(float(calculateAcc(vi, vf, ti, tf)))

    acc = pd.DataFrame(acc, columns=['acceleration'])
    """Clean zero values in relevant data,
    then append data to one csv file."""

    df = pd.concat([result, cat_dst, velocity, moving, notMoving, acc], axis=1)

    cols = ['cat_distance', 'velocity', 'acceleration']

    idx = df.index[df['indx']].tolist()

    console.print("\nCLEANING OUTPUT", style="bold green")

    for s, w in tqdm(zip(df['velocity'], idx)):
        if s == 0:
            df = df.drop(w)
        elif s > 100:
            df = df.drop(w)

    df[cols] = df[cols].replace({0: nan})

    [remove(i) for i in [owner_improved, cat_improved]]

    df.to_csv(cat.strip('chwo.csv') + 'improved.csv',
              index=False,
              sep=',',
              encoding='utf-8')

    console.print("\nDONE!", style="bold green")
