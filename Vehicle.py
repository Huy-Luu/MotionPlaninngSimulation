import numpy as np
import math
import matplotlib.pyplot as plt

k = 0.5  # control gain
Kp = 1.0  # speed proportional gain
dt = 0.1  # [s] time difference
L = 0.29  # [m] Wheel base of vehicle
max_steer = np.radians(30.0)  # [rad] max steering angle

# Vehicle parameters
LENGTH = 0.41  # [m]
WIDTH = 0.36  # [m]
BACKTOWHEEL = 0.03  # [m]
WHEEL_LEN = 0.13  # [m]
WHEEL_WIDTH = 0.015  # [m]
TREAD = 0.33  # [m]
WB = 0.29  # [m]

class Vehicle (object):
    def __init__ (self, x = 0.0, y = 0.0, yaw = 0.0, v = 0.0, max_steer = 30.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.max_steer = max_steer
        print("Position: " + str(self.getX()) + " and " + str(self.getY()))
        
    def plotCar(self, x, y, yaw, steer=0.0, cabcolor="-r", truckcolor="-k"):
        outline = np.array([[-BACKTOWHEEL, (LENGTH - BACKTOWHEEL), (LENGTH - BACKTOWHEEL), -BACKTOWHEEL, -BACKTOWHEEL],
                            [WIDTH / 2, WIDTH / 2, - WIDTH / 2, -WIDTH / 2, WIDTH / 2]])

        fr_wheel = np.array([[WHEEL_LEN, -WHEEL_LEN, -WHEEL_LEN, WHEEL_LEN, WHEEL_LEN],
                                [-WHEEL_WIDTH - TREAD, -WHEEL_WIDTH - TREAD, WHEEL_WIDTH - TREAD, WHEEL_WIDTH - TREAD, -WHEEL_WIDTH - TREAD]])

        rr_wheel = np.copy(fr_wheel)

        fl_wheel = np.copy(fr_wheel)
        fl_wheel[1, :] *= -1
        rl_wheel = np.copy(rr_wheel)
        rl_wheel[1, :] *= -1

        Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                            [-math.sin(yaw), math.cos(yaw)]])
        Rot2 = np.array([[math.cos(steer), math.sin(steer)],
                            [-math.sin(steer), math.cos(steer)]])

        fr_wheel = (fr_wheel.T.dot(Rot2)).T
        fl_wheel = (fl_wheel.T.dot(Rot2)).T
        fr_wheel[0, :] += WB
        fl_wheel[0, :] += WB

        fr_wheel = (fr_wheel.T.dot(Rot1)).T
        fl_wheel = (fl_wheel.T.dot(Rot1)).T

        outline = (outline.T.dot(Rot1)).T
        rr_wheel = (rr_wheel.T.dot(Rot1)).T
        rl_wheel = (rl_wheel.T.dot(Rot1)).T

        print(x)

       # print(outline[0, :])
        outline[0, :] += self.x
        outline[1, :] += self.y
        fr_wheel[0, :] += self.x
        fr_wheel[1, :] += self.y
        rr_wheel[0, :] += self.x
        rr_wheel[1, :] += self.y
        fl_wheel[0, :] += self.x
        fl_wheel[1, :] += self.y
        rl_wheel[0, :] += self.x
        rl_wheel[1, :] += self.y

        outline[0, :] = np.add(outline[0, :], x)
        outline[1, :] += y
        fr_wheel[0, :] += x
        fr_wheel[1, :] += y
        rr_wheel[0, :] += x
        rr_wheel[1, :] += y
        fl_wheel[0, :] += x
        fl_wheel[1, :] += y
        rl_wheel[0, :] += x
        rl_wheel[1, :] += y

        plt.plot(np.array(outline[0, :]).flatten(),
                    np.array(outline[1, :]).flatten(), truckcolor)
        plt.plot(np.array(fr_wheel[0, :]).flatten(),
                    np.array(fr_wheel[1, :]).flatten(), truckcolor)
        plt.plot(np.array(rr_wheel[0, :]).flatten(),
                    np.array(rr_wheel[1, :]).flatten(), truckcolor)
        plt.plot(np.array(fl_wheel[0, :]).flatten(),
                    np.array(fl_wheel[1, :]).flatten(), truckcolor)
        plt.plot(np.array(rl_wheel[0, :]).flatten(),
                    np.array(rl_wheel[1, :]).flatten(), truckcolor)
        plt.plot(x, y, "*")
        plt.show()

    def update(self, acceleration, delta, dt):
        delta = np.clip(delta, -max_steer, max_steer)

        self.x += self.v * np.cos(self.yaw) * dt
        self.y += self.v * np.sin(self.yaw) * dt
        self.yaw += self.v / L * np.tan(delta) * dt
        self.yaw = normalize_angle(self.yaw)
        self.v += acceleration * dt

    def getX(self):
        return self.x

    def getY(self):
        return self.y

