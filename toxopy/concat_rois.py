import pandas as pd
import csv
import glob
from pathlib import Path


def concat_rois(directory):

    files = glob.glob(directory + '/*.csv')

    for file in files:

        cat = Path(file).stem
        cat = cat[:-5]

        df = pd.read_csv(file)

        df["cat"] = cat

        df = df[['cat', 'ROI_name', 'transitions_per_roi', 'cumlative_time_in_roi_sec', 'avg_time_in_roi_sec', 'avg_vel_in_roi']]

        df.to_csv(file, index=False)


    combined_csv = pd.concat([pd.read_csv(f) for f in files ])

    combined_csv.to_csv("combined_rois.csv", index=False, encoding='utf-8-sig')
