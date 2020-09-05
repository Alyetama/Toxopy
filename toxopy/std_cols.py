import pandas as pd
from sklearn.preprocessing import StandardScaler


def std_cols(csv_file, vars_list):

    df = pd.read_csv(csv_file, index_col=[0])

    df[vars_list] = StandardScaler().fit_transform(df[vars_list])
