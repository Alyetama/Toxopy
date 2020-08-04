#!/usr/bin/python

# todo: add option for either cat or owner trials

import os
from subprocess import call


def ffconcat(cats, tvp):
# cats is a list of strings ["cat--id"]
# tvp: /path/to/trials/videos/

    for cat in cats:

        vid_list = [
            tvp + cat + '_T2.mp4', tvp + cat + '_T4.mp4', tvp + cat + '_T6.mp4',
            tvp + cat + '_T8.mp4', tvp + cat + '_T10.mp4'
        ]

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
        ffmpeg_command = "#!/bin/bash \n" + ffmpeg_container + "ffmpeg -f concat -safe 0 -i " + cat + ".txt -c copy -y " + tvp + cat + "_cat.mp4"

        file_sh.write(ffmpeg_command)
        file_sh.close()

        os.chmod('./' + cat + '.sh', 0o755)
        call('./' + cat + '.sh', shell=True)
