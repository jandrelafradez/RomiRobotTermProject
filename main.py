import gc
import pyb
import cotask
import task_share
from pyb import Pin, I2C
from motor import Motor
from Encoder import Encoder
from time import ticks_us, ticks_diff,sleep
from linesensor import Sensor,SensorArray, PID  # Assuming Sensor and SensorArray are in sensor.py
from imu import BNO055

def motor_task_left(shares):
    motor_effort, encoder_position, encoder_velocity, test_state = shares

    motor = Motor('A9', 'C7', 'B6', 1, 2)
    encoder = Encoder(2, "A15", "B3")

    S_INIT = 0
    S_IDLE = 1
    S_RUNNING = 2

    state = S_INIT
    prev_test_state = 0

    while True:
        if state == S_INIT:
            print('Initial state: Left Motor')
            motor.enable()
            state = S_IDLE

        elif state == S_IDLE:
            motor.set_effort(0)
            if test_state.get() in [1,2] and prev_test_state == 0:
                state = S_RUNNING

        elif state == S_RUNNING:
            if test_state.get() == 0:
                motor.set_effort(0)
                state = S_IDLE
            else:
                motor_effort = eff_L.get()
                motor.set_effort(motor_effort)

        prev_test_state = test_state.get()
        yield state


def motor_task_right(shares):
    motor_effort, encoder_position, encoder_velocity, test_state = shares

    motor = Motor('B1', 'B15', 'B2', 3, 4)
    encoder = Encoder(5, "A0", "A1")

    S_INIT = 0
    S_IDLE = 1
    S_RUNNING = 2

    state = S_INIT
    prev_test_state = 0

    while True:
        if state == S_INIT:
            print('Initial state: Left Motor')
            motor.enable()
            state = S_IDLE

        elif state == S_IDLE:
            motor.set_effort(0)
            if test_state.get() in [1,2] and prev_test_state == 0:
                state = S_RUNNING

        elif state == S_RUNNING:
            if test_state.get() == 0:
                motor.set_effort(0)
                state = S_IDLE
            else:
                motor_effort = eff_R.get()
                motor.set_effort(motor_effort)


        prev_test_state = test_state.get()
        yield state


def user_task(shares):
    eff_L, eff_R, test_state = shares

    vcp = pyb.USB_VCP()

    S_MENU_DISPLAY = 0
    S_WAIT_FOR_INPUT = 1
    S_START_TEST = 2

    state = S_MENU_DISPLAY

    while True:
        if state == S_MENU_DISPLAY:
            print('\r\nRomi Control Menu:')
            print('1. Start Line Following')
            print('2. Stop Line Following')
            state = S_WAIT_FOR_INPUT

        elif state == S_WAIT_FOR_INPUT:
            if vcp.any():
                eff = vcp.read(1).decode()
                if eff == '1':
                    test_state.put(1)
                    state = S_START_TEST
                elif eff == '2':
                    test_state.put(0)
                    eff_L.put(0)
                    eff_R.put(0)
                    print('Line following stopped.')
                    state = S_MENU_DISPLAY

        elif state == S_START_TEST:
            if test_state.get() == 0:
                state = S_MENU_DISPLAY

        yield state

def sensor_task(shares):
    eff_L, eff_R, pos_L, pos_R,heading_share, test_state = shares

    # Initialize PID
    pid = PID(Kp=4.5, Ki=0, Kd=0)

    # Range for triggering the action
    position_range_L = (30, 37)  # Left encoder range: 23 <= pos_L < 30


    # Timer variables for the action
    action_start_time = None  # None indicates no action is currently happening
    action_duration = 2250  # Duration of the action in milliseconds

    while True:

        if test_state.get() == 2:
            print('In State 2')
            yield

        elif test_state.get() == 1:
            # Read sensor and encoder values
            readings = sensor_array.read_linearized()
            centroid = sensor_array.get_centroid(readings)
            active_sensor = sum(readings)
            print(f'Active sensor: {active_sensor}')



            # Check if encoder values are within the specified range
            if position_range_L[0] <= pos_L.get() < position_range_L[1] and active_sensor <= 4.5:
                if action_start_time is None:  # Start action if not already happening
                    action_start_time = ticks_us()
                    print("Action started based on encoder position range")

                elapsed_time = ticks_diff(ticks_us(), action_start_time) / 1000  # Convert to ms
                if elapsed_time < action_duration:
                    # Perform the specific action (e.g., drive straight or spin)
                    eff_L.put(20)
                    eff_R.put(20)
                    print(f"Performing action for {elapsed_time:.2f} ms")
                else:
                    # Action complete
                    action_start_time = None  # Reset the timer
                    print("Action complete")
            else:
                # If encoders are out of range, reset the timer and return to normal behavior
                action_start_time = None

                if centroid is not None:
                    # Normal PID-based line following
                    error = 4.5 - centroid
                    correction = pid.calc(error)

                    left_effort = BASE_SPEED - correction
                    right_effort = BASE_SPEED + correction

                    # Constrain efforts within range
                    left_effort = max(0, min(100, left_effort))
                    right_effort = max(0, min(100, right_effort))

                    eff_L.put(left_effort)
                    eff_R.put(right_effort)
                else:
                    # Line lost: Stop motors or handle recovery
                    print("Line Lost")
                    eff_L.put(0)
                    eff_R.put(0)


        else:
            # Stop motors if test_state is 0
            eff_L.put(0)
            eff_R.put(0)

        yield


def encoder_task(shares):
    pos_L, vel_L, pos_R, vel_R, test_state = shares

    # Initialize encoders
    encoder_left = Encoder(2, "A15", "B3")
    encoder_right = Encoder(5, "A0", "A1")

    while True:
        if test_state.get() in [1,2] :
            # Read Encoder Values
            encoder_left.update()
            encoder_right.update()
            position_left = encoder_left.get_position()
            velocity_left = encoder_left.get_velocity()
            position_right = encoder_right.get_position()
            velocity_right = encoder_right.get_velocity()

            # Debug: Ensure values are being read correctly
            print(f" Left Pos: {position_left} Right Pos: {position_right}")

            # Store values in shared variables
            pos_L.put(position_left)
            vel_L.put(velocity_left)
            pos_R.put(position_right)
            vel_R.put(velocity_right)
        else:
            # If not active, reset the values to zero
            pos_L.put(0)
            vel_L.put(0)
            pos_R.put(0)
            vel_R.put(0)

        yield

def imu_task(shares):
    heading_share, test_state = shares

    # Initialize I2C, and the IMU
    i2c = I2C(1, I2C.MASTER, baudrate=400000)
    imu = BNO055(i2c, Pin.cpu.B9, Pin.cpu.B8, Pin.cpu.A10)
    imu.set_mode(0x0C)

    while True:
        if test_state.get() in [1,2]:
            heading = imu.read_heading()
            heading_share.put(heading)
            #print(f" Heading: {heading}")

        else:
            heading_share.put(0)

        yield
#
def monitor_task(shares):
    pos_L, pos_R, heading_share, initial_heading_share, test_state = shares
    initial_heading = None  # Store initial heading

    while True:
        if test_state.get() == 1:  # Monitor conditions during line-following
            current_heading = heading_share.get()
            print(f" Current Heading: {current_heading}")
            left_pos = pos_L.get()
            right_pos = pos_R.get()

            if initial_heading is None:
                initial_heading = current_heading  # Store initial heading
                initial_heading_share.put(initial_heading)
                print(f"Initial Heading: {initial_heading}")


            # Check conditions for switching to bypass mode
            if ( pos_L.get() >= 110  and abs(current_heading - initial_heading - 180) < 2.5):
                print("Conditions met. Switching to grid mode.")
                test_state.put(2)  # Switch to grid mode
        elif test_state.get() == 2:
            yield
        yield

def grid_task(shares):
    eff_L, eff_R, pos_L, pos_R, heading_share, initial_heading_share, test_state = shares

    # Create State Variables
    S_INIT = 0
    S_GRID = 1
    S_TURN_RIGHT = 2
    S_WALL = 3
    S_CUP = 4
    S_HOME = 5

    # Variables for the grid task
    state = S_INIT
    BASE_SPEED = 20  # Base speed for motors
    Kp = 4
    grid_duration = 2500

    while True:
        if test_state.get() == 1:
            yield
        elif test_state.get() == 2:
            if state == S_INIT:
                print("Grid Mode Initialized")
                action_start_time = ticks_us()
                state = S_GRID


            elif state == S_GRID:
                # Target heading is 180 degrees from the initial heading
                target_heading = (initial_heading_share.get() - 180) % 360
                current_heading = heading_share.get()
                elapsed_time = ticks_diff(ticks_us(), action_start_time)/1000

                if grid_duration > elapsed_time:
                    # Calculate heading error
                    heading_error = target_heading - current_heading
                    # Normalize the heading error to the range [-180, 180]
                    if heading_error > 180:
                        heading_error -= 360
                    elif heading_error < -180:
                        heading_error += 360

                    # Use PID to calculate correction
                    correction = Kp * heading_error

                    # Set motor efforts
                    left_effort = BASE_SPEED - correction
                    right_effort = BASE_SPEED + correction

                    # Constrain efforts within range
                    left_effort = max(-100, min(100, left_effort))
                    right_effort = max(-100, min(100, right_effort))

                    eff_L.put(left_effort)
                    eff_R.put(right_effort)

                # Check if target position is reached
                else:
                    print("Grid Mode Stopped")
                    eff_L.put(0)
                    eff_R.put(0)


            elif state == S_TURN_RIGHT:
                print("Grid Mode Turned Right")
                # Rotate the robot 90 degrees
                target_heading = (initial_heading_share.get() + 90) % 360
                current_heading = heading_share.get()

                heading_error = target_heading - current_heading
                if abs(heading_error) > 2.5:
                    eff_L.put(20)
                    eff_R.put(-20)
                else:
                    eff_L.put(0)
                    eff_R.put(0)
                    state = S_GRID  # Return to grid mode

        yield







if __name__ == '__main__':
    eff_L = task_share.Share('f', thread_protect=True, name='Left Effort')
    eff_R = task_share.Share('f', thread_protect=True, name='Right Effort')
    pos_L = task_share.Share('f', thread_protect=True, name='Left Position')
    pos_R = task_share.Share('f', thread_protect=True, name='Right Position')
    vel_L = task_share.Share('f', thread_protect=True, name='Left Velocity')
    vel_R = task_share.Share('f', thread_protect=True, name='Right Velocity')
    heading_share = task_share.Share('f', thread_protect=True, name='IMU Heading')
    initial_heading_share = task_share.Share('f', thread_protect=True, name='Initial Heading')
    test_state = task_share.Share('B', thread_protect=True, name='Test State')

    # Sensor Array and PID setup
    sensor_pins = [('C0', 2815, 4095), ('C1', 1832, 4095), ('B0', 931, 4095), ('A4', 1297, 4095),
                   ('A7', 910, 4095), ('A6', 1164, 4095),('C3', 1323, 4095),('C2', 2348, 4095)]  # Replace with your calibrated values
    sensor_array = SensorArray(sensor_pins)


    # Calibrate sensors
    print("Calibrating sensors White Sensors")
    sensor_array.cal_white()
    sleep(3)
    print("Calibrating sensors Black Sensors")
    sensor_array.cal_black()
    sleep(3)
    print("Calibration complete.")

    # Reinitialize sensor array with updated values
    sensor_pins = [('C0', sensor_array.get_white(0), sensor_array.get_black(0)),
                   ('C1', sensor_array.get_white(1), sensor_array.get_black(1)),
                   ('B0', sensor_array.get_white(2), sensor_array.get_black(2)),
                   ('A4', sensor_array.get_white(3), sensor_array.get_black(3)),
                   ('A7', sensor_array.get_white(4), sensor_array.get_black(4)),
                   ('A6', sensor_array.get_white(5), sensor_array.get_black(5)),
                   ('C3', sensor_array.get_white(6), sensor_array.get_black(6)),
                   ('C2', sensor_array.get_white(7), sensor_array.get_black(7))]
    sensor_array = SensorArray(sensor_pins)

    # Task setup
    BASE_SPEED = 20
    task_left = cotask.Task(motor_task_left, name='Left Motor', priority=1, period=30, profile=True, trace=False,
                            shares=(eff_L, pos_L, vel_L, test_state))
    task_right = cotask.Task(motor_task_right, name='Right Motor', priority=1, period=30, profile=True, trace=False,
                             shares=(eff_R, pos_R, vel_R, test_state))
    task_sensor = cotask.Task(sensor_task,name = "Sensor Task",priority=1, period = 40, profile = True, trace = False,
                              shares = (eff_L, eff_R, pos_L, pos_R,heading_share, test_state  ))
    task_imu = cotask.Task(imu_task, name='IMU Task', priority=2, period = 100, profile = True, trace = False,
                            shares = (heading_share, test_state))
    task_encoder = cotask.Task(encoder_task,name = "Encoder Task",priority=1, period = 50, profile = True, trace = False,
                               shares = (pos_L, vel_R,pos_R,vel_R, test_state))
    task_user = cotask.Task(user_task, name='User', priority=2, period=100, profile=True, trace=False,
                            shares=(eff_L, eff_R, test_state))
    task_grid = cotask.Task(grid_task, name='Grid Task', priority=1, period = 30, profile=True, trace=False,
                            shares=(eff_L, eff_R, pos_L, pos_R, heading_share,initial_heading_share, test_state))
    task_monitor = cotask.Task(monitor_task, name='Monitor Task', priority=2, period = 30, profile=True, trace=False,
                               shares=(pos_L, pos_R, heading_share,initial_heading_share, test_state))

    cotask.task_list.append(task_left)
    cotask.task_list.append(task_right)
    cotask.task_list.append(task_sensor)
    cotask.task_list.append(task_grid)
    cotask.task_list.append(task_user)
    cotask.task_list.append(task_encoder)
    cotask.task_list.append(task_imu)
    cotask.task_list.append(task_monitor)



    gc.collect()

    while True:
        try:
            #print('\nTask Performance:')
            #print(cotask.task_list)
            cotask.task_list.pri_sched()
            gc.collect()
        except KeyboardInterrupt:
            break
    print('\n' + str(cotask.task_list))
    print(task_share.show_all())
