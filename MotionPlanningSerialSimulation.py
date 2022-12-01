from enum import Flag
from SlidingWindow import SlidingWindow
from StanleyController import StanleyController
import numpy as np
import matplotlib.pyplot as plt
from Vehicle import Vehicle
from UTMmodule import UTMmodule
from Point import OriginalPoint
from Point import Point
from PathGenerator import PathGenerator
from StanleyController import StanleyController
from MQTTclient import MQTTclient
from SerialDataHandler import SerialDataHandler
from Simulation_3 import Simulation


dt = 0.1

print("Init car")
vehicle = Vehicle(0.0, 0.0, 0.0, 1.388, 30)
scontroller = StanleyController()
sw = SlidingWindow(10)
shandler = SerialDataHandler('COM1', 115200)
client = MQTTclient("broker.hivemq.com", 1883, "SimulationCart")
client.init("control/auto")


og_points = []
og_points.append(OriginalPoint("10.772998,106.659779"))
og_points.append(OriginalPoint("10.772829,106.659798"))
og_points.append(OriginalPoint("10.772861,106.660020"))
og_points.append(OriginalPoint("10.773066,106.659999"))
og_points.append(OriginalPoint("10.772998,106.659779"))

# og_points.append(OriginalPoint("106.659779,10,772998"))
# og_points.append(OriginalPoint("106.659798,10.772829"))
# og_points.append(OriginalPoint("106.660020,10.772861"))
# og_points.append(OriginalPoint("106.659999,10.773066"))
# og_points.append(OriginalPoint("106.659779,10,772998"))

path_generator_instance  = PathGenerator()
utm = UTMmodule()

path, yaw, waypoint_indices, offset = path_generator_instance.generatePath(og_points, utm)

#print("Type of path: " + str(type(path)))

path_x = []
path_y = []
waypoints = []
waypoints_x = []
waypoints_y = []

for i in range(0, len(waypoint_indices)):
    waypoints.append(path[waypoint_indices[i] - 1])
    waypoints_x.append(waypoints[i].x)
    waypoints_y.append(waypoints[i].y)
    #print(waypoints[i].x, waypoints[i].y)


for i in range(len(path)):
    path_x.append(path[i].x)
    path_y.append(path[i].y)

# plt.plot(path_x, path_y, ".r", label="course")
# plt.show()
last_idx = len(path_x) -1
target_idx, _ = scontroller.calcTargetIndex(vehicle, path, 0)
print(target_idx)

#Simulation.simulate(vehicle, dt, 500, 3, client, scontroller, sw, utm, target_idx, last_idx, path, waypoints, waypoint_indices, offset, yaw, True)

Simulation.simulate(
    vehicle = vehicle,
    dt=dt,
    max_sim_time=500,
    target_speed=3,
    client=client,
    scontroller=scontroller,
    shandler=shandler,
    sw=sw,
    utmmodule=utm,
    target_idx=target_idx,
    last_idx=last_idx,
    og_points=og_points,
    path=path,
    waypoints=waypoints,
    waypoint_indices=waypoint_indices,
    offset=offset,
    yaw=yaw,
    show_animation=True
)

