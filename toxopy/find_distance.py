import pandas as pd
import math


def find_distance(cat, owner):

    df_cat = pd.read_csv(cat, sep=",")
    names = df_cat.columns
    df_cat = pd.DataFrame(df_cat, columns=names)

    df_owner = pd.read_csv(owner, sep=",")
    names = df_owner.columns
    df_owner = pd.DataFrame(df_owner, columns=names)

    ds = []

    for i, j in zip(df_cat['indx'], df_owner['indx']):

        p1 = [df_cat['x'][i], df_cat['y'][i]]
        p2 = [df_owner['x'][j], df_owner['y'][j]]
        distance = math.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))
        ds.append(distance)

    ds = pd.DataFrame(ds, columns=['distance'])

    df_cat.rename(columns={'x': 'x_cat', 'y': 'y_cat'}, inplace=True)
    df_owner.rename(columns={'x': 'x_owner', 'y': 'y_owner'}, inplace=True)

    result = pd.concat([
        df_cat[{'indx', 'x_cat', 'y_cat'}],
        df_owner[{'x_owner', 'y_owner', 'time', 'trial'}], ds
    ],
                       axis=1)

    result = result[[
        'indx', 'time', 'trial', 'x_cat', 'y_cat', 'x_owner', 'y_owner',
        'distance'
    ]]

    result.to_csv(cat[:-24] + '_improved.csv',
                  index=False,
                  sep=',',
                  encoding='utf-8')
