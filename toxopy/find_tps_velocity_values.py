"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
import glob


def find_tps_velocity_values(csv_dir, tp_dir, output_dir):
    """
    'csv_dir' is the directory with the 'improved_dlc' files
    'tp_dir' is the directory with the improved turning points csv files
    'output_dir' is the directory where output files will be save
    """
    def tp_csv_file(cat):

        fs = glob.glob(f'{tp_dir}/{cat}_turnpoints_improved.csv')

        for f in fs:
            return pd.read_csv(f)


    files = glob.glob(f'{csv_dir}/*.csv')

    for file in files:

        df = pd.read_csv(file)

        cat = Path(file).stem

        df3 = tp_csv_file(cat)

        velocity_value = []

        for i in df3['tppos']:
            velocity_value.append(df['velocity_loess05'][i])

        df3['velocity_value'] = velocity_value

        df3.to_csv(f'{output_dir}/{Path(file).stem}_tps_improved.csv',
                   index=False,
                   encoding='utf-8-sig')
