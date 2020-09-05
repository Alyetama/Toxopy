"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import pandas as pd
from pathlib import Path
import glob
from toxopy import trials_cap, trials
from os import remove
from tqdm import tqdm


def correct_times(csv_dir, output_dir):
    """'csv_dir' is the path to the folder containing the combined csv files"""

    files = glob.glob(f'{csv_dir}/*.csv')

    tls = trials_cap()

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

                fdf.to_csv(f'{output_dir}/{cat}_{trial}.csv',
                           index=False,
                           encoding='utf-8-sig')

        fs = glob.glob(f'{output_dir}/{cat}_*.csv')

        ccsv = pd.concat([pd.read_csv(i) for i in fs])

        old_names, new_names = trials_cap(), trials()

        ccsv['trial'] = ccsv['trial'].replace(old_names, new_names)

        ccsv = ccsv.sort_values(by=['time'])

        ccsv.to_csv(f'{output_dir}/{cat}.csv',
                    index=False,
                    encoding='utf-8-sig')

        [remove(i) for i in fs]
