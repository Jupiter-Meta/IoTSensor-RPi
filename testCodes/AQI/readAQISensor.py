from sds011reader import SDS011Reader

sensor = SDS011Reader()
print(sensor.readValue())
sensor.close()
