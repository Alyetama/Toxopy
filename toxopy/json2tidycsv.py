import json


def json2tidycsv(json_file_loc, csv_output=False):

    # Converts dlc avgs data from JSON format to a tidy data in csv
    #json_file_loc is the path to the json file with all individual avgs data

    with open(json_file_loc) as json_file:
        data = json.load(json_file)

    param = [
        'distance', 'vel', 'cat_distance', 'vel', 'acceleration', 'moving'
    ]

    trials = [
        'no treatment', 'cat alone (1)', 'first saline', 'cat alone (2)',
        'first urine', 'cat alone (3)', 'second saline', 'cat alone (4)',
        'second urine', 'cat alone (5)'
    ]

    with open('dlc_avgs_data_tidy.csv', 'w') as f:

        for i in ['positive', 'negative']:

            for c in list(data[i].keys()):

                for x in trials:

                    for z in param:

                        if csv_output == True:

                            print(c + ',positive,' + z + ',' + x + ',' +
                                  str(data[i][c][x][z]),
                                  file=f)

                        else:

                            print(c + ',positive,' + z + ',' + x + ',' +
                                  str(data[i][c][x][z]))

    f.close()
