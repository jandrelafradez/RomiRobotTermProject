from pyb import Pin, I2C
import time
import struct

class BNO055:
    def __init__(self, i2c,serial_data,serial_clock,reset):
        self.i2c  = i2c
        # Default I2C address for BNO055
        self.addr = 0x28
        # Default Mode
        self.mode = 0x00

        # Initialize the reset pin
        self.reset_pin = Pin(reset,Pin.OUT_PP)
        # Ensure reset pin is high (active low)
        self.reset_pin.high()
        time.sleep(0.75)

    def set_mode(self,mode):
        self.mode = mode
        self.i2c.mem_write(self.mode,self.addr, 0x3D)
        time.sleep(0.05)

    def get_calibration(self):
        # Get the calibration status from the IMU
        calib_stat  = bytearray([0 for n in range(1)])
        calib_stat  = self.i2c.mem_read(calib_stat,self.addr,0x35)


        # Unpack the calibration status and assign bytes to the
        # system, gyrator, accelerometer, and magnetometer
        calib_byte, = struct.unpack('<B',calib_stat)
        sys_calib   = (calib_byte >> 6 ) & 0x03
        gyr_calib   = (calib_byte >> 4 ) & 0x03
        acc_calib   = (calib_byte >> 2 ) & 0x03
        mag_calib   =  calib_byte & 0x03
        return sys_calib, gyr_calib, acc_calib, mag_calib

    def get_calib_coeffs(self):
        calib_coeffs = bytearray([0 for n in range(22)])
        self.i2c.mem_read(calib_coeffs,self.addr,0x55)
        acc_offset_x, acc_offset_y, acc_offset_z = struct.unpack('<hhh',calib_coeffs[0:6])
        mag_offset_x, mag_offset_y, mag_offset_z = struct.unpack('<hhh',calib_coeffs[6:12])
        gyr_offset_x, gyr_offset_y, gyr_offset_z = struct.unpack('<hhh',calib_coeffs[12:18])
        acc_radius, mag_radius = struct.unpack('<hh',calib_coeffs[18:22])
        return (acc_offset_x, acc_offset_y, acc_offset_z,
                mag_offset_x, mag_offset_y, mag_offset_z,
                gyr_offset_x, gyr_offset_y, gyr_offset_z,
                acc_radius, mag_radius)

    def set_calib_coeffs(self,calib_data):
        self.i2c.mem_write(self.mode,self.addr,0x55)
        time.sleep(0.05)

    def read_euler(self):
        euler_data = bytearray([0 for n in range(6)])
        self.i2c.mem_read(euler_data,self.addr,0x1A)
        heading,roll,pitch = struct.unpack('<hhh',euler_data)
        return heading/16,roll/16,pitch/16

    def read_heading(self):
        heading_data = bytearray([0 for n in range(2)])
        self.i2c.mem_read(heading_data,self.addr,0x1A)
        heading, = struct.unpack('<h',heading_data)
        return heading/16

    def read_angular_velocity(self):
        angular_data = bytearray([0 for n in range(6)])
        self.i2c.mem_read(angular_data, self.addr, 0x14)
        gyro_x, gyro_y, gyro_z = struct.unpack('<hhh',angular_data)
        return gyro_x/16,gyro_y/16,gyro_z/16

    def read_yaw_rate(self):
        yaw_data = bytearray([0 for n in range(2)])
        self.i2c.mem_read(yaw_data, self.addr, 0x18)
        yaw_rate,= struct.unpack('<h',yaw_data)
        return yaw_rate/16













