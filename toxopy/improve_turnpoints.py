"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
import glob
from toxopy import trials


def improve_turnpoints(csv_dir, output_dir):
    """csv_dir is the initial turnpoints csv files dir"""

    tt = [300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]

    files = glob.glob(f'{csv_dir}/*.csv')

    for file in files:

        df = pd.read_csv(file)

        tls, times, proba = [], [], []

        trls = trials()

        for x in df['tppos']:
            times.append(round(x / 30, 4))
        for y in df['proba']:
            proba.append(format(y, '.8f'))

        df = df.drop(columns=['proba'])

        k, j, t = 300, 180, 120

        for i in times:
            if i < tt[0]:
                tls.append('FT')
            else:
                for q, p in zip(range(0, 10), trls[1:]):
                    if tt[q] < i < tt[q+1]:
                        tls.append(p)

        df['proba'], df['trial'], df['time'] = proba, tls, times

        df.to_csv(f'{output_dir}/{Path(file).stem}_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
