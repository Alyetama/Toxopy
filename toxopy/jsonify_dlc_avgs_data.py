"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from numpy import mean
import json
from toxopy import trials


def jsonify_dlc_avgs(csv_file):
    """csv_file is one file with all the experiment data"""

    df = pd.read_csv(csv_file)

    def percentage(part, whole):
        return 100 * float(part) / float(whole)

    cats = df.cat.unique()

    tls = trials()

    d = {}

    vars1 = ['distance', 'cat_distance', 'vel', 'acceleration']
    vars2 = ['distance_loess05', 'cat_distance_loess05',
             'velocity_loess05', 'acceleration_loess05']

    for cat in cats:

        df2 = df.loc[(df['cat'] == cat)]
        d[cat] = {}

        for t in tls:
            d[cat][t] = {}
            df3 = df2.loc[(df['trial'] == t)]
            for i, j in zip(vars1, vars2):
                d[cat][t][i] = mean(df3[j])
            d[cat][t]['moving'] = percentage(sum(df3['moving']), len(df2))

    with open('dlc_avgs.json', 'w') as outfile:
        json.dump(d, outfile)
