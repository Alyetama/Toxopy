"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from toxopy import trials, fwarnings
import pandas as pd
from scipy.stats import mannwhitneyu
from os import remove


def calc_dlc_mw(csv_file, export=False):

    df = pd.read_csv(csv_file)

    tls = trials()

    variables = ['vel', 'distance', 'cat_distance', 'acceleration', 'moving']

    for t in tls:

        with open(t, 'w') as f:

            if export is False:

                print('\nTrial:', t, '\n')

                remove(t)

            else:
                print('trial, var, statistics, p', file=f)

            for j in variables:

                pv = df[(df['status'] == 'Positive') & (df['trial'] == t) &
                        (df['var'] == j)]['value']

                nv = df[(df['status'] == 'Negative') & (df['trial'] == t) &
                        (df['var'] == j)]['value']

                stat, p = mannwhitneyu(pv, nv)

                if stat != 0:

                    alpha = 0.05

                    if export is False:

                        print(j, '\nStatistics=%.3f, p=%.3f' % (stat, p))

                        if p > alpha:

                            print('Same distribution (fail to reject H0)\n')
                        elif p < alpha:
                            print('Different distribution (reject H0)\n')

                    else:

                        if p > alpha:

                            print(f'{t},{j},{stat},{p}', file=f)

                        elif p < alpha:
                            print(f'{t},{j},{stat},{p},*', file=f)

    if export is True:

        combined_csv = pd.concat([pd.read_csv(f) for f in tls])

        combined_csv.to_csv("mannwhitneyu_stats_results.csv",
                            index=False,
                            encoding='utf-8-sig')

        [remove(f) for f in tls]
