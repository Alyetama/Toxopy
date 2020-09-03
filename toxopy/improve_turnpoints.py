"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path


def improve_turnpoints(csv_file, trial_type, output_dir):

    df = pd.read_csv(csv_file)

    tls, times, proba = [], [], []

    for x in df['tppos']: times.append(round(x / 30, 4))
    for y in df['proba']: proba.append(format(y, '.8f'))

    df = df.drop(columns=['proba'])

    k, j, t = 300, 180, 120

    if trial_type == "with_owner":
        for i in times:
            if i < k: tls.append('FT')
            elif k < i < k + j: tls.append('ST1')
            elif k + j < i < k + j * 2: tls.append('UT1')
            elif k + j * 2 < i < k + j * 3: tls.append('ST2')
            elif k + j * 3 < i <= k + j * 4: tls.append('UT2')

    elif trial_type == "cat_alone":
        for i in times:
            if i < t: tls.append('CA1')
            elif t < i < t * 2: tls.append('CA2')
            elif t * 2 < i < t * 3: tls.append('CA3')
            elif t * 3 < i < t * 4: tls.append('CA4')
            elif t * 4 < i <= t * 5: tls.append('CA5')


    df['proba'], df['trial'], df['time'] = proba, tls, times

    df.to_csv(f'{output_dir}/{Path(csv_file).stem}_improved.csv',
              index=False,
              sep=',',
              encoding='utf-8')
