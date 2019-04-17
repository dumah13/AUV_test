from control.pid.pid_itf import IPID
from sensors.depth.depth_itf import IDepthSensor
from threading import Thread, Lock
import time

UP_MARGIN = 0.04

class PID(IPID):
    def __init__(self,
                 set_engine_driver_fun,
                 get_depth_fun,
                 ahrs,
                 loop_delay,
                 main_logger=None,
                 local_log=False,
                 log_directory="",
                 log_timing=0.5,
                 kp=0.5,
                 ki=0.0,
                 kd=0.0):
        # moze parametry z pliku?
        '''
        Set linear velocity as 100% of engines power
        @param set_engine_driver_fun: reference to _set_engine_driver_values
                in Movements object (see movments_itf.py)
        @param get_depth_fun: reference to method returning depth
                (see get_depth in sensor/depth/depth_itf.py)
        @param ahrs: reference to AHRS object
                (see AHRS in sensors/ahrs/ahrs_itf.py)
        '''
        super().__init__(main_logger, local_log, log_directory, log_timing)
        self.set_engine_driver_fun = set_engine_driver_fun
        self.get_depth_fun = get_depth_fun
        self.ahrs = ahrs
        self.sample_time = loop_delay
        self.pid_loop_lock = Lock()
        self.close_bool = False

        self.current_time = time.time()
        self.last_time = self.current_time
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.clear()

    def clear(self):
        '''
        Clears all PID variables and SetPoint.
        '''
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 20.0
        self.output = 0.0

    def update(self, feedback_value):
        '''
        Calculate PID for given feedback.
        Result is stored in PID.output.
        '''
        error = self.SetPoint - feedback_value

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (
                self.Kd * self.DTerm)

    def run(self):
        super().run()
        thread = Thread(target=self.pid_loop)
        thread.run()

    def close(self):
        super().close()
        with self.pid_loop_lock:
            self.close_bool = True

    def hold_depth(self):
        self.SetPoint = self.get_depth_fun()

    def set_depth(self, depth):
        self.SetPoint = depth

    def pid_loop(self):
        while True:
            self.update(self.get_depth_fun())
            time.sleep(self.sample_time)
            with self.pid_loop_lock:
                if self.close_bool:
                    break

    @staticmethod
    def val_to_range(val):
        if val < -1.0:
            return -1.0
        if val > 1.0:
            return 1.0
        return val

    def set_velocities(self, front=0, right=0, up=0, roll=0, pitch=0, yaw=0):
        if up<UP_MARGIN and up > -UP_MARGIN:
            self.set_engine_driver_fun(front, right, up, roll, pitch, yaw)
        else:
            self.set_engine_driver_fun(front, right, self.val_to_range(self.output), roll, pitch, yaw)
