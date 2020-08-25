"""Object-specific python package to run automated tasks in the Chase Lab."""

from .ffsync import ffsync
from .ffconcat import ffconcat
from .lazytrim import lazytrim
from .improve_dlc_output import improve_dlc_output
from .improve_dlc_csv import improve_dlc_csv
from .improve_dlc_output_cat_alone import improve_dlc_output_cat_alone
from .csv2h5 import csv2h5
from .analyze_rois import analyze_rois
from .concat_rois import concat_rois
from .roi_calc_mw import roi_calc_mw
from .json2tidycsv import json2tidycsv
from .obtain_grand_m import obtain_grand_m

from .version import __version__, VERSION
