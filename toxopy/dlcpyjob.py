import tensorflow as tf
import os

os.environ["DLClight"] = "True"
import deeplabcut


def dlcpyjob(cfg, videofile_path):

    deeplabcut.create_training_dataset(cfg, Shuffles=[1])

    deeplabcut.train_network(cfg,
                             shuffle=1,
                             saveiters=1000,
                             displayiters=1000,
                             maxiters=200000)

    deeplabcut.evaluate_network(cfg, Shuffles=[1], plotting=True)

    deeplabcut.analyze_videos(cfg, videofile_path, videotype='mp4')

    deeplabcut.create_labeled_video(cfg, videofile_path, filtered=False)

    deeplabcut.plot_trajectories(cfg,
                                 videofile_path,
                                 videotype='.mp4',
                                 filtered=False)

    prj_path = cfg.replace('/config.yaml', '/videos/')

    os.rename(prj_path + 'plot-poses', prj_path + 'plot-poses-unfiltered')

    deeplabcut.filterpredictions(cfg,
                                 videofile_path,
                                 shuffle=1,
                                 trainingsetindex=0,
                                 filtertype='arima',
                                 p_bound=0.01,
                                 ARdegree=3,
                                 MAdegree=1,
                                 alpha=0.01)

    deeplabcut.create_labeled_video(cfg,
                                    videofile_path,
                                    videotype='.mp4',
                                    filtered=True)

    deeplabcut.plot_trajectories(cfg,
                                 videofile_path,
                                 videotype='.mp4',
                                 filtered=True)

    os.rename(prj_path + 'plot-poses', prj_path + 'plot-poses-filtered')
