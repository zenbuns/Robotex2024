from machine import Pin
import utime

class UltraSound():
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def get_distance(self) -> float:
        '''
        Returns distance in cm.
        '''
        
        signalon = 0
        signaloff = 0

        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep_us(5)
        self.trigger.low()

        while self.echo.value() == 0:
            signaloff = utime.ticks_us()
        while self.echo.value() == 1:
            signalon = utime.ticks_us()

        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return distance

if __name__ == '__main__':
    while True:
        ultra_sensor1 = UltraSound(3, 2)
        distance = ultra_sensor1.get_distance()
        print(f"Distance: {distance}")
        utime.sleep(0.1)