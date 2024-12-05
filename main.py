from machine import I2C, Pin, UART, PWM
import utime
import time
from vl53l0x import VL53L0X
import serial_uart as ser
from hc_sr04 import UltraSound  

class Master():
   def __init__(self):
       self.tof = VL53L0X(I2C(0, scl=Pin(13), sda=Pin(12)))
       #self.setup_tof()
       self.uart = UART(0, baudrate=115200)
       self.r_ultrasensor = UltraSound(19, 18)
       self.l_ultrasensor = UltraSound(21, 20)
       # self.r_motor = Pin()
       # self.l_motor = Pin()
       self.r_motor_speed = 0
       self.l_motor_speed = 0
       self.grabber_state = 0
       self.setup_tof()
       
   def setup_tof(self) -> None:
       '''
       All the necessary settings to make the tof sensor work properly.
       '''
       self.tof.set_measurement_timing_budget(40000)
       self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[1], 8)
   
   def tof_distance(self) -> int:
       offset_mm = 30
       distance = self.tof.ping() - offset_mm
       return int(distance)

def main() -> None:
   m = Master()
   delay = 0.005 # Seconds
   
   while True:
       #array = [m.tof_distance(), m.r_ultrasensor.get_distance(), m.l_ultrasensor.get_distance()]
       #array = [1234, m.r_ultrasensor.get_distance(), m.l_ultrasensor.get_distance()]
       
       r_distance = m.r_ultrasensor.get_distance()
       utime.sleep_ms(50)  # Add delay between sensors
       l_distance = m.l_ultrasensor.get_distance() 
       tof_dist = m.tof_distance()
       
       sensor_array = [r_distance, l_distance, tof_dist]
       ser.send_array(m.uart, sensor_array)
       
       received_array = ser.receive_array(m.uart, 3)
       if received_array:
           m.r_motor_speed = received_array[0]
           m.l_motor_speed = received_array[1]
           m.grabber_state = received_array[2]
       
       print(f'right: {r_distance}, left: {l_distance}, tof: {tof_dist}')
       time.sleep(delay)

if __name__ == '__main__':
   main()
