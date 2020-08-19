"""Object-specific python package to run automated tasks in the Chase Lab."""

from .ffsync import ffsync
from .ffconcat import ffconcat
from .lazytrim import lazytrim
from .improve_dlc_output import improve_dlc_output
from .improve_dlc_csv import improve_dlc_csv
from .improve_dlc_output_cat_alone import improve_dlc_output_cat_alone
from .csv2h5 import csv2h5
from .rois import rois
from .concat_rois import concat_rois

from .version import __version__, VERSION
