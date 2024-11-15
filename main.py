from machine import I2C, Pin
import utime
import time
from hc_sr04 import UltraSound
from vl53l0x import VL53L0X

class Master():
    def __init__(self):
        self.tof = VL53L0X(I2C(0, scl=Pin(17), sda=Pin(16)))
        self.setup_tof()
        #self.l_ultrasensor = UltraSound(3, 2)
        #self.r_ultrasensor = UltraSound(5, 4)

    def setup_tof(self) -> None:
        '''
        All the necessary settings to make the tof sensor work properly.
        '''
        self.tof.set_measurement_timing_budget(40000)
        self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[1], 8)
    
    def tof_distance(self) -> int:
        offset_mm = 30
        distance = self.tof.ping() - offset_mm
        return distance

def main() -> None:
    m = Master()

    while True:
        distance = m.tof_distance()
        print(f"{distance} mm")
        time.sleep(0.005)

if __name__ == '__main__':
    main()