import pandas as pd
import csv
import glob
from pathlib import Path


def concat_rois(directory, output_dir, trial_type):

    if output_dir.endswith('/') == False:

        raise ValueError(
            'Output directory does not end with a trailing slash "/"!')

    else:
        pass

    files = glob.glob(directory + '/*.csv')

    for file in files:

        cat = Path(file).stem
 
        if trial_type == 'with_owner':

            cat = cat[:-16]

        elif trial_type == 'cat_alone':

            cat = cat[:-15]

        df = pd.read_csv(file)

        df["cat"] = cat

        df = df[['cat', 'ROI_name', 'trial', 'transitions_per_roi', 'cumulative_time_in_roi_sec', 'avg_time_in_roi_sec', 'avg_vel_in_roi']]

        df.to_csv(file, index=False)


    combined_csv = pd.concat([pd.read_csv(f) for f in files ])

    if trial_type == 'with_owner':

        combined_csv.to_csv(output_dir + "with_owner_combined_rois.csv", index=False, encoding='utf-8-sig')

    elif trial_type == 'cat_alone':

        combined_csv.to_csv(output_dir + "cat_alone_combined_rois.csv", index=False, encoding='utf-8-sig')
