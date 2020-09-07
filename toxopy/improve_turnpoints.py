"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
import glob


def improve_turnpoints(csv_dir, output_dir):
    """csv_dir is the initial turnpoints csv files dir"""

    tt = [300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]

    files = glob.glob(f'{csv_dir}/*.csv')

    for file in files:

        df = pd.read_csv(file)

        tls, times, proba = [], [], []

        for x in df['tppos']:
            times.append(round(x / 30, 4))
        for y in df['proba']:
            proba.append(format(y, '.8f'))

        df = df.drop(columns=['proba'])

        k, j, t = 300, 180, 120

        for i in times:
            if i < tt[0]:
                tls.append('FT')
            elif tt[0] < i < tt[1]:
                tls.append('CA1')
            elif tt[1] < i < tt[2]:
                tls.append('ST1')
            elif tt[2] < i < tt[3]:
                tls.append('CA1')
            elif tt[3] < i < tt[4]:
                tls.append('UT1')
            elif tt[4] < i < tt[5]:
                tls.append('CA3')
            elif tt[5] < i < tt[6]:
                tls.append('ST2')
            elif tt[6] < i < tt[7]:
                tls.append('CA4')
            elif tt[7] < i < tt[8]:
                tls.append('UT2')
            elif tt[8] < i < tt[9]:
                tls.append('CA5')

        df['proba'], df['trial'], df['time'] = proba, tls, times

        df.to_csv(f'{output_dir}/{Path(file).stem}_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
