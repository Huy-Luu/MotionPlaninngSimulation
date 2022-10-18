from StanleyController import StanleyController
from SlidingWindow import SlidingWindow
import matplotlib.pyplot as plt

class Simulation:
    
    @staticmethod
    def simulate(vehicle, dt, max_sim_time, target_speed, scontroller, sw, target_idx, last_idx, path, yaw, show_animation):
        time = 0.0
        cx, cy = zip(*[(float(i.x),float(i.y)) for i in path])
        while max_sim_time >= time and last_idx > target_idx:
            di, target_idx = scontroller.stanleyControl(vehicle, path, yaw, target_idx)
            vehicle.update(di, dt)

            time += dt

            # print(vehicle.x, vehicle.y, vehicle.yaw)

            if show_animation:
                plt.cla()
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                    lambda event: [exit(0) if event.key == 'escape' else None])
                vehicle.plot(plt, vehicle.x, vehicle.y, vehicle.yaw)
                sw.plot(plt)
                plt.plot(cx, cy, ".r", label="course")
                plt.plot(cx[target_idx], cy[target_idx], "xg", label="target")
                plt.axis("equal")
                plt.grid(True)
                plt.title("Speed[km/h]:" + str(vehicle.v * 3.6)[:4])
                plt.pause(0.001)




