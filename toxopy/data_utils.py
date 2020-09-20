"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import json
from toxopy import trials
from os import remove
from numpy import mean, median
import pandas as pd


# Global variables
var = ['distance', 'vel', 'cat_distance', 'acceleration', 'moving']
tls = trials()


def json2tidycsv(json_file_loc, csv_output=False):
    """
    Converts dlc avgs data from JSON format to a tidy data in csv
    json_file_loc is the path to the json file with all individual avgs data
    """

    with open(json_file_loc) as json_file:
        data = json.load(json_file)

    with open('dlc_avgs_data_tidy.csv', 'w') as f:

        for i in ['positive', 'negative']:
            for c in list(data[i].keys()):
                for x in tls:
                    for z in behaviors:
                        if csv_output is True:
                            print(f'{c},positive,{z},{x},{data[i][c][x][z]}',
                                  file=f)
                        else:
                            print(f'{c},positive,{z},{x},{data[i][c][x][z]}')

        remove('dlc_avgs_data_tidy.csv') if csv_output is False else None


def obtain_grand_m(json_file_loc, output_dir):
    """
    json_file_loc is the path to the json file with all individual avgs data
    output_dir is where you want to dump the .csv file to (optional)
    """

    with open(json_file_loc) as json_file:
        data = json.load(json_file)

    dct = {}

    for i in var:
        dct['p%s' % i] = []
        dct['n%s' % i] = []

    for p, n in zip(list(data['positive'].keys()),
                    list(data['negative'].keys())):

        for t in tls:
            for v, o in zip(var, range(0, 5)):
                if v == var[o]:
                    dct['p' + var[o]].append(data['positive'][p][t][v])
                    dct['n' + var[o]].append(data['negative'][n][t][v])

    for y in ['pdistance', 'ndistance']:
        dct[y] = [i for i in dct[y] if i != "NaN"]

    if output_dir is not None:
        output = f'{output_dir}/grand_avgs_mds.csv'
    else:
        output = 'grand_avgs_mds.csv'

    with open(output, 'w') as f:

        print('infection_status,variable,mean,median', file=f)

        for g in dct:
            for q in ['positive', 'negative']:
                if g.startswith(q[0]):
                    print(f'{q},{g[1:]},{mean(dct[g])},{median(dct[g])}',
                          file=f)


def jsonify_dlc_avgs(csv_file):
    """csv_file is one file with all the experiment data"""

    df = pd.read_csv(csv_file)

    def percentage(part, whole):
        return 100 * float(part) / float(whole)

    cats = df.cat.unique()

    d = {}

    vars2 = ['distance_loess05', 'cat_distance_loess05',
             'velocity_loess05', 'acceleration_loess05']

    for cat in cats:
        df2 = df.loc[(df['cat'] == cat)]
        d[cat] = {}

        for t in tls:
            d[cat][t] = {}
            df3 = df2.loc[(df['trial'] == t)]
            for i, j in zip(var, vars2):
                d[cat][t][i] = mean(df3[j])
            d[cat][t]['moving'] = percentage(sum(df3['moving']), len(df2))

    with open('dlc_avgs.json', 'w') as outfile:
        json.dump(d, outfile)
