import pandas as pd
from math import sqrt
from numpy import nan
import os
from tqdm import tqdm
from pathlib import Path
"""Add time and trial type."""


def improve_dlc_output_cat_alone(cat, output_dir):

    if output_dir.endswith('/') == False:

        raise ValueError(
            'Output directory does not end with a trailing slash "/"!')


    def improve_dlc_csv(csv_file):


        df = pd.read_csv(csv_file)
        df = df.iloc[:, :3]

        n = len(df)

        time = 600

        f = n / time

        indx = []

        for i in range(0, n):
            i = i / f
            indx.append(i)

        result = pd.DataFrame(indx, columns=['time'])

        trials = []

        t = 120
        for i in indx:
            if i < t:
                trials.append('Cat alone (1)')
            elif t < i < t * 2:
                trials.append('Cat alone (2)')
            elif t * 2 < i < t * 3:
                trials.append('Cat alone (3)')
            elif t * 3 < i < t * 4:
                trials.append('Cat alone (4)')
            elif t * 4 < i <= t * 5:
                trials.append('Cat alone (5)')

        tl = pd.DataFrame(trials, columns=['trial'])

        result = pd.concat([df, result, tl], axis=1)
        result = result.iloc[2:, :]

        result.columns = ['indx', 'x', 'y', 'time', 'trial']

        result.to_csv(csv_file.strip('.csv') + '_init_improved.csv',
                      index=False,
                      sep=',',
                      encoding='utf-8')


    improve_dlc_csv(cat)
    """Create dataframes for each file type."""

    cat_file_name = Path(cat).stem

    cat_improved = cat_file_name + '_init_improved.csv'

    df_cat = pd.read_csv(cat[:-4] + '_init_improved.csv', sep=",")
    df_cat = pd.DataFrame(df_cat, columns=df_cat.columns)

    tls = pd.DataFrame(df_cat, columns=['trial'])


    """Calculate cat traveled distance."""

    def calculateDistance(x1, y1, x2, y2):
        dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    df_cat = df_cat.iloc[:, :4]

    cat_dst = []

    n = len(df_cat)

    print("\nCALCULATING THE CAT'S TRAVELED DISTANCE")

    for i in tqdm(range(0, n)):

        x1 = df_cat.iloc[i]['x']
        x2 = df_cat.iloc[i - 1]['x']
        y1 = df_cat.iloc[i]['y']
        y2 = df_cat.iloc[i - 1]['y']

        cat_dst.append(float(calculateDistance(x1, y1, x2, y2)))

    cat_dst[0] = nan

    cat_dst = pd.DataFrame(cat_dst, columns=['cat_distance'])
    """Calculate cat velocity."""

    def calculateVelocity(dist, time):
        return dist / time

    velocity_ls = []

    print("\nCALCULATING THE CAT'S VELOCITY")

    for j in tqdm(range(0, n)):

        if j == 0:
            velocity_ls.append(nan)
            continue

        d = cat_dst.iloc[j]['cat_distance']

        t = df_cat.iloc[j]['time'] - df_cat.iloc[j - 1]['time']

        velocity_ls.append(float(calculateVelocity(d, 0.033)))

    velocity = pd.DataFrame(velocity_ls, columns=['velocity'])
    """Calculate cat movement state."""

    moving = []
    notMoving = []

    print("\nESTIMATING THE CAT'S MOVEMENT STATE")

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

    print("\nCALCULATING THE CAT'S ACCELERATION")

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

    df = pd.concat([df_cat, tls, cat_dst, velocity, moving, notMoving, acc], axis=1)

    cols = ['cat_distance', 'velocity', 'acceleration']

    idx = df.index[df['indx']].tolist()

    print("\nCLEANING OUTPUT")

    for s, w in tqdm(zip(df['velocity'], idx)):
        if s == 0:
            df = df.drop(w)
        elif s > 100:
            df = df.drop(w)

    df[cols] = df[cols].replace({0: nan})


    df.to_csv(output_dir + Path(cat).stem + '_improved.csv',
              index=False,
              sep=',',
              encoding='utf-8')


    os.remove(cat[:-4] + '_init_improved.csv')

    print("\nDONE!")
