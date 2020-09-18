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
        return df.to_hdf(f'{Path(file).stem}.h5',
                         'data',
                         mode='w',
                         format='table')

    if isinstance(path, str):
        files = glob.glob(f'{path}/*.csv')
        for file in tqdm(files):
            toh5(file)

    elif isinstance(path, list):
        for file in tqdm(path):
            toh5(file)


def concat_csv(directory, output_file_name):

    files = glob.glob(directory + '/*.csv')

    combined_csv = pd.concat([pd.read_csv(f) for f in files])
    combined_csv.to_csv(f'{directory}/{output_file_name}.csv',
                        index=False,
                        encoding='utf-8-sig')
