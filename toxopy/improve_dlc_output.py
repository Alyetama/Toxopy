import pandas as pd
from csv import reader


def improve_dlc_output(csv_file):

    df = pd.read_csv(csv_file)

    df = df.iloc[:, :3]

    n = len(df)
    time = 1020
    f = n / time

    indx = []

    for i in range(0, n):
        i = i / f
        indx.append(i)

    result = pd.DataFrame(indx, columns=['time'])

    trials = []

    for i in indx:
        if i < 300:
            trials.append('No treatment')
        elif 300 < i < 480:
            trials.append('Saline')
        elif 480 < i < 660:
            trials.append('Urine')
        elif 660 < i < 840:
            trials.append('Saline')
        elif 840 < i <= 1020:
            trials.append('Urine')

    tl = pd.DataFrame(trials, columns=['trial'])

    result = pd.concat([df, result, tl], axis=1)

    result.to_csv(csv_file.strip('.csv') + '_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
