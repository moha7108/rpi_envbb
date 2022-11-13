import time, os, csv, datetime
from rpi_sensor_monitors import monitors
from rpi_control_center import rpi_usb

str_format = '%Y%m%d%H%M%S'

def find_ts_path(ts, data_files):

	for file in data_files:
		if ts in file['file']:
			return file['file']
		else:
			return None


class csv_handler():
	def __init__(self, base_dir ='log/', filename='pi_data', max_file_size =89000, max_handling_size = 5000000):

		if not os.path.exists(base_dir): os.makedirs(base_dir)

		self.base_dir = base_dir
		self.filename = filename
		self.max_file_size = max_file_size *1000
		self.max_handling_size = max_handling_size *1000


		self.data_files = dict()
		self.writing_to = None
		self.total_size = None

		self.check_files()



	def __call__(self, data):
		'''
		'''

		self.check_files()

		if not self.writing_to:
			ts = datetime.datetime.now().strftime(str_format)
			self.writing_to = f'{self.base_dir}{ts}_{self.filename}.csv'

		self.push_to_csv(self.writing_to, data)

		self.check_files()


	def check_files(self):
		'''
		'''
		data_file_paths = [self.base_dir+file for file in os.listdir(self.base_dir) if os.path.isfile(self.base_dir+file) and self.filename in file and '.csv' in file]

		# if not data_file_paths:
		#     ts = datetime.datetime.now().strftime(str_format)
		#     data_file_paths = [f'{self.base_dir}{ts}_{self.filename}.csv']

		data_files = []
		total_size = 0

		for file in data_file_paths:
			file_stats = os.stat(file)

			data_file = {   'file': file,
							'size': file_stats.st_size,
							'last_modified': file_stats.st_mtime,
							'status': 'active' if file_stats.st_size <= self.max_file_size else 'full'
						  }

			total_size += data_file['size']

			data_files.append(data_file)

		self.data_files = data_files
		self.total_size = total_size

		if self.total_size > self.max_handling_size: self.purge_data_files()

		active_files = [file for file in data_files if file['status'] == 'active']


		if active_files:

			ts = max([datetime.datetime.strptime(file['file'].split('_')[0].split('/')[-1], str_format) for file in active_files]).strftime(str_format)

			# max([int(file['file'].split('_')[0].split('/')[-1]) for file in self.data_files if file['status'] == 'active'])
			# self.writing_to = max([int(file['file'].split('_')[0].split('/')[-1]) for file in self.data_files if file['status'] == 'active'])

			self.writing_to = find_ts_path(ts, active_files)

		elif not active_files:
			self.writing_to = None

			# ts = datetime.datetime.now().strftime(str_format)
			# self.writing_to = f'{self.base_dir}{ts}_{self.filename}.csv'
			# self.data_files.append(self.writing_to)


	def purge_data_files(self, all_files = False):
		''''''

		if all_files:
			for  data_file in self.data_files:
				os.remove(data_file['file'])
				self.data_files.remove(data_file)

		else:
			for data_file in self.data_files:
				if data_file['status'] =='full':
					os.remove(data_file['file'])
					self.data_files.remove(data_file)
				else:
					pass

		self.total_size = sum([file['size'] for file in self.data_files])

	def push_to_csv(self, csv_file, data):
		""" """
		fieldnames = [label for label, paremeter in data.items()]

		if not os.path.isfile(csv_file):
			with open(csv_file, 'w', newline='') as file:
				writer = csv.DictWriter(file, fieldnames =fieldnames)
				writer.writeheader()
				writer.writerow(data)
		else:
			with open(csv_file, 'a', newline='') as file:
				writer = csv.DictWriter(file, fieldnames =fieldnames)
				writer.writerow(data)


if __name__ == '__main__':

	test_data = {'hello': 13, 'poop':'34013'}

	test_csv = csv_handler(filename='test_data')

	print(test_csv.data_files)
	print(test_csv.writing_to)
	print(test_csv.total_size)

	test_csv(test_data)


	lol_csv = csv_handler()

	print(lol_csv.data_files)
	print(lol_csv.writing_to)
	print(lol_csv.total_size)

	# env_sensor = monitors.BME680()
	# log_dir = env_sensor.log_file.rsplit('/',1)
	# log_dir.pop()
	# csv_file = f'{log_dir[0]}/envbb_data.csv'
	#
	#
	# env_sensor.start()
	# time.sleep(5)
	#
	# try:
	# 	while True:
	# 		# print(env_sensor.sensor_readings)
	# 		push_to_csv(csv_file, env_sensor.sensor_readings)
	# 		time.sleep(1)
	#
	# except:
	# 	env_sensor.stop()
