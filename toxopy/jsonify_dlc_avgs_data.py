import pandas as pd
from numpy import mean
import json


def jsonify_dlc_avgs(csv_file):

    # csv_file is a .csv file with all the data from all the experiment trials

    df = pd.read_csv(csv_file)

    def percentage(part, whole):
        return 100 * float(part) / float(whole)

    cats = df.cat.unique()

    trials = [
        'No treatment', 'Cat alone (1)', 'First Saline', 'Cat alone (2)',
        'First Urine', 'Cat alone (3)', 'Second Saline', 'Cat alone (4)',
        'Second Urine', 'Cat alone (5)'
    ]

    d = {}

    for cat in cats:

        df2 = df.loc[(df['cat'] == cat)]
        d[cat] = {}

        for t in trials:
            df3 = df2.loc[(df['trial'] == t)]
            d[cat][t] = {}
            d[cat][t]['distance'] = mean(df3['distance_loess05'])
            d[cat][t]['cat_distance'] = mean(df3['cat_distance_loess05'])
            d[cat][t]['vel'] = mean(df3['velocity_loess05'])
            d[cat][t]['acceleration'] = mean(df3['acceleration_loess05'])
            d[cat][t]['moving'] = percentage(sum(df3['moving']), len(df2))

    with open('dlc_avgs.json', 'w') as outfile:
        json.dump(d, outfile)
