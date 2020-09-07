from toxopy import turnpoints_time_diff, concat_csv
import pandas as pd
import glob
from pathlib import Path
import os


def create_time_diff_data(csv_file, csv_dir, output_dir):

	"""
	'csv_file' is the file "turnpoints_super_improved.csv"
	'csv_dir' is "turnpoints_super_improved" directory
	'output_dir' is the output directory for the output file
	"""

	files = glob.glob(f'{csv_dir}/*.csv')

	cats = []

	for i in files:
		cats.append(Path(i).stem[:-13])

	def return_cats_lists():
		cats_list = []
		for i in range(0, len(cats)):
			cats_list.append([])
		return cats_list

	cats_lists = return_cats_lists()

	for cat, i in zip(cats, range(0, len(cats_lists))):
		cats_lists[i].append(cat)
		cats_lists[i].append(turnpoints_time_diff(csv_file, cat))
		df = pd.DataFrame()
		df['time_diff'] = cats_lists[i][1]
		df['cat'] = cats_lists[i][0]

		set_status(df)
		
		df = df[['cat', 'infection_status', 'time_diff']]

		df.to_csv(f'{output_dir}/{cat}.csv', index=False, encoding='utf-8-sig')


	if os.path.exists(f'{output_dir}/all_time_diff.csv'):
	  os.remove(f'{output_dir}/all_time_diff.csv')

	concat_csv(output_dir, 'all_time_diff')

	[os.remove(f'{output_dir}/{i}.csv') for i in cats]
