"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from glob import glob
from pathlib import Path


def one_cat_one_file(dir1, dir2, output_dir):
    """'dir1' is the dir with cat_alone_improved csv files
        'dir2' is the dir with with_owner_improved csv files"""

    cat_alone, with_owner = glob(dir1 + '/*.csv'), glob(dir2 + '/*.csv')

    for f1, f2 in zip(sorted(cat_alone), sorted(with_owner)):

        cat1, cat2 = Path(f1).stem[:-10], Path(f2).stem[:-11]

        files = []

        if cat1 == cat2:
            files.append(f1)
            files.append(f2)

        else:
            raise ValueError('Something is wrong!')

        combined_csv = pd.concat([
            pd.read_csv(f,
                        usecols=[
                            'time', 'velocity_loess05', 'acceleration_loess05',
                            'trial'
                        ]) for f in files
        ])

        combined_csv.to_csv(f'{output_dir}/{cat1}.csv',
                            index=False,
                            encoding='utf-8-sig')
