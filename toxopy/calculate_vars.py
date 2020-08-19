import pandas as pd
from math import sqrt
from numpy import nan



def calculateDistance(x1, y1, x2, y2):
    dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


df_cat = pd.read_csv(csv_file, sep=",")

names = df_cat.columns

df_cat = pd.DataFrame(df_cat, columns=names)

df_cat = df_cat.iloc[:, :4]

cat_dst = []

n = len(df_cat)

i = 0

for i in range(0, n):

    x1 = df_cat.iloc[i]['x']
    x2 = df_cat.iloc[i - 1]['x']
    y1 = df_cat.iloc[i]['y']
    y2 = df_cat.iloc[i - 1]['y']

    cat_dst.append(float(calculateDistance(x1, y1, x2, y2)))

cat_dst[0] = nan

cat_dst = pd.DataFrame(cat_dst, columns=['cat_distance'])


def calculateVelocity(dist, time):
    return dist / time


velocity = []

for j in range(0, n):

    if j == 0:
        velocity.append(nan)
        continue

    d = cat_dst.iloc[j]['cat_distance']

    t = df_cat.iloc[j]['time'] - df_cat.iloc[j - 1]['time']

    velocity.append(float(calculateVelocity(d, 0.033)))

velocity = pd.DataFrame(velocity, columns=['velocity'])

moving = []
notMoving = []

for z in cat_dst['cat_distance']:

    if str(z) == 'nan':
        moving.append(nan)
        notMoving.append(nan)
    elif z >= 0.07:
        moving.append(1)
        notMoving.append(0)
    else:
        moving.append(0)
        notMoving.append(1)

moving = pd.DataFrame(moving, columns=['moving'])
notMoving = pd.DataFrame(notMoving, columns=['not_moving'])


def calculateAcc(vi, vf, ti, tf):
    return (vi - vf) / (ti - tf)


acc = []

for q in range(0, n):

    velocity['velocity'].astype('float')

    vi = velocity.iloc[q]['velocity'].astype('float')
    vf = velocity.iloc[q - 1]['velocity'].astype('float')
    ti = df_cat.iloc[q]['time']
    tf = df_cat.iloc[q - 1]['time']

    acc.append(float(calculateAcc(vi, vf, ti, tf)))

acc = pd.DataFrame(acc, columns=['acceleration'])

df = pd.concat([df_cat, cat_dst, velocity, moving, notMoving, acc], axis=1)

print(df)
