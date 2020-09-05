"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from tqdm import tqdm
import glob
from pathlib import Path


def csv2h5(path, head=[1]):
    def toh5(file):
        df = pd.read_csv(file, header=head, index_col=[0])

        return df.to_hdf(Path(file).stem + '.h5',
                         'data',
                         mode='w',
                         format='table')

    if isinstance(path, str):

        csv_files_dir = path + '/*.csv'

        files = glob.glob(csv_files_dir)

        for file in tqdm(files):

            toh5(file)

    elif isinstance(path, list):

        for file in tqdm(path):

            toh5(file)
