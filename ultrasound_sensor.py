from machine import Pin
import utime

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def ultra():
   signalon = 0
   signaloff = 0

   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()

   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()

   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   return distance

if __name__ == '__main__':
    while True:
        distance = ultra()
        print(f"Distance: {distance}")
        utime.sleep(0.1)