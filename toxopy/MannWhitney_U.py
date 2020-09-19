"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials, nadlc


def MannWhitney_U(csv_file, test, drop_non_dlc=True, only_sig=False):

    df = pd.read_csv(csv_file)

    excluded_cats = nadlc()

    trls = trials()

    if drop_non_dlc is True:
        for c in excluded_cats:
            df.drop(df[df.cat == c].index, inplace=True)

    alpha = 0.05

    def statVal(stat, p):
        return 'Statistics=%.3f, p=%.3f' % (stat, p)

    def alphaTest(p):
        if p > alpha:
            result = 'fail to reject H0'
        else:
            result = 'reject H0'
        return result


    if test == 'time_budget':

        def time_budget_mw(csv_file, only_sig):
            """
            << TIME BUDGET >>
            The time budget of a cat for a trial was determined by summing the times
            it spent on the individual behaviors assigned to each behavioral category
            (Affiliative, Calm, Exploration/Locomotion, and Fear). 
            """

            df = pd.read_csv(csv_file)

            excluded_cats = nadlc()

            behaviors = ['Exploration/locomotion',
                         'Fear', 'Calm', 'Affiliative']

            def calc_mw(t, b):
                def slct(s, t, b):
                    return list(df.loc[(df['infection_status'] == s)
                                       & (df['trial'] == t) &
                                       ((df['Behavior'] == b))]['value'])

                neg, pos = slct('Negative', t, b), slct('Positive', t, b)
                stat, p = mannwhitneyu(neg, pos)
                stat_values = statVal(stat, p)

                if only_sig is False:
                    result = alphaTest(p)
                    return stat_values, result

                if only_sig is True:
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

        time_budget_mw(csv_file, only_sig)


    elif test == 'latency':

        def latency_mw(csv_file):
            """
            << The Latency Test >>
            The latency of the cat to exit the carrier, the latency test, was defined
            as the time from when the owner opened the carrier to the time when the
            cat’s entire body was outside of the carrier. Scores on a single behavior
            “latency to exit the carrier” were used to compute results for
            the latency test. 
            """

            def slct(status):
                return list(df.loc[(df['infection_status'] == status)]['t1_latency_to_exit_carrier'])

            neg, pos = slct('Negative'), slct('Positive')
            stat, p = mannwhitneyu(neg, pos)
            stat_values = statVal(stat, p)
            result = alphaTest(p)

            print(f'Latency to exit the carrier ==> {stat_values}, {result}')

        latency_mw(csv_file)


    elif test == 'roi':

        def roi_mw(csv_file, drop_non_dlc=False):
            """
            << Time Spent in Regions of Interest >>
            Video pixel coordinates for the DeepLabCut-generated labels were used to
            he average time a cat spent within 80 pixels (~0.80 meters) of the walls
            (as opposed to being in the center) of the experimental room. 
            """

            df = pd.read_csv(csv_file)

            vois = ["cumulative_time_in_roi_sec",
                    "avg_time_in_roi_sec", "avg_vel_in_roi"]

            def slct(i, s, j):
                return df.loc[(df['trial'] == i) & (df['infection_status'] == s) & (df['ROI_name'] == j)]

            for j in ['walls', 'middle']:
                print(f'\n{j}')

                for i in trls:
                    pos, neg = slct(i, 'Positive', j), slct(i, 'Negative', j)
                    print(f'\n{i}')

                    for voi in vois:
                        stat, p = mannwhitneyu(neg[voi], pos[voi])
                        print(f'{voi} ==> {statVal(stat, p)}, {alphaTest(p)}')

        roi_mw(csv_file)


    elif test == 'sniffing_vial':

        def sniff_mw(csv_file):
            """
            << Sniffing Treatment Vial >>
            a single behavior “sniff treatment vial” was used in
            the “Sniffing Treatment Vial” test. 
            """

            df = pd.read_csv(csv_file)

            behaviors = ['t3_sniffsaline', 't5_sniffurine',
                         't7_sniffsaline', 't9_sniffurine']

            def slct(s, i):
                return list(df.loc[(df['infection_status'] == s)][i])

            for i in behaviors:
                neg. pos = slct('Negative', i), slct('Positive', i)
                stat, p = mannwhitneyu(neg, pos)
                stat_values = statVal(stat, p)
                result = alphaTest(p)
                print(f'{i} ==> {stat_values}, {result}')
