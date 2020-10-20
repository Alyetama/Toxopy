"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

from toxopy import fwarnings, trials
from pca import pca
import os
import pandas as pd
import inspect

# inspect.getargspec(pca.biplot3d)
# colormaps: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html


def PlotPCA(csv_file, Trial, legend=True, save=False, path=os.getcwd()):

    df = pd.read_csv(csv_file)

    trls = trials()

    d = {}

    for t, n in zip(trls, range(1, 11)):
        trial = []
        [trial.append(x) for x in list(df.columns[9:]) if f't{n}_' in x]
        d[t] = trial

    features = [x[3:] for x in d[Trial]]

    for i in features:
        df.rename(columns={i: i[3:]}, inplace=True)

    idx = df.loc[:, 'infection_status'].values
    dt = df[d[Trial]].to_numpy()

    # Load dataset
    X = pd.DataFrame(data=dt, columns=features, index=idx)

    # Initialize to reduce the data up to the nubmer of componentes that explains 95% of the variance.
    model = pca(n_components=0.95)

    # Reduce the data towards 3 PCs
    model = pca(n_components=3)

    # Fit transform
    results = model.fit_transform(X)

    fig, ax = model.biplot3d(legend=legend, SPE=True, hotellingt2=True)

    fig = ax.get_figure()

    if save is True:
        fig.savefig(f'{path}/{Trial}.png', bbox_inches='tight',
                    dpi=100, pad_inches=0.4)
