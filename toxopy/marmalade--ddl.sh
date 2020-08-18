#!/bin/bash 
 singularity exec /work/chaselab/malyetama/containers/ffmpeg_3.2-nvidia.sif ffmpeg -f concat -safe 0 -i marmalade--ddl.txt -c copy -y /work/chaselab/malyetama/marmalade--ddl_cat.mp4