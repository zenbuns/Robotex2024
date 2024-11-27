import machine
import struct
import utime


def send_array(uart, data, data_type='i') -> None:
    '''
    :param uart: Uart object.
    :param data: Array of n size to send.
    :param data_type: Type of data in array, 'i' (integer) is default, 'f' for float.
    '''
    fmt = f'<{len(data)}{data_type}'
    binary_data = struct.pack(fmt, *data)
    uart.write(binary_data)

def receive_array(uart, array_length, data_type='i'):
    '''
    :param uart: Uart object.
    :param data: Array of n size that gets received.
    :param data_type: Type of data in array, 'i' (integer) is default, 'f' for float.
    :return: Received array
    '''
    num_bytes = array_length * 4
    data = uart.read(num_bytes)
    
    if data and len(data) == num_bytes:
        fmt = f'<{array_length}{data_type}'
        received_arr = struct.unpack(fmt, data)
        return received_arr
    
    return None

if __name__ == '__main__':
    uart = machine.UART(0, baudrate=115200)
    
    x, y, z = 3, 2, 1

    while True:
        array = [x, y, z]
        send_array(uart, array)
        received = receive_array(uart, 4)
        if received:
            print(f"Received array: {received}")
        x += 1
        y += 2
        z += 3
        
        utime.sleep(0.01)