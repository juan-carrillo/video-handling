from os import listdir, mkdir, path
from datetime import datetime
from math import floor
from moviepy.editor import VideoFileClip
from database.database import MySql


import numpy as np
import pandas as pd


def exists_path(directory_path):
	return path.exists(directory_path)


def create_directory(directory_path):
	try:
		mkdir(directory_path)
		print('Directory created {}'.format(directory_path))
	except FileExistsError as e:
		print('Directory already created {}'.format(directory_path))


def data_row(clip, file_name=None, extension=None, save=False, saving_dir=None):
	if save:
		file_path = saving_dir + '/' + file_name + '.' + extension
		clip.write_videofile(file_path)
		print('Saved video clip at: {}'.format(file_path))
	return {'clip_name': file_name, 'clip_file_extension': extension, 'clip_duration': clip.duration, 'clip_location': saving_dir, 'created_at': datetime.now(), 'updated_at': datetime.now()}


def buid_report(array_with_dicts, save=False, saving_dir='./reports'):
	report = pd.DataFrame(array_with_dicts)

	if save:
		create_directory(saving_dir)
		csv_file_path = saving_dir + '/reports.csv'
		report.to_csv(csv_file_path, index=False)
		print(f'Saved CSV report at: {csv_file_path}')

	return report

def read_csv(file_path):
	return pd.read_csv(file_path)


def save_dataframe_report_in_database(dataframe_report):
	db_values = ''
	max_idx = len(dataframe_report) - 1
	for row in dataframe_report.itertuples():
		separator = ';' if getattr(row, 'Index') == max_idx else ', '
		db_values += "('{}', '{}', '{}', '{}', '{}', '{}'){}\n".format(row.clip_name, row.clip_file_extension, row.clip_duration, row.clip_location, row.created_at, row.updated_at, separator)
	db_columns = "clip_name, clip_file_extension, clip_duration, clip_location, created_at, updated_at"

	sql_handler = MySql()
	try:
		sql_handler.change_database('test')

		if sql_handler.connection.is_connected():
			db_Info = sql_handler.connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)

			sql_handler.cursor.execute("select database();")
			record = sql_handler.cursor.fetchone()

			print(sql_handler.insert_rows('video_data', db_columns, db_values))
			print("You're connected to database: ", record)
	except Error as e:
		print("Error while connecting to MySQL", e)
	else:
		if sql_handler.connection.is_connected():
			sql_handler.cursor.close()
			sql_handler.connection.close()
			print("MySQL connection is closed")


def save_frames_with_moviepy():
	video_directory = './video_clips'
	create_directory(video_directory)

	video_file = VideoFileClip('/Users/juancarrillo/code/data_academy/airshow.mp4')
	fps = round(video_file.fps)

	n_total_secs = floor(video_file.duration)
	print('Video total duration: {} (fps: {})'.format(str(video_file.duration), fps))

	rows = []
	for i in np.arange(0, n_total_secs, 60):
		ini_limit, end_limit = i, i + 60 - 1
		ith_frame = ini_limit * fps
		if end_limit > n_total_secs:
			end_limit = n_total_secs
		print(f'{ini_limit} - {end_limit}')
		clip = video_file.subclip(ini_limit, end_limit)
		rows.append(data_row(clip, str(ith_frame) + 'thFrame', 'mp4', save=True, saving_dir=video_directory))
	report = buid_report(rows, True)
	# report = read_csv('./reports/reports.csv')
	save_dataframe_report_in_database(report)
	print(report)


def main():
	save_frames_with_moviepy()
	print('End of Main Method')


if __name__ == '__main__':
	main()
