import pandas as pd
from csv import reader


def improve_dlc_output(csv_file, type=None):

    df = pd.read_csv(csv_file)

    df = df.iloc[:, :3]

    n = len(df)

    if type is None:
        print("Please specify type!")

    if type is 'owner':
        time = 1020

    if type is 'cat':
        time = 600

    f = n / time

    indx = []

    for i in range(0, n):
        i = i / f
        indx.append(i)

    result = pd.DataFrame(indx, columns=['time'])

    trials = []

    if type is None:
        print("Please specify type!")

    elif type is "owner":

        for i in indx:
            if i < 300:
                trials.append('No treatment')
            elif 300 < i < 480:
                trials.append('First Saline')
            elif 480 < i < 660:
                trials.append('First Urine')
            elif 660 < i < 840:
                trials.append('Second Saline')
            elif 840 < i <= 1020:
                trials.append('Second Urine')

    elif type is "cat":
        t = 120
        if i < t:
            trials.append('Cat alone (1)')
        elif t < i < t * 2:
            trials.append('Cat alone (2)')
        elif t * 2 < i < t * 3:
            trials.append('Cat alone (3)')
        elif t * 3 < i < t * 4:
            trials.append('Cat alone (4)')
        elif t * 4 < i <= t * 5:
            trials.append('Cat alone (5)')

    tl = pd.DataFrame(trials, columns=['trial'])

    result = pd.concat([df, result, tl], axis=1)

    result = result.iloc[2:, :]

    result.to_csv(csv_file.strip('.csv') + '_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
