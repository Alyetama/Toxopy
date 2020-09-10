"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from glob import glob
from scipy.stats import sem
from numpy import mean


def return_sem(directory):
    """Directory is the path to all 'evaluation results' files"""

    def calc_sem():

        files = glob(f'{directory}/*.csv')

        train_err, test_err = [], []

        for file in files:

            df = pd.read_csv(file)

            train_err.append(float(df[' Train error(px)']))
            test_err.append(float(df[' Test error(px)']))

        return [[mean(train_err), mean(test_err)], [sem(train_err), sem(test_err)]]

    def results(i):
        return [round(x, 4) for x in calc_sem()[i]]

    return {'Train Error': {'Mean': results(0)[0], 'S.E.M.': results(1)[0]},
            'Test Error': {'Mean': results(0)[1], 'S.E.M.': results(1)[1]}}
