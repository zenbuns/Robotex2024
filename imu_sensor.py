from machine import I2C, Pin
import time
import math

# MPU-6050 default I2C address
MPU6050_ADDR = 0x68

# MPU-6050 Registers
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class MPU6050:
    def __init__(self, i2c, addr=MPU6050_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, PWR_MGMT_1, b'\x00')
        self.gyro_scale = 131  # Gyroscope scale factor for ±250°/s
        self.gyro_offsets = self.calibrate_gyro()

    def calibrate_gyro(self, num_samples=1000):
        print("Calibrating gyroscope...")
        offset_x = offset_y = offset_z = 0
        
        for _ in range(num_samples):
            gx, gy, gz = self.read_raw_gyro()
            offset_x += gx
            offset_y += gy
            offset_z += gz
            time.sleep(0.005)
        
        offset_x /= num_samples
        offset_y /= num_samples
        offset_z /= num_samples
        
        print("Gyro calibration offsets:", offset_x, offset_y, offset_z)
        return offset_x, offset_y, offset_z

    def read_raw_gyro(self):
        data = self.i2c.readfrom_mem(self.addr, GYRO_XOUT_H, 6)
        
        gyro_x = self.convert_to_int16(data[0], data[1])
        gyro_y = self.convert_to_int16(data[2], data[3])
        gyro_z = self.convert_to_int16(data[4], data[5])
        
        return gyro_x, gyro_y, gyro_z

    def convert_to_int16(self, high, low):
        value = (high << 8) | low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value

    def get_gyro_data(self):
        gx, gy, gz = self.read_raw_gyro()
        
        gx -= self.gyro_offsets[0]
        gy -= self.gyro_offsets[1]
        gz -= self.gyro_offsets[2]
        
        gx = gx / self.gyro_scale
        gy = gy / self.gyro_scale
        gz = gz / self.gyro_scale
        return gx, gy, gz

def main():
    i2c = I2C(0, scl=Pin(17), sda=Pin(16))
    mpu = MPU6050(i2c)
    
    rotation_x = 0
    rotation_y = 0
    rotation_z = 0
    
    last_time = time.ticks_ms()
    
    try:
        while True:
            current_time = time.ticks_ms()
            dt = time.ticks_diff(current_time, last_time) / 1000  # dt in seconds
            last_time = current_time
            
            gx, gy, gz = mpu.get_gyro_data()
            
            rotation_x += gx * dt
            rotation_y += gy * dt
            rotation_z += gz * dt
            
            print("Rotation (degrees): X={:.2f}, Y={:.2f}, Z={:.2f}".format(rotation_x, rotation_y, rotation_z))
            
            time.sleep(0.002)
    
    except KeyboardInterrupt:
        print("Measurement stopped")

if __name__ == '__main__':
    main()