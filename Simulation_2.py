from http import client
from StanleyController import StanleyController
from SlidingWindow import SlidingWindow
from MQTTclient import MQTTclient
import matplotlib.pyplot as plt
import time as t
import threading

class Simulation:

    def mainSimulationThread(vehicle, dt, max_sim_time, target_speed, scontroller, sw, target_idx, last_idx, path, waypoints, waypoint_indices, yaw, show_animation):
        try:
            global info
            info = "test"

            time = 0.0
            count = 0
            cx, cy = zip(*[(float(i.x),float(i.y)) for i in path])
            wpx, wpy = zip(*[(float(wp.x),float(wp.y)) for wp in waypoints])
            while max_sim_time >= time and last_idx > target_idx:
                di, target_idx = scontroller.stanleyControl(vehicle, path, yaw, target_idx)
                vehicle.update(di, dt)

                if(info == "f"):
                    vehicle.v = 0
                else:
                    vehicle.v = 1.83

                if(target_idx > waypoint_indices[count]):
                    print("REACHED WAYPOINT")
                    t.sleep(2)
                    count+=1

                time += dt

                #print(vehicle.x, vehicle.y, vehicle.yaw)

                if show_animation:
                    plt.cla()
                    # for stopping simulation with the esc key.
                    plt.gcf().canvas.mpl_connect('key_release_event',
                        lambda event: [exit(0) if event.key == 'escape' else None])
                    vehicle.plot(plt, vehicle.x, vehicle.y, vehicle.yaw)
                    plt.plot(cx, cy, ".r", label="course")
                    sw.plot(plt, path, vehicle, target_idx)
                    plt.plot(wpx, wpy, ".g")
                    plt.plot(cx[target_idx], cy[target_idx], "xg", label="target")
                    plt.axis("equal")
                    plt.grid(True)
                    plt.title("Speed[km/h]:" + str(vehicle.v * 3.6)[:4] + " " + info)
                    plt.pause(0.001)

        except KeyboardInterrupt:
            print("Stopped the current path")

    def communicationThread(mqttclient):
        global info
        info = "test"
        while(True):
            info = input("Write something")
            print(info)
            if(info == "w"):
                mqttclient.writeMessageArray()
            t.sleep(1)
    
    @staticmethod
    def simulate(vehicle, dt, max_sim_time, target_speed, client, scontroller, sw, target_idx, last_idx, path, waypoints, waypoint_indices, yaw, show_animation):
        info = ""
        
        SimulationThread = threading.Thread(target = Simulation.mainSimulationThread, args =(vehicle, dt, max_sim_time, target_speed, scontroller, sw, target_idx, last_idx, path, waypoints, waypoint_indices, yaw, show_animation))
        CommunicationThread  = threading.Thread(target = Simulation.communicationThread, args = (client,))

        #SimulationThread.setDaemon(True)
        CommunicationThread.setDaemon(True)

        SimulationThread.start()
        CommunicationThread.start()


