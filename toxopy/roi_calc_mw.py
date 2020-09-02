"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials


def roi_calc_mw(data_file, voi):

    filterwarnings("ignore")

    df = pd.read_csv(data_file)

    tls = trials()

    for j in ['walls', 'middle']:

        print('\n', j)

        for i in tls:

            positive = df.loc[(df['trial'] == i)
                              & (df['infection_status'] == 'Positive') &
                              (df['ROI_name'] == j)]
            negative = df.loc[(df['trial'] == i)
                              & (df['infection_status'] == 'Negative') &
                              (df['ROI_name'] == j)]

            print('\n', i)

            # compare samples
            stat, p = mannwhitneyu(negative[voi], positive[voi])
            print('Statistics=%.3f, p=%.3f' % (stat, p))

            # interpret
            alpha = 0.05
            if p > alpha:
                print('Same distribution (fail to reject H0)')
            else:
                print('Different distribution (reject H0)')
