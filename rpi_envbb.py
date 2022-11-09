import time
from rpi_sensor_monitors import monitors



if __name__ == '__main__':

    env_sensor = monitors.BME680()
    log_dir = env_sensor.log_file.split('/',1)
    log_dir.pop()
    print(log_dir)




    env_sensor.start()

    try:
        while True:

            time.sleep(1)
    except:
        env_sensor.stop()
