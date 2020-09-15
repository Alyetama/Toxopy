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

            def slct(status):
                return list(df.loc[(df['infection_status'] == status)]['t1_latency_to_exit_carrier'])

            neg, pos = slct('Negative'), slct('Positive')

            stat, p = mannwhitneyu(neg, pos)
            stat_values = statVal(stat, p)
            result = alphaTest(p)

            print(f'Latency to exit the carrier ==> {stat_values}, {result}')

        latency_mw(csv_file)

    elif test == 'roi':
        def roi_calc_mw(csv_file, drop_non_dlc=False):

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

        roi_calc_mw(csv_file)
