"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials, nadlc, roi_behaviors
from itertools import combinations


excluded_cats, trls, vois = nadlc(), trials(), roi_behaviors()


def alphaTest(p):
    alpha = 0.05
    if p > alpha:
        result = 'fail to reject H0'
    else:
        result = 'reject H0'
    return result


def statVal(stat, p):
    res = 'Statistics=%.3f, p=%.3f' % (stat, p)
    return res


def boris_mw(csv_file, include_ns=True, drop_non_dlc=False):
    """
    df is typically "bin_data_grouped_____percentage____tidy" for the time
    budget analysis, and "bin_data_all_behaviors____frequency____tidy" for
    single behavior comparisons.
    """
    df = pd.read_csv(csv_file)
    if drop_non_dlc is True:
        for c in excluded_cats:
            df.drop(df[df.cat == c].index, inplace=True)

    behaviors = list(df.Behavior.unique())

    def statVal(stat, p):
        res = 'Statistics=%.3f, p=%.3f' % (stat, p)
        return res

    def slct(status, trial, behavior):
        return df[(df['infection_status'] == status) & (df['trial'] == trial) & (df['Behavior'] == behavior)]['value']

    for t in trls:
        print(f'\n{"-" * 60}\n{t}\n')

        for b in behaviors:
            neg, pos = slct('Negative', t, b), slct('Positive', t, b)
            if sum(neg) and sum(pos) != 0:
                stat, p = mannwhitneyu(neg, pos)
                stat_values = statVal(stat, p)
                result = alphaTest(p)
                res_str = f'{b} ==> {stat_values}, {result}'
                if result == 'reject H0':
                    print(f'{res_str}  *')
                elif result != 'reject H0' and include_ns is True:
                    print(res_str)


def roi_mw(csv_file):
    """
    << Time Spent in Regions of Interest (ROIs) >>
    Video pixel coordinates for the DeepLabCut-generated labels were
    used to calculate the average time a cat spent near the walls (as opposed to being in the center) in the experimental room. 
    """
    df = pd.read_csv(csv_file)

    def slct(i, s, j):
        return df.loc[(df['trial'] == i) & (df['infection_status'] == s) & (df['ROI_name'] == j)]

    for j in ['walls', 'middle']:
        print(f'\n{j}')
        for i in trls:
            pos, neg = slct(i, 'Positive', j), slct(i, 'Negative', j)
            print(f'\n{i}')
            for voi in vois:
                stat, p = mannwhitneyu(neg[voi], pos[voi])
                print(f'{voi} ==> {statVal(stat, p)}, '
                      + f'{alphaTest(p)}')


def roi_diff_Btrials_Wgroup_mw(csv_file, comparison, trial_type=None, export_csv=False):
    """
    << Time Spent in ROIs – Within-group >>
    Similar to 'roi'. Except it compares time spent in ROI *within* group between trials.
    """
    df = pd.read_csv(csv_file)

    def slct(tr):
        if comparison == 'all':
            return df.loc[(df['ROI_name'] == 'walls')
                          & (df['infection_status'] == k) &
                          (df['trial'] == tr)][b]
        elif comparison == 'split':
            return df.loc[(df['ROI_name'] == 'walls') & (df['infection_status'] == k) & df.trial.isin(tr)][b]

    def res(s):
        if comparison == 'all':
            pt_comp = f'{combs[i][0]} vs {combs[i][1]}'
        elif comparison == 'split':
            pt_comp = '1st-half vs 2nd-half'
        return f'{pt_comp}{s}{stat}{s}{round(p, 4)}{s}{result}'

    def ttype(rng):
        return list(combinations(rng, 2))

    if comparison == 'all' and trial_type is None:
        raise ValueError('Missing argument: "trial_type"!')
    if comparison == 'split' and trial_type is not None:
        raise ValueError('"split" cannot take a "trial_type" argument')

    if trial_type == 'treatment':
        combs, r = ttype(trls[::2][1:]), range(0, 6)
    elif trial_type == 'CA':
        combs, r = ttype(trls[1::2]), range(0, 10)
    else:
        r = range(0, 1)

    if export_csv is True:
        f = open('results.csv', 'w')
        print('status,comparison,stat,p,interpretation', file=f)

    for k in ['Negative', 'Positive']:
        if export_csv is not True:
            print(f'{"-" * 65}\n<< {k} >>')
        for b in vois:
            if export_csv is not True:
                print(f'\n#{b}')
            for i in r:
                if comparison == 'all':
                    c1, c2 = slct(combs[i][0]), slct(combs[i][1])
                elif comparison == 'split':
                    c1, c2 = slct(trls[0:5]), slct(trls[5:10])
                stat, p = mannwhitneyu(c1, c2)
                result = alphaTest(p)
                if export_csv is not True:
                    print(res(' ==> '))
                else:
                    print(f'{k},', res(','), file=f)

    if export_csv is True:
        f.close()
