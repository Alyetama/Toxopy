"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from glob import glob
from pathlib import Path
from toxopy import trials_cap, trials
from os import remove
from tqdm import tqdm


def combine_dlc_improved(ca_dir, wo_dir, output_dir):

    def one_cat_one_file(ca_dir, wo_dir, output_dir):
        """
        'ca_dir' is the dir with cat_alone_improved csv files
        'wo_dir' is the dir with with_owner_improved csv files
        """

        cat_alone, with_owner = glob(
            ca_dir + '/*.csv'), glob(wo_dir + '/*.csv')

        for f1, f2 in tqdm(zip(sorted(cat_alone), sorted(with_owner))):

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
                                'time', 'x_cat_loess05', 'y_cat_loess05', 'velocity_loess05', 'acceleration_loess05',
                                'trial'
                            ]) for f in files
            ])

            combined_csv.to_csv(f'{output_dir}/{cat1}.csv',
                                index=False,
                                encoding='utf-8-sig')

    one_cat_one_file(ca_dir, wo_dir, output_dir)

    def correct_times(output_dir, f_output_dir):
        """'csv_dir' is the path to the folder containing the combined csv files"""

        files = glob(f'{output_dir}/*.csv')

        # tls = trials_cap()
        tls = trials()

        trials_times = [300, 420, 600, 720, 900, 1020, 1200, 1320, 1500, 1620]

        additions = [0, 300, 120, 480, 240, 660, 360, 840, 480, 1020]

        for file in tqdm(files):

            df = pd.read_csv(file, header=[0])

            cat = Path(file).stem

            for trial, ttime, ad in zip(tls, trials_times, additions):

                time = df.loc[(df['trial'] == trial)]['time']

                diff = max(time) - min(time)

                if trial == trial and diff > ttime:

                    raise ValueError('Fails!', cat, trial, diff)

                elif trial == trial and diff < ttime:

                    def subdf(variable):

                        return df[df['trial'] == trial][variable]

                    t, v, a, r = subdf('time') + ad, subdf(
                        'velocity_loess05'), subdf('acceleration_loess05'), subdf(
                            'trial')

                    fdf = pd.DataFrame([t, v, a, r]).T

                    fdf.to_csv(f'{f_output_dir}/{cat}_{trial}.csv',
                               index=False,
                               encoding='utf-8-sig')

            fs = glob(f'{f_output_dir}/{cat}_*.csv')

            ccsv = pd.concat([pd.read_csv(i) for i in fs])

            ccsv = ccsv.sort_values(by=['time'])

            ccsv.to_csv(f'{f_output_dir}/{cat}.csv',
                        index=False,
                        encoding='utf-8-sig')

            [remove(i) for i in fs]

    correct_times(output_dir, output_dir)
