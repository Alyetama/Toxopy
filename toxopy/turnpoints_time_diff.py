"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from scipy.stats import ks_2samp


def turnpoints_time_diff(csv_file, cat):

    # csv_file is typivally "all_turnpoints_with_owner_improved.csv"
    # use the output of this function in ks_2samp(output1, output2)

    df = pd.read_csv(csv_file)

    df = df.loc[(df['cat'] == cat)]

    df = df.reset_index()

    def altElement(a):

        firstispeak = str(df['firstispeak'][0])

        if firstispeak == 'False':
            return a[::2]

        elif firstispeak == 'True':
            return a[1::2]

    ls = df[df['cat'] == cat]['time'].tolist()

    n = len(altElement(ls))

    time_diff = []

    for i in range(0, n):
        if i == n - 1:
            break
        else:
            time_diff.append(altElement(ls)[i + 1] - altElement(ls)[i])

    return [round(x, 4) for x in time_diff]
