from http import client
from StanleyController import StanleyController
from SlidingWindow import SlidingWindow
from MQTTclient import MQTTclient
from Point import Point
import numpy as np
import matplotlib.pyplot as plt
import time as t
import threading

class Simulation:

    def mainSimulationThread(vehicle, dt, max_sim_time, target_speed, client, scontroller, sw, utmmodule, target_idx, last_idx, path, waypoints, waypoint_indices, offset, yaw, show_animation):
        try:
            #write to file for testing real life situation
            f = open("E:\\New folder\BK\HK221\Luan_van_tot_nghiep\Software\MotionPlaninngSimulation\data.txt", 'a')


            global info
            info = "test"
            time = 0.0
            count = 0
            wp_arr_flag = 0
            wp_no_arrived = 1
            wp_about_to_arrive = 1
            cx, cy = zip(*[(float(i.x),float(i.y)) for i in path])
            wpx, wpy = zip(*[(float(wp.x),float(wp.y)) for wp in waypoints])
            while max_sim_time >= time and last_idx > target_idx:
                di, target_idx = scontroller.stanleyControl(vehicle, path, yaw, target_idx)
                vehicle.update(di, dt)

                x, y =utmmodule.toLatLon(vehicle.x + offset.x, vehicle.y + offset.y, 48, zone_letter="N")
                f.write(str(x) + "," + str(y) + "," + str(vehicle.v) + "," + str(np.degrees(vehicle.yaw)) + ","  + '\r')
                
                point_to_send = Point(x, y)
                message = str(point_to_send.getY()) + "," + str(point_to_send.getX()) + "," + str(wp_arr_flag) + "," + str(wp_no_arrived) + "," + str(wp_about_to_arrive) + "," + "3.0" + "," + "180.0"
                client.publish(message, "data/position")

                if(info == "f"):
                    vehicle.v = 0
                else:
                    vehicle.v = 1.83

                if(target_idx > waypoint_indices[count]):
                    wp_arr_flag = 1
                    wp_no_arrived += 1
                    wp_about_to_arrive += 1
                    message = str(point_to_send.getY()) + "," + str(point_to_send.getX()) + "," + str(wp_arr_flag) + "," + str(wp_no_arrived) + "," + str(wp_about_to_arrive) + "," + "3.0" + "," + "180.0"
                    client.publish(message, "data/position")
                    print("REACHED WAYPOINT")
                    t.sleep(3)
                    count+=1

                wp_arr_flag = 0
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

            wp_arr_flag = 1
            wp_no_arrived += 1
            wp_about_to_arrive += 1
            message = str(point_to_send.getY()) + "," + str(point_to_send.getX()) + "," + str(wp_arr_flag) + "," + str(wp_no_arrived) + "," + str(wp_about_to_arrive) + "," + "3.0" + "," + "180.0"
            client.publish(message, "data/position")

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
    def simulate(vehicle, dt, max_sim_time, target_speed, client, scontroller, sw, utmmodule, target_idx, last_idx, path, waypoints, waypoint_indices, offset, yaw, show_animation):
        info = ""
        
        SimulationThread = threading.Thread(target = Simulation.mainSimulationThread, args =(vehicle, dt, max_sim_time, target_speed, client, scontroller, sw, utmmodule, target_idx, last_idx, path, waypoints, waypoint_indices, offset, yaw, show_animation))
        CommunicationThread  = threading.Thread(target = Simulation.communicationThread, args = (client,))

        #SimulationThread.setDaemon(True)
        CommunicationThread.setDaemon(True)

        SimulationThread.start()
        CommunicationThread.start()

