import json


def lazytrim(trial_times_json):

    def getList(dict):
        list = []
        for key in dict.keys():
            list.append(key)

        return list

    with open(trial_times_json) as json_file:
        trial_times = json.load(json_file)

    catslist = getList(trial_times)

    trials = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']

    for i in catslist:

        d = '#' * 20
        print('\n\n', d, '#' * len(i), d, '\n', d, i, d, '\n', d, '#' * len(i), d,
              '\n')

        for j in trials:

            start = trial_times[i][j][0]
            total = trial_times[i][j][1] - trial_times[i][j][0]
            input_dir = ''
            output_dir = ''
            print('ffmpeg -ss', start, '-i', input_dir + i + '.mp4', '-t', total,
                  '-y', output_dir + i + '_' + j + '.mp4')
            print('&&')
