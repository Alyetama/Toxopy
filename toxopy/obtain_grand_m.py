import json
from numpy import mean, median


def obtain_grand_m(json_file_loc):

    # json_file_loc is the path to the json file with all individual avgs data
    # output_dir is where you want to dump the .csv file to (optional)

    with open(json_file_loc) as json_file:
        data = json.load(json_file)

    var = ['distance', 'cat_distance', 'vel', 'acceleration', 'moving']

    trials = [
        'no treatment', 'cat alone (1)', 'first saline', 'cat alone (2)',
        'first urine', 'cat alone (3)', 'second saline', 'cat alone (4)',
        'second urine', 'cat alone (5)'
    ]

    dct = {}

    for i in var:
        dct['p%s' % i] = []
        dct['n%s' % i] = []

    for p, n in zip(list(data['positive'].keys()),
                    list(data['negative'].keys())):

        for t in trials:

            for v, o in zip(var, range(0, 5)):

                if v == var[o]:
                    dct['p' + var[o]].append(data['positive'][p][t][v])
                    dct['n' + var[o]].append(data['negative'][n][t][v])

    for y in ['pdistance', 'ndistance']:
        dct[y] = [i for i in dct[y] if i != "NaN"]

    with open('grand_avgs_mds.csv', 'w') as f:

        print('infection_status,variable,mean,median', file=f)

        for g in dct:

            for q in ['positive', 'negative']:

                if g.startswith(q[0]):

                    print(q + ',' + g[1:] + ',' + str(mean(dct[g])) + ',' +
                          str(median(dct[g])),
                          file=f)
    f.close()
