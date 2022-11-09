import time, os
from rpi_sensor_monitors import monitors

def push_to_csv(csv_file, data):
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
	print(f'data pushed to {csv_file}')


if __name__ == '__main__':

    env_sensor = monitors.BME680()
    log_dir = env_sensor.log_file.rsplit('/',1)
    log_dir.pop()
    csv_file = f'{log_dir}/envbb_data.csv'


    env_sensor.start()

    push_to_csv(csv_file, env_sensor.sensor_readings)
    env_sensor.stop()

    try:
        while True:
            push_to_csv(csv_file, env_sensor.sensor_readings)
            time.sleep(1)
    except:
        env_sensor.stop()
