import pandas as pd
import numpy as np


def turning_points(array):
    ''' turning_points(array) -> min_indices, max_indices
    Finds the turning points within an 1D array and returns the indices of the minimum and 
    maximum turning points in two separate lists.
    Adapted from httpts://stackoverflow.com/a/48360671
    '''
    idx_max, idx_min = [[]] * 2
    if (len(array) < 3):
        return idx_min, idx_max

    STATIONARY, MAXIMA, MINIMA = range(3)

    def get_state(i, j):
        if i < j:
            return MAXIMA
        if i > j:
            return MINIMA
        return STATIONARY

    pts = get_state(array[0], array[1])
    start = 1
    for i in range(2, len(array)):
        x = get_state(array[i - 1], array[i])
        if x != STATIONARY:
            if pts != STATIONARY and pts != x:
                if x == MINIMA:
                    idx_max.append((start + i - 1) // 2)
                else:
                    idx_min.append((start + i - 1) // 2)
            start = i
            pts = x
    return idx_min, idx_max


def turning_points_output(csv_file, variable):

    df = pd.read_csv(csv_file)

    i = df[variable]

    i = i.to_numpy()

    return sum(len(x) for x in turning_points(i)), turning_points(i)
