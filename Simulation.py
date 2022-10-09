from StanleyController import StanleyController
import matplotlib.pyplot as plt

class Simulation:
    
    @staticmethod
    def simulate(vehicle, dt, max_sim_time, target_speed, scontroller, target_idx, last_idx, cx, cy, cyaw, show_animation):
        time = 0.0
        while max_sim_time >= time and last_idx > target_idx:
            di, target_idx = scontroller.stanleyControl(vehicle, cx, cy, cyaw, target_idx)
            vehicle.update(di, dt)

            time += dt

            print(vehicle.x, vehicle.y, vehicle.yaw)

            if show_animation:
                plt.cla()
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                    lambda event: [exit(0) if event.key == 'escape' else None])
                vehicle.plot(plt, vehicle.x, vehicle.y, vehicle.yaw)
                plt.plot(cx, cy, ".r", label="course")
                plt.plot(cx[target_idx], cy[target_idx], "xg", label="target")
                plt.axis("equal")
                plt.grid(True)
                plt.title("Speed[km/h]:" + str(vehicle.v * 3.6)[:4])
                plt.pause(0.001)




