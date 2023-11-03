from sds011 import SDS011
import time

def read_sds011_sensor(port='/dev/ttyUSB0'):
    try:
        sds = SDS011(port=port)
        sds.set_work_period(work_time=0)  # Set continuous mode

        while True:
            pm25, pm10 = sds.query()
            print(f'PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³')
            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        sds.set_work_period(work_time=0)  # Set to sleep mode before exiting
        print('Exiting.')

if __name__ == "__main__":
    read_sds011_sensor()
