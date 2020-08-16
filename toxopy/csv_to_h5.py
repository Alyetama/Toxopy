import pandas as pd
import glob


def csv2h5(directory=None, files=None):

    if directory == None:

        for file in files:

            df = pd.read_csv(file)

            df.to_hdf(file.strip('.csv') + '.h5',
                      'data',
                      mode='w',
                      format='table')
            del df

    else:

        csv_files_dir = directory + '/*.csv'

        files = glob.glob(csv_files_dir)

        for file in files:

            df = pd.read_csv(file)

            df.to_hdf(file.strip('.csv') + '.h5',
                      'data',
                      mode='w',
                      format='table')
            del df
