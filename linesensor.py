import cotask
import task_share
from motor import Motor
from pyb import Pin, ADC
from time import sleep



class Sensor:
    # Initializes a sensor
    def __init__(self, pin):
        self.sensor = ADC(pin[0])
        self.white = pin[1]
        self.black = pin[2]
        self.reading = 0
        self.linear = 0

    # Calibrates the value of white
    def cal_white(self):
        self.white = self.sensor.read()
        print(self.white)
        return self.white

    # Calibrates the value of black
    def cal_black(self):
        self.black = self.sensor.read()
        print(self.black)
        return self.black

    def get_white(self):
        return self.white

    def get_black(self):
        return self.black

    # Gets current sensor reading
    def get_reading(self):
        self.reading = self.sensor.read()
        return self.reading

    # Normalizes the raw data to determine if the sensor is on the black line
    def interpolate(self,reading):
        if self.white == self.black:
            return 0  # or some default behavior
        self.linear = (reading - self.white) / (self.black - self.white)

        if self.linear > 1:
            self.linear = 1
        elif self.linear < 0:
            self.linear = 0

        return self.linear

class SensorArray:

    # An array for a multiple sensors
    def __init__(self,pins):
        self.array = []
        self.readings = []

        for pin in pins:
            sensor = Sensor(pin)
            self.array.append(sensor)

    # Calibrates the 'white' values for all of the sensors
    def cal_white(self):
        for sensor in self.array:
            sensor.cal_white()

    # Calibrates the 'black' values for all of the sensors
    def cal_black(self):
        for sensor in self.array:
            sensor.cal_black()

    # Reads and linearizes data from all of the sensors
    def read_linearized(self):
        self.readings = []
        for sensor in self.array:
            reading = sensor.get_reading()
            self.readings.append(sensor.interpolate(reading))

        return self.readings

    def get_white(self,index):
        return self.array[index].get_white()

    def get_black(self,index):
        return self.array[index].get_black()

    def get_all_white(self):
        return [sensor.get_white() for sensor in self.array]

    def get_all_black(self):
        return [sensor.get_black() for sensor in self.array]

    # Calculates the centroid of the sensor reading
    def get_centroid(self,readings):
        numerator = 0
        denominator = 0

        for i, value in enumerate(readings):
            numerator += value * (i + 1)
            denominator += value

        if denominator == 0:
            # No line detected
            return None
        return numerator / denominator

class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.prev_error = 0
        self.integral = 0

    def calc(self, error):
        P = self.Kp * error

        self.integral += error
        I = self.Ki * self.integral

        D = self.Kd * (error - self.prev_error)
        self.prev_error = error

        output=P+I+D
        return output





