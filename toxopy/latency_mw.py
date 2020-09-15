from scipy.stats import mannwhitneyu
import pandas as pd
from toxopy import trials, nadlc


def latency_mw(csv_file, drop_non_dlc=True):
    
    df = pd.read_csv(csv_file)

    excluded_cats = nadlc()
    
    if drop_non_dlc is True:
        for c in excluded_cats:
            df.drop(df[df.cat == c].index, inplace=True)
            
    def slct(status):
        return list(df.loc[(df['infection_status'] == status)]['t1_latency_to_exit_carrier'])

    neg, pos = slct('Negative'), slct('Positive')

    stat, p = mannwhitneyu(neg, pos)
    stat_values = 'Statistics=%.3f, p=%.3f' % (stat, p)
    
    alpha = 0.05
    if p > alpha:
        result = 'fail to reject H0'
    else:
        result = 'reject H0'

    print(f'Latency to exit the carrier ==> {stat_values}, {result}')
