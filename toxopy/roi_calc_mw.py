from scipy.stats import mannwhitneyu
import pandas as pd


def roi_calc_mw(data_file, voi):

    filterwarnings("ignore")

    df = pd.read_csv(data_file)

    trial_names = [
        'No treatment', 'Cat alone (1)', 'First Saline', 'Cat alone (2)',
        'First Urine', 'Cat alone (3)', 'Second Saline', 'Cat alone (4)',
        'Second Urine', 'Cat alone (5)'
    ]

    for j in ['walls', 'middle']:

        print('\n', j)

        for i in trial_names:

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
