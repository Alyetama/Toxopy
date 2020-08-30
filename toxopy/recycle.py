import warnings

def fwarnings():

    return warnings.filterwarnings("ignore")


def trials():

    return [
        'no treatment', 'cat alone (1)', 'first saline', 'cat alone (2)',
        'first urine', 'cat alone (3)', 'second saline', 'cat alone (4)',
        'second urine', 'cat alone (5)'
    ]

def trials_abv():
    
    return ['FT', 'CA1', 'ST1', 'CA2', 'UT1', 'CA3', 'ST2', 'CA4', 'UT2', 'CA5']