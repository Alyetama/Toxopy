"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""


def trials_full():

    return [
        'no treatment', 'cat alone (1)', 'first saline', 'cat alone (2)',
        'first urine', 'cat alone (3)', 'second saline', 'cat alone (4)',
        'second urine', 'cat alone (5)'
    ]


def trials_cap():

    return [
        'No treatment', 'Cat alone (1)', 'First Saline', 'Cat alone (2)',
        'First Urine', 'Cat alone (3)', 'Second Saline', 'Cat alone (4)',
        'Second Urine', 'Cat alone (5)'
    ]


def trials():

    return [
        'FT', 'CA1', 'ST1', 'CA2', 'UT1', 'CA3', 'ST2', 'CA4', 'UT2', 'CA5'
    ]


def set_status(cat, df):

    if cat in ['daisy', 'mila', 'marmalade', 'washburne', 'lavoisier']:

        df['infection_status'] = 'Positive'

    else:

        df['infection_status'] = 'Negative'
