"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import json


def lazytrim(select_cats, trial_times_json):

    # select_cat is a list ['cat--id']
    # trial_times_json is a json file with trials time

    with open(trial_times_json) as json_file:
        trial_times = json.load(json_file)

    trials = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']

    for i in select_cats:

        d, b = '#' * 20, '#' * len(i)
        print(f'\n\n {d} {b} {d} \n {d} {i} {d} \n {d} {b} {d} \n')

        for j in trials:

            start = trial_times[i][j][0]
            total = trial_times[i][j][1] - trial_times[i][j][0]

            print(f'ffmpeg -ss {start} -i {i}.mp4 -t {total} -y {i}_{j}.mp4 &&')
