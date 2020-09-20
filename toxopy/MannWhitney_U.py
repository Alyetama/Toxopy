"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials, nadlc, roi_behaviors, sniff_instances
from itertools import combinations


class MannWhitney_U:

    def read(csv_file, drop_non_dlc):
        df = pd.read_csv(csv_file)
        excluded_cats, trls = nadlc(), trials()
        if drop_non_dlc is True:
            for c in excluded_cats:
                df.drop(df[df.cat == c].index, inplace=True)
        return df

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


    def time_budget_mw(csv_file, only_sig=False):
        """
        << TIME BUDGET >>
        The time budget of a cat for a trial was determined by summing the times it spent on the individual behaviors assigned to each
        behavioral category (Affiliative, Calm, Exploration/Locomotion,
        and Fear). 
        """
        df = MannWhitney_U.read(csv_file, drop_non_dlc)

        behaviors = ['Exploration/locomotion',
                     'Fear', 'Calm', 'Affiliative']

        def calc_mw(t, b):
            def slct(s, t, b):
                return list(df.loc[(df['infection_status'] == s)
                                   & (df['trial'] == t) &
                                   ((df['Behavior'] == b))]['value'])

            neg, pos = slct('Negative', t, b), slct('Positive', t, b)
            stat, p = mannwhitneyu(neg, pos)
            stat_values = MannWhitney_U.statVal(stat, p)

            if only_sig is False:
                result = MannWhitney_U.alphaTest(p)
                return stat_values, result
            else:
                if p < alpha:
                    result = 'reject H0'
                    return stat_values, result

        for t in trls:
            print(f'{"-" * 60}\n{t}')
            for b in behaviors:
                mw_res = calc_mw(t, b)
                res = f'{b} ==> {mw_res}'
                if mw_res is not None:
                    print(res)


    def latency_mw(csv_file, drop_non_dlc):
        """
        << The Latency Test >>
        Scores on a single behavior “latency to exit the carrier” were
        used to compute results for the latency test. 
        """
        df = MannWhitney_U.read(csv_file, drop_non_dlc)

        def slct(status):
            return list(df.loc[(df['infection_status'] == status)]['t1_latency_to_exit_carrier'])

        neg, pos = slct('Negative'), slct('Positive')
        stat, p = mannwhitneyu(neg, pos)
        stat_values = MannWhitney_U.statVal(stat, p)
        result = MannWhitney_U.alphaTest(p)

        print(f'Latency to exit the carrier ==> {stat_values}, {result}')


    def roi_mw(csv_file):
        """
        << Time Spent in Regions of Interest (ROIs) >>
        Video pixel coordinates for the DeepLabCut-generated labels were
        used to calculate the average time a cat spent near the walls (as opposed to being in the center) in the experimental room. 
        """
        df = MannWhitney_U.read(csv_file)

        vois = roi_behaviors()

        def slct(i, s, j):
            return df.loc[(df['trial'] == i) & (df['infection_status'] == s) & (df['ROI_name'] == j)]

        for j in ['walls', 'middle']:
            print(f'\n{j}')
            for i in trls:
                pos, neg = slct(i, 'Positive', j), slct(i, 'Negative', j)
                print(f'\n{i}')
                for voi in vois:
                    stat, p = mannwhitneyu(neg[voi], pos[voi])
                    print(f'{voi} ==> {MannWhitney_U.statVal(stat, p)}, {MannWhitney_U.alphaTest(p)}')


    def sniff_mw(csv_file, drop_non_dlc):
        """
        << Sniffing Treatment Vial >>
        a single behavior “sniff treatment vial” was used in the “Sniffing Treatment Vial” test. 
        """
        df = MannWhitney_U.read(csv_file, drop_non_dlc)

        sniff_inst = sniff_instances()

        def slct(s, i):
            return list(df.loc[(df['infection_status'] == s)][i])

        for i in sniff_inst:
            neg, pos = slct('Negative', i), slct('Positive', i)
            stat, p = mannwhitneyu(neg, pos)
            stat_values = MannWhitney_U.statVal(stat, p)
            result = MannWhitney_U.alphaTest(p)
            print(f'{i} ==> {stat_values}, {result}')


    def roi_diff_Btrials_Wgroup(csv_file, comparison, trial_type=None, export_csv=False):
        """
        << Time Spent in ROIs – Within-group >>
        Similar to 'roi'. Except it compares time spent in ROI *within* group between trials.
        """
        df = MannWhitney_U.read(csv_file)

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

        trls, vois = trials(), roi_behaviors()

        if comparison == 'all' and trial_type is None:
            raise ValueError('Missing argument: "trial_type"!')
        if comparison == 'split' and trial_type is not None:
            raise ValueError('"split" cannot take a "trial_type" argument')

        if trial_type == 'treatment':
            ombs, r = ttype(trls[::2][1:]), range(0, 6)
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
                    result = MannWhitney_U.alphaTest(p)
                    if export_csv is not True:
                        print(res(' ==> '))
                    else:
                        print(f'{k},', res(','), file=f)

        if export_csv is True:
            f.close()
