from http import client
from StanleyController import StanleyController
from SlidingWindow import SlidingWindow
from MQTTclient import MQTTclient
from Point import Point
from SteeringMappingSender import SteeingMappingSender
import matplotlib.pyplot as plt
import time as t
import threading

class Simulation:

    def simulate(vehicle, dt, max_sim_time, target_speed, client, scontroller, shandler, sw, utmmodule, target_idx, last_idx, og_points, path, waypoints, waypoint_indices, offset, yaw, show_animation):
        try:
            global info
            info = "test"
            time = 0.0
            count = 0
            wp_arr_flag = 0
            wp_no_arrived = 1
            wp_about_to_arrive = 1

            f = open(r"E:/New folder/BK/HK221/Luan_van_tot_nghiep/Software/MotionPlaninngSimulation/real_data.txt", "a")
            f.write("Waypoints" + '\r')
            for i in range(0, len(og_points)):
                f.write(str(og_points[i].getLat()) + str(og_points[i].getLon()) + '\r')
            f.write("Positions" + '\r')

            cx, cy = zip(*[(float(i.x),float(i.y)) for i in path])
            wpx, wpy = zip(*[(float(wp.x),float(wp.y)) for wp in waypoints])
            shandler.send("t") # update continuously
            vehicle.x, vehicle.y, vehicle.v, vehicle.yaw = shandler.receiveFourInputs()
            while max_sim_time >= time and last_idx > target_idx:
                di, target_idx = scontroller.stanleyControl(vehicle, path, yaw, target_idx)
                SteeingMappingSender.sendMapped(shandler, di)
                
                #Replace vehicle update with reading data
                #vehicle.update(di, dt)
                shandler.send("t") # update continuously
                vehicle.x, vehicle.y, vehicle.v, vehicle.yaw = shandler.receiveFourInputs()
                lat=vehicle.x
                lon = vehicle.y
                print("Got data")
                f.write(str(vehicle.x) + "," + str(vehicle.y) + "," + str(vehicle.v) + "," + str(vehicle.yaw) + ","  + '\r')

                x,y =utmmodule.fromLatlon(vehicle.x, vehicle.y)
                vehicle.x = x - offset.x
                vehicle.y = y - offset.y
                point_to_send = Point(lat, lon)
                message = str(point_to_send.getY()) + "," + str(point_to_send.getX()) + "," + str(wp_arr_flag) + "," + str(wp_no_arrived) + "," + str(wp_about_to_arrive) + "," + "3.0" + "," + "180.0"
                client.publish(message, "data/position")

                print("Done processing")

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
                    f.write("Reached Waypoint" + '\r')
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
            f.write(str(vehicle.x) + "," + str(vehicle.y) + "," + str(vehicle.v) + "," + str(vehicle.yaw) + ","  + '\r')

        except KeyboardInterrupt:
            print("Stopped the current path")
