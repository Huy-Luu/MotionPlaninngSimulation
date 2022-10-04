import numpy as np
import math

class StanleyController:
    k = 0.5  # control gain
    Kp = 1.0  # speed proportional gain
    L = 0.29  # [m] Wheel base of vehicle
    max_steer = np.radians(30.0)  # [rad] max steering angle

    def __init__(self):
        print("Initiated a Controller")

    def steeringBoundary(self, angle):
        if angle > self.max_steer:
            angle = self.max_steer
        elif angle < (-1 * self.max_steer):
            angle = -1 * self.max_steer
        return angle

    def steeringMapping(self, angle):
        angle = math.degrees(angle)
        remains = angle % 10
        angle = angle - remains
        return math.radians(angle)

    def stanleyControl(self, vehicle, cx, cy, cyaw, last_target_idx):

        current_target_idx, error_front_axle = self.calcTargetIndex(vehicle, cx, cy)

        if last_target_idx >= current_target_idx:
            current_target_idx = last_target_idx

        # theta_e corrects the heading error
        theta_e = self.normalizeAngle(cyaw[current_target_idx] - vehicle.yaw)
        # theta_d corrects the cross track error
        theta_d = np.arctan2(self.k * error_front_axle, vehicle.v)
        # Steering control
        delta = theta_e + theta_d

        delta = self.steeringBoundary(delta)
        delta = self.steeringMapping(delta)

        print(math.degrees(delta))

        return delta, current_target_idx


    def normalizeAngle(self, angle):
        while angle > np.pi:
            angle -= 2.0 * np.pi

        while angle < -np.pi:
            angle += 2.0 * np.pi

        return angle


    def calcTargetIndex(vehicle, cx, cy):
        # Calc front axle position
        fx = vehicle.x + vehicle.WB * np.cos(vehicle.yaw)
        fy = vehicle.y + vehicle.WB * np.sin(vehicle.yaw)

        # Search nearest point index
        dx = [fx - icx for icx in cx]
        dy = [fy - icy for icy in cy]
        d = np.hypot(dx, dy)
        target_idx = np.argmin(d)

        # Project RMS error onto front axle vector
        front_axle_vec = [-np.cos(vehicle.yaw + np.pi / 2),
                        -np.sin(vehicle.yaw + np.pi / 2)]
        error_front_axle = np.dot([dx[target_idx], dy[target_idx]], front_axle_vec)

        return target_idx, error_front_axle