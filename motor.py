from pyb import Pin, Timer

class Motor:
    # 1a) Initializes a Motor object
    def __init__(self, PWM, DIR, nSLP, timer, channel):
        self.PWM = Pin(PWM, mode=Pin.OUT_PP)  # PWM pin
        self.DIR = Pin(DIR, mode=Pin.OUT_PP)  # Direction pin
        self.nSLP = Pin(nSLP, mode=Pin.OUT_PP, value=0)  # Sleep pin, initially off

        # Timer setup
        self.timer = Timer(timer, freq=1000)  # 1 kHz PWM frequency
        self.channel = self.timer.channel(channel, Timer.PWM, pin=self.PWM)  # PWM channel setup

    # 1b) Set effort of motors [-100,100]
    def set_effort(self, effort):
        effort = max(min(effort, 100), -100)  # Constrain effort to [-100, 100]

        if effort == 0:
            self.channel.pulse_width_percent(0)  # Stop motor
        elif effort > 0:
            self.DIR.low()  # Forward direction
            self.channel.pulse_width_percent(effort)  # Set PWM duty cycle
        else:
            self.DIR.high()  # Reverse direction
            self.channel.pulse_width_percent(-effort)  # Set PWM duty cycle

    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake mode'''
        self.nSLP.high()

    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.nSLP.low()