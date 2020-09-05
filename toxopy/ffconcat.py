"""
Toxopy (https://github.com/bchaselab/Toxopy)
© M. Alyetama, University of Nebraska at Omaha
Licensed under the terms of the MIT license
"""

import os
from subprocess import call


def ffconcat(cats, tvp, trial_type):
    # cats is a list of strings ["cat--id"]
    # tvp: /path/to/trials/videos/
    # trial_type: either "cat_alone" or "owner"

    if tvp.endswith('/') is False:

        raise ValueError('Path does not end with a trailing slash "/"')

    for cat in cats:
        tc = tvp + cat
        if trial_type == "cat_alone":
            vid_list = [
                tc + '_T2.mp4', tc + '_T4.mp4', tc + '_T6.mp4', tc + '_T8.mp4',
                tc + '_T10.mp4'
            ]

        elif trial_type == "with_owner":
            vid_list = [
                tc + '_T1.mp4', tc + '_T3.mp4', tc + '_T5.mp4', tc + '_T7.mp4',
                tc + '_T9.mp4'
            ]

        else:
            raise ValueError(
                'False trial type!  The trial type should be either "cat_alone" or "with_owner".'
            )

        cat_txt = f'{cat}.txt'

        if os.path.exists(cat_txt):
            os.remove(cat_txt)

        file_vids = open(cat_txt, 'a')

        for video in vid_list:
            files_list = f'file {video} \n'
            file_vids.write(files_list)
        file_vids.close()

        cat_sh = f'{cat}.sh'

        if os.path.exists(cat_sh):
            os.remove(cat_sh)

        file_sh = open(cat_sh, 'a')

        if trial_type == "cat_alone":

            ffmpeg_command = f'#!/bin/bash\n ffmpeg -f concat -safe 0 -i {cat}.txt -c copy -y {tvp}{cat}_cat.mp4'

        elif trial_type == "with_owner":

            ffmpeg_command = f'#!/bin/bash\n ffmpeg -f concat -safe 0 -i {cat}.txt -c copy -y {tvp}{cat}_owner.mp4'

        file_sh.write(ffmpeg_command)
        file_sh.close()

        os.chmod('./' + cat + '.sh', 0o755)
        call('./' + cat + '.sh', shell=True)
