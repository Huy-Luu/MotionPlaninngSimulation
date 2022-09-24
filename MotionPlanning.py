import numpy as np
from Vehicle import Vehicle
from UTMmodule import UTMmodule
from Point import OriginalPoint
from PathGenerator import PathGenerator


print("Init car")
vehicle = Vehicle(0.0, 0.0, 0.0, 0.0, 30)

#Initiate a set of original points
og_points = []
#vehicle.plotCar(1.0, 1.0, 1.0)
#op1 = OriginalPoint(10.772580, 106.658847)
#op2 = OriginalPoint(10.773004, 106.659656)
#op3 = OriginalPoint(10.772529, 106.659708)
og_points.append(OriginalPoint(10.772580, 106.658847))
og_points.append(OriginalPoint(10.773004, 106.659656))
og_points.append(OriginalPoint(10.772529, 106.659708))
#og_points.append(OriginalPoint(10.772640, 106.659920))

path_generator_instance  = PathGenerator()
utm = UTMmodule()

path_generator_instance.generatePath(og_points, utm)



#print("Point 1: " + str(op1.getLat()) + " and " + str(op1.getLon()))
# print(UTMmodule.zone_number_to_central_longitude(2))
print("Plotted car")
