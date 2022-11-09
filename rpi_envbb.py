import time
from rpi_sensor_monitors import monitors



if __name__ == '__main__':

    env_sensor = monitors.BME680()

    env_sensor.start()

    try:
        while True:
            time.sleep(1)
    except:
        env_sensor.stop()
