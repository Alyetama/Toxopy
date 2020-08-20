#!/usr/bin/python

import os
from subprocess import call


def ffconcat(cats, tvp, trial_type):
    # cats is a list of strings ["cat--id"]
    # tvp: /path/to/trials/videos/
    # trial_type: either "cat_alone" or "owner"

    if tvp.endswith('/') == False:

        raise ValueError('Path does not end with a trailing slash "/"')

    for cat in cats:

        if trial_type == "cat_alone":
            vid_list = [
                tvp + cat + '_T2.mp4', tvp + cat + '_T4.mp4',
                tvp + cat + '_T6.mp4', tvp + cat + '_T8.mp4',
                tvp + cat + '_T10.mp4'
            ]

        elif trial_type == "with_owner":
            vid_list = [
                tvp + cat + '_T1.mp4', tvp + cat + '_T3.mp4',
                tvp + cat + '_T5.mp4', tvp + cat + '_T7.mp4',
                tvp + cat + '_T9.mp4'
            ]

        else:
            raise ValueError(
                'False trial type!  The trial type should be either "cat_alone" or "with_owner".'
            )

        cat_txt = cat + '.txt'

        if os.path.exists(cat_txt):
            os.remove(cat_txt)

        file_vids = open(cat_txt, 'a')

        for video in vid_list:
            files_list = 'file ' + video + '\n'
            file_vids.write(files_list)
        file_vids.close()

        cat_sh = cat + '.sh'

        if os.path.exists(cat_sh):
            os.remove(cat_sh)

        file_sh = open(cat_sh, 'a')
        ffmpeg_container = " singularity exec /work/chaselab/malyetama/containers/ffmpeg_3.2-nvidia.sif "

        if trial_type == "cat_alone":

            ffmpeg_command = "#!/bin/bash \n" + ffmpeg_container + "ffmpeg -f concat -safe 0 -i " + cat + ".txt -c copy -y " + tvp + cat + "_cat.mp4"

        elif trial_type == "with_owner":

            ffmpeg_command = "#!/bin/bash \n" + ffmpeg_container + "ffmpeg -f concat -safe 0 -i " + cat + ".txt -c copy -y " + tvp + cat + "_owner.mp4"

        file_sh.write(ffmpeg_command)
        file_sh.close()

        os.chmod('./' + cat + '.sh', 0o755)
        call('./' + cat + '.sh', shell=True)
