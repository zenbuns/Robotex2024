from machine import Pin
import utime

class UltraSound:
   """HC-SR04 ultrasonic distance sensor with filtering."""
   
   def __init__(self, trigger_pin: int, echo_pin: int):
       self.trigger = Pin(trigger_pin, Pin.OUT)
       self.echo = Pin(echo_pin, Pin.IN)
       self.last_valid = 0
       self.readings = [0] * 3
       self.index = 0

   def get_distance(self) -> int:
       """Get filtered distance in mm."""
       try:
           # Trigger measurement
           self.trigger.low()
           utime.sleep_us(2)
           self.trigger.high() 
           utime.sleep_us(5)
           self.trigger.low()

           # Get echo with timeout
           timeout = utime.ticks_us() + 30000
           while self.echo.value() == 0:
               start = utime.ticks_us()
               if utime.ticks_us() > timeout:
                   return self.last_valid

           while self.echo.value() == 1:
               end = utime.ticks_us()
               if utime.ticks_us() > timeout:
                   return self.last_valid

           # Calculate and filter distance
           dist_mm = int((end - start) * 0.0343 / 2 * 10)
           if 5 <= dist_mm <= 4000:
               self.readings[self.index] = dist_mm
               self.index = (self.index + 1) % 3
               valid = sorted([x for x in self.readings if x != 0])
               if valid:
                   self.last_valid = valid[len(valid)//2]
           return self.last_valid

       except:
           return self.last_valid


def main():
   sensor1 = UltraSound(19, 18)
   sensor2 = UltraSound(21, 20)
   
   while True:
       dist1 = sensor1.get_distance()
       utime.sleep_ms(10)
       dist2 = sensor2.get_distance()
       print(f"Sensor 1: {dist1}mm, Sensor 2: {dist2}mm")
       utime.sleep(0.1)

if __name__ == '__main__':
   main()
