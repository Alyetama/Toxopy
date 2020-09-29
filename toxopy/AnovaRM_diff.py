"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
from statsmodels.stats.anova import AnovaRM


def AnovaRM_diff(csv_file, trls=[], sets=False):
    """
    'csv_file' is either 'vel_diff' or 'time_diff'
    'trls' is user-specified trials that will be used in the comparison,
        leave as empty list if 'sets' is True
    'sets' is an option to compare by sets (['ST1', 'UT1'] vs ['ST2', 'UT2'])
    """

    # 'voi' is the variable of interest: either 'vel_diff' or 'time_diff'
    voi = Path(csv_file).stem[4:]

    df = pd.read_csv(csv_file)
    df = df.groupby(['cat', 'infection_status',
                     'trial'])[voi].mean().reset_index()

    cats = df.cat.unique()

    def slct(j):
        def sub(i):
            return pd.concat(
                [df[(df.trial == x)].reset_index(drop=True) for x in i])

        return pd.concat([sub(x) for x in [j]])

    def checkTlen(n):
        cts = []
        for cat in cats:
            nt = len(list(df[df['cat'] == cat]['trial']))
            if nt != n:
                cts.append(cat)
        return cts

    def ANVtest(df, voi, w):
        return AnovaRM(data=df, depvar=voi, subject='cat', within=[w], aggregate_func='mean').fit()


    if sets is not False:
        # Compare by sets (['ST1', 'UT1'] vs ['ST2', 'UT2'])
        w = 'set'
        s1, s1['set'] = slct(['ST1', 'UT1']), 'first'
        s2, s2['set'] = slct(['ST2', 'UT2']), 'second'
        df = pd.concat([s1, s2])
        return print(ANVtest(df, voi, w))

    else:
        # Compare by a user-specified trials list
        n = len(trls)
        df = slct(trls)
        w = 'trial'
        if checkTlen(n) == []:
            return print(ANVtest(df, voi, w))
        else:
            raise ValueError(
                f'The following cats\'s len(trials) != n:\n{checkTlen(n)}')
