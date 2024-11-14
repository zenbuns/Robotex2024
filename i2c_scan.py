from machine import I2C, Pin

i2c = I2C(0, scl=Pin(17), sda=Pin(16))

devices = i2c.scan()
if devices:
    print("I2C devices found:", [hex(device) for device in devices])
else:
    print("No I2C devices found")