"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import os
from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials, nadlc, roi_behaviors, fwarnings
from itertools import combinations


def alphaTest(p):
    alpha = 0.05
    if p > alpha:
        result = 'fail to reject H0'
    else:
        result = 'reject H0'
    return result


def statVal(stat, p):
    res = 'Statistics=%.2f, p=%.4f' % (stat, p)
    return res


def comparison(compare_by):
    if compare_by == 'infection_status':
        control, test = 'Control', 'Infected'
    elif compare_by == 'indoor_outdoor_status':
        control, test = 'Indoor', 'Indoor-outdoor'

    return control, test


excluded_cats, trls, vois = nadlc(), trials(), roi_behaviors()


def boris_mw(csv_file, include_ns=True, drop_non_dlc=False, export_csv=False, path=os.getcwd(), compare_by='infection_status'):
    """
    df is typically "bin_data_grouped_____percentage____tidy" for the time
    budget analysis, and "bin_data_all_behaviors____frequency____tidy" for
    single behavior comparisons.
    """
    df = pd.read_csv(csv_file)

    control, test = comparison(compare_by)

    if drop_non_dlc is True:
        for c in excluded_cats:
            df.drop(df[df.cat == c].index, inplace=True)

    behaviors = sorted(list(df.Behavior.unique()))

    def slct(status, trial, behavior):
        return df[(df[compare_by] == status) & (df['trial'] == trial) &
                  (df['Behavior'] == behavior)]['value']

    if export_csv is True:
        f = open(f'{path}/results.csv', 'w')
        print('trial,behavior,stat,p,interpretation', file=f)

    for t in trls:
        print(f'\n{"-" * 60}\n{t}\n')

        for b in behaviors:
            neg, pos = slct(control, t, b), slct(test, t, b)

            if sum(neg) and sum(pos) != 0:
                stat, p = mannwhitneyu(neg, pos)
                stat_values = statVal(stat, p)
                result = alphaTest(p)
                res_str = f'{b} ==> {stat_values}, {result}'

                if result == 'reject H0':
                    print(f'{res_str}  *')
                    ast = '*'
                elif result != 'reject H0' and include_ns is True:
                    print(res_str)
                    ast = ''

                if export_csv is True:
                    if t in trls[1::2] and b == 'Affiliative':
                        pass
                    else:
                        print(f'{t},{b},{"%.2f" % stat},{"%.4f" % p}' +
                              f'{ast},{result}', file=f)

    if export_csv is True:
        f.close()


def roi_mw(csv_file, compare_by='infection_status'):
    """
    Time Spent in Regions of Interest (ROIs)
    Video pixel coordinates for the DeepLabCut-generated labels were
    used to calculate the average time a cat spent near the walls
    (as opposed to being in the center) in the experimental room.
    """
    df = pd.read_csv(csv_file)

    control, test = comparison(compare_by)

    def slct(i, s, j):
        return df.loc[(df['trial'] == i) & (df[compare_by] == s) &
                      (df['ROI_name'] == j)]

    for j in ['walls', 'middle']:
        print(f'\n{j}')
        for i in trls:
            pos, neg = slct(i, test, j), slct(i, control, j)
            print(f'\n{i}')
            for voi in vois:
                stat, p = mannwhitneyu(neg[voi], pos[voi])
                print(f'{voi} ==> {statVal(stat, p)}, ' + f'{alphaTest(p)}')


def roi_diff_Btrials_Wgroup_mw(csv_file,
                               comparison,
                               trial_type=None,
                               export_csv=False,
                               compare_by='infection_status'):
    """
    Time Spent in ROIs – Within-group
    Similar to 'roi'. Except it compares time spent in
    ROI *within* group between trials.
    """
    df = pd.read_csv(csv_file)

    control, test = comparison(compare_by)

    def slct(tr):
        if comparison == 'all':
            return df.loc[(df['ROI_name'] == 'walls')
                          & (df[compare_by] == k) &
                          (df['trial'] == tr)][b]
        if comparison == 'split':
            return df.loc[(df['ROI_name'] == 'walls')
                          & (df[compare_by] == k)
                          & df.trial.isin(tr)][b]

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

    for k in [control, test]:
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


def calc_dlc_mw(csv_file, export=False, compare_by='infection_status'):

    df = pd.read_csv(csv_file)

    control, test = comparison(compare_by)

    variables = ['vel', 'distance', 'cat_distance', 'acceleration', 'moving']

    for t in trls:
        with open(t, 'w') as f:
            if export is False:
                print('\nTrial:', t, '\n')
                os.remove(t)
            else:
                print('trial, var, statistics, p', file=f)

            for j in variables:

                def slct(status):
                    return df[(df[compare_by] == status) & (df['trial'] == t) &
                              (df['var'] == j)]['value']

                pv, nv = slct(test), slct(control)
                stat, p = mannwhitneyu(pv, nv)
                alpha = 0.05

                if stat != 0:
                    if export is False:
                        print(f'{j} ==>', statVal(stat, p), alphaTest(p))
                    else:
                        if p > alpha:
                            print(f'{t},{j},{stat},{p}', file=f)
                        elif p < alpha:
                            print(f'{t},{j},{stat},{p}*', file=f)

    if export is True:
        combined_csv = pd.concat([pd.read_csv(f) for f in trls])
        combined_csv.to_csv("mannwhitneyu_stats_results.csv",
                            index=False,
                            encoding='utf-8-sig')

        [os.remove(f) for f in trls]
