"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path


def improve_dlc_csv(csv_file, trial_type):

    df = pd.read_csv(csv_file)

    df = df.iloc[:, :3]

    n = len(df)

    if trial_type == 'owner':
        time = 1020

    elif trial_type == 'cat':
        time = 600

    f = n / time

    indx, trials = [], []

    for i in range(0, n):
        i = i / f
        indx.append(i)

    result = pd.DataFrame(indx, columns=['time'])

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

    result.to_csv(f'{Path(csv_file).stem}_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
