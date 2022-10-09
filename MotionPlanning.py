from StanleyController import StanleyController
import numpy as np
import matplotlib.pyplot as plt
from Vehicle import Vehicle
from UTMmodule import UTMmodule
from Point import OriginalPoint
from PathGenerator import PathGenerator
from StanleyController import StanleyController
from Simulation import Simulation

dt = 0.1

print("Init car")
vehicle = Vehicle(0.0, 0.0, 0.0, 0.833, 30)
scontroller = StanleyController()

#Initiate a set of original points
og_points = []
#vehicle.plotCar(1.0, 1.0, 1.0)
#op1 = OriginalPoint(10.772580, 106.658847)
#op2 = OriginalPoint(10.773004, 106.659656)
#op3 = OriginalPoint(10.772529, 106.659708)
og_points.append(OriginalPoint(10.772580, 106.658847))
og_points.append(OriginalPoint(10.773004, 106.659656))
og_points.append(OriginalPoint(10.772529, 106.659708))
og_points.append(OriginalPoint(10.772640, 106.659920))

path_generator_instance  = PathGenerator()
utm = UTMmodule()

path, yaw = path_generator_instance.generatePath(og_points, utm)

path_x = []
path_y = []

for i in range(len(path)):
    path_x.append(path[i].x)
    path_y.append(path[i].y)

# plt.plot(path_x, path_y, ".r", label="course")
# plt.show()
last_idx = len(path_x) -1
target_idx, _ = scontroller.calcTargetIndex(vehicle, path_x, path_y)
print(target_idx)

Simulation.simulate(vehicle, dt, 500, 3, scontroller, target_idx, last_idx, path_x, path_y, yaw, 1)


#print("Point 1: " + str(op1.getLat()) + " and " + str(op1.getLon()))
# print(UTMmodule.zone_number_to_central_longitude(2))
print("Plotted car")
