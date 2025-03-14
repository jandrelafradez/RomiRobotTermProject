from pyb import Timer,Pin
from time import ticks_us, ticks_diff
from array import array

class Encoder:
    def __init__(self,en_tim, chA_pin, chB_pin):


        # Initializes the Encoder Object and position variables

        self.position = 0              # Total accumulated position of the encoder
        self.prev_count = 0            # Counter value from the most recent update
        self.delta = 0                 # Change in count between last two updates
        self.dt = 0                    # Amount of time between last two updates
        self.prev_ticks = 0
        self.current_count = 0
        #self.EN_counter = EN_tim.counter()
        self.AR = 65535

        # Configure the time in encoder mode
        #self.en_tim = Timer(en_tim, prescaler=0, period=0xFFFF, mode=Timer.ENC_AB)
        self.enable_timer = Timer(en_tim, prescaler=0, period=0xFFFF)
        self.chA_PIN = self.enable_timer.channel(1,mode=Timer.ENC_AB, pin=Pin(chA_pin))
        self.chB_PIN = self.enable_timer.channel(2,mode=Timer.ENC_AB, pin=Pin(chB_pin))


        # Time tracking variables
        self.start_time = ticks_us()      # Reference time in microseconds
        self.last_time = self.start_time  # Last update time


    def update (self):
        # Updates encoder'sk timer counter
        current_time = ticks_us()
        self.dt  = ticks_diff(current_time, self.last_time)
        self.last_time= current_time

        # Updates the encoder counts
        self.current_count = self.enable_timer.counter()
        self.delta = self.current_count - self.prev_count
        self.prev_count = self.current_count

        #Update delta if rollover has occurred
        if self.delta > ((self.AR+1)/2):
            self.delta = self.delta - (self.AR+1)
        if self.delta <- ((self.AR+1)/2):
            self.delta = self.delta + (self.AR+1)
        self.position += self.delta

    def get_position(self):
        #Returns current position
        return self.position * 2 * 3.141592653589793/1440

    def get_velocity(self):
        # Returns the velocity by measuring the change in displacement v change in time
        if self.dt == 0:
            return 0
        else:
            #return self.delta/(self.dt/1_000_000)
            return (self.delta * 2 * 3.141592653589793/1440)/(self.dt/1_000_000)

    def get_delta(self):
        # Returns the change count between the last two updates
        elapsed = ticks_diff(ticks_us(), self.start_time)
        return elapsed/1_000_000

    def zero(self):
        # Resets position back to zero
        self.position = 0
        self.dt = 0




