from machine import Pin, UART
import time
import struct

def send_array(uart, data, data_type='i'):
   '''
   Sends array over UART using struct packing.
   :param uart: UART object for serial communication
   :param data: Array to send over UART
   :param data_type: Type of data in array ('i' for int, 'f' for float)
   '''
   fmt = f'<{len(data)}{data_type}'  # Little-endian format string
   binary_data = struct.pack(fmt, *data)
   uart.write(binary_data)

def receive_array(uart, array_length, data_type='i'):
   '''
   Receives array from UART using struct unpacking.
   :param uart: UART object for serial communication 
   :param array_length: Expected length of array to receive
   :param data_type: Type of data in array ('i' for int, 'f' for float)
   :return: Tuple of received values or None if read failed
   '''
   type_size = struct.calcsize(data_type)
   num_bytes = array_length * type_size
   data = uart.read(num_bytes)
   
   if data and len(data) == num_bytes:
       fmt = f'<{array_length}{data_type}'
       return struct.unpack(fmt, data)
   return None

if __name__ == '__main__':
   uart = UART(0, baudrate=115200)  # UART0: GP0 (TX), GP1 (RX)
   
   x, y, z = 3, 2, 1 
   while True:
       # Test sending two different arrays
       rand_array = [1, 3, 5, 7, 11, 13]
       send_array(uart, rand_array)
       time.sleep(0.01)  # Prevent buffer overflow
       
       array = [x, y, z]
       send_array(uart, array)
       
       # Try to receive 4 integers
       received = receive_array(uart, 4)
       if received:
           print(f"Received: {received}")
       
       # Increment test values
       x += 1
       y += 2
       z += 3
       
       time.sleep(0.01)