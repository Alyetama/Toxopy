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


def nadlc():
    return [
        'angel', 'becky', 'ellis', 'lil-spot', 'olive', 'rue', 'snowball',
        'stripe', 'teja', 'zelda', 'zenon', 'zoltan'
    ]


def roi_behaviors():
    return [
        'cumulative_time_in_roi_sec', 'avg_time_in_roi_sec', 'avg_vel_in_roi'
    ]


def sniff_instances():
    return [
        't3_sniffsaline', 't5_sniffurine', 't7_sniffsaline', 't9_sniffurine'
    ]


def combined_behaviors():
    return [
        'cat', 'infection_status', 'time', 'trial', 'x_cat', 'y_cat',
        'cat_distance', 'velocity', 'acceleration', 'moving', 'not_moving',
        'x_cat_loess05', 'y_cat_loess05', 'cat_distance_loess05',
        'velocity_loess05', 'acceleration_loess05'
    ]
