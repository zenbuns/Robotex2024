from machine import I2C, Pin
import utime
import time
from ultrasound_sensor import UltraSound

#left_ultrasensor = UltraSound(3, 2)

def main() -> None:
    try:
        while True:
            
            time.sleep(0.005)
    
    except KeyboardInterrupt:
        print("Program stopped")
        #print(f"Distance: {left_ultrasensor.get_distance()}")
        #utime.sleep(0.1)

if __name__ == '__main__':
    main()