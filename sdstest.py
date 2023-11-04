from sds011lib import sensor_wake, sensor_sleep, sensor_read, getData

sdssensorinit=getData()
print(sdssensorinit)
sdssensor=sensor_wake()
print(sdssensor)
sdsvalue=sensor_read
print(sdsvalue)
