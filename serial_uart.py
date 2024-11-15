from machine import Pin, UART
import time

uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

def send_array(array):
    data = bytearray(array)
    chunk_size = 64
    for i in range(0, len(data), chunk_size):
        uart.write(data[i:i+chunk_size])
        time.sleep(0.01)

if __name__ == '__main__':
    while True:
        rand_array = [1, 3, 5, 7, 11, 13]
        send_array(rand_array)
        time.sleep(1)