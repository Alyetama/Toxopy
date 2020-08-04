import os
from subprocess import run
import pandas as pd
import shlex


def ffsync(sync_csv, videos_dir):

    df = pd.read_csv(sync_csv, sep=",")

    names = df.columns
    df = pd.DataFrame(df, columns=names)

    camera_1 = df.iloc[0][0]
    camera_2 = df.iloc[1][0]

    offset_1 = df.iloc[0][1]
    offset_2 = df.iloc[1][1]

    offset = []

    if offset_1 != 0:
        offset.append(camera_1)
        offset.append(offset_1)
        offset.append(camera_2)
    elif offset_2 != 0 and offset_2 > 0:
        offset.append(camera_2)
        offset.append(offset_2)
        offset.append(camera_1)
    elif offset_2 != 0 and offset_2 < 0:
        offset.append(camera_1)
        offset.append(offset_2 * -1)
        offset.append(camera_2)

    ffprobe_command = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + videos_dir + '/'

    ffprobe_1 = ffprobe_command + offset[0]
    ffprobe_2 = ffprobe_command + offset[2]

    duration_values = []

    for i in [ffprobe_1, ffprobe_2]:
        ffprobe_run = os.popen(i)
        video_duration = ffprobe_run.read()
        video_duration = video_duration.strip('\n')
        duration_values.append(video_duration)

    end_time = min(duration_values)

    ffmpeg_run = shlex.split('ffmpeg -ss ' + str(offset[1]) + ' -i ' +
                             videos_dir + '/' + str(offset[0]) + ' -t ' +
                             end_time + ' -y ' + videos_dir + '/synced_' +
                             str(offset[0]))

    run(ffmpeg_run)
