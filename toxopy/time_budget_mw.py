from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials


def time_budget_mw(csv_file, only_sig=False, drop_non_dlc=True):

    df = pd.read_csv(csv_file)
    
    exc_cats = ['angel', 'becky', 'ellis', 'lil-spot', 'olive', 'rue', 'snowball', 'stripe', 'teja', 'zelda', 'zenon', 'zoltan']
        
    if drop_non_dlc == True:
        for c in exc_cats:
            df.drop(df[df.cat == c].index, inplace=True)
    

    behaviors = ['Exploration/locomotion', 'Fear', 'Calm', 'Affiliative']
    trls = trials()
    

    def mw(t, b):
        def slct(s, t, b):
            return list(df.loc[(df['infection_status'] == s)
                               & (df['trial'] == t) &
                               ((df['Behavior'] == b))]['value'])

        neg, pos = slct('Negative', t, b), slct('Positive', t, b)

        stat, p = mannwhitneyu(neg, pos)
        stat_values = 'Statistics=%.3f, p=%.3f' % (stat, p)
        alpha = 0.05

        if only_sig is False:
            if p > alpha:
                result = 'fail to reject H0'
            else:
                result = 'reject H0'
            return stat_values, result

        if only_sig is True:
            if p < alpha:
                result = 'reject H0'
                return stat_values, result

    for t in trls:
        print(f'{"-" * 60}\n{t}\n')

        for b in behaviors:
            mw_res = mw(t, b)
            res = f'{b} ==> {mw_res}'

            if mw_res is not None:
                print(res)
