from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
time.sleep(1)

devices = i2c.scan()
if devices:
    print("I2C device found at address:", hex(devices[0]))
    print("All I2C devices found:", [hex(device) for device in devices])
else:
    print("No I2C devices found")