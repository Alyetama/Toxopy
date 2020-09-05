"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
import glob


def find_tps_velocity_values(csv_dir, tp_dir, output_dir, trial_type):
    """
    'csv_dir' is the directory with the 'improved_dlc' files
    'tp_dir' is the directory with the improved turning points csv files
    'output_dir' is the directory where output files will be save
    """

    def tp_csv_file(cat):
        tp_files_dir = tp_dir + f'/{cat}*.csv'
        fs = glob.glob(tp_files_dir)
        for f in fs:
            return pd.read_csv(f)

    csv_files_dir = csv_dir + '/*.csv'

    files = glob.glob(csv_files_dir)

    for file in files:

        df = pd.read_csv(file)

        if trial_type == 'cat_alone':
            cat = Path(file).stem[:-10]

        elif trial_type == 'with_owner':
            cat = Path(file).stem[:-11]

        df3 = tp_csv_file(cat)

        velocity_value = []

        for i in df3['tppos']:
            velocity_value.append(df['velocity_loess05'][i])

        df3['velocity_value'] = velocity_value

        df3.to_csv(f'{output_dir}/{Path(file).stem}_tps_improved.csv',
                   index=False,
                   encoding='utf-8-sig')
