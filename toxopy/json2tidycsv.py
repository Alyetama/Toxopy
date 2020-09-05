"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import json
from toxopy import trials
from os import remove


def json2tidycsv(json_file_loc, csv_output=False):

    # Converts dlc avgs data from JSON format to a tidy data in csv
    # json_file_loc is the path to the json file with all individual avgs data

    with open(json_file_loc) as json_file:
        data = json.load(json_file)

    param = ['distance', 'vel', 'cat_distance', 'acceleration', 'moving']

    tls = trials()

    with open('dlc_avgs_data_tidy.csv', 'w') as f:

        for i in ['positive', 'negative']:

            for c in list(data[i].keys()):

                for x in tls:

                    for z in param:

                        if csv_output is True:

                            print(f'{c},positive,{z},{x},{data[i][c][x][z]}',
                                  file=f)

                        else:

                            print(f'{c},positive,{z},{x},{data[i][c][x][z]}')

        remove('dlc_avgs_data_tidy.csv') if csv_output is False else None
