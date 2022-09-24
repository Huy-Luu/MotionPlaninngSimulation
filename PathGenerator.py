
from pathlib import Path
from UTMmodule import UTMmodule
import math
import numpy as np
from Point import OriginalPoint
from Point import Point

class PathGenerator():

    def line(p0, p1):
        a = (p0.y - p1.y)/(p0.x - p1.x)
        b = p0.y - a*p0.x
        return a,b

    def calcPerpendicular(p,a,b):
        a_p = -1/a
        b_p = p.y - a_p * p.x
        return a_p, b_p

    def intersection(a1,b1,a2,b2):
        x = (b1-b2)/(a2-a1)
        y = a1 * x + b1
        p = Point(x, y)
        return p

    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def vectorAngle(center, p):
        return math.atan2(p.y - center.y, p.x - center.x)

    def printPoint(p):
        print(p.x, p.y)

    @staticmethod
    def generatePath(og_points, utm):
        cv_points = []

        for i in range (0,len(og_points)):
            #print(og_points[i].getLat(), og_points[i].getLon())
            x_temp, y_temp = utm.fromLatlon(og_points[i].getLat(), og_points[i].getLon())
            cv_points.append(Point(x_temp, y_temp))
        
        offset_x = cv_points[0].x
        offset_y = cv_points[0].y
            
        #offset
        for i in range(0,len(cv_points)):
            cv_points[i].x = cv_points[i].x - offset_x
            cv_points[i].y = cv_points[i].y - offset_y
            #PathGenerator.printPoint(cv_points[i])
            #print(cv_points[i].x, cv_points[i].y)

        line = []
        path = []
        ap = []
        bp = []
        end_point_each_segments = []
        arc = []

        #draw lines
        for i in range(0,len(cv_points)-1):
            a, b = PathGenerator.line(cv_points[i], cv_points[i+1])
            #print(a,b)
            #length = math.sqrt((x[i]-x[i+1])**2 + (y[i]- y[i+1])**2)
            length = PathGenerator.distance(cv_points[i], cv_points[i+1])
            segments = int(length * 10)
            x_delta = (cv_points[i+1].x - cv_points[i].x)/ segments
            y_delta = (cv_points[i+1].y - cv_points[i].y)/ segments
            for j in range(0, segments):
                line.append(Point(cv_points[i].x + j * x_delta, cv_points[i].y + j * y_delta))
                #PathGenerator.printPoint(line[j])
            
            path = np.append(path, line)
        
            #for i in range(0, len(path)):
                #PathGenerator.printPoint(path[i])

            end_point_each_segments.append(len(path)) # as the name suggested

            a_p, b_p = PathGenerator.calcPerpendicular(line[10], a, b)
            ap.append(a_p)
            bp.append(b_p)

            arc.append(Point(line[10].x, line[10].y))

            a_p, b_p = PathGenerator.calcPerpendicular(line[len(line) - 10], a, b)
            ap.append(a_p)
            bp.append(b_p)

            arc.append(Point(line[len(line) - 10].x, line[len(line) - 10].y))
            #for i in range(0, len(arc)):
            #    PathGenerator.printPoint(arc[i])

            line.clear()

        centers = []
        radiuses = []
        angles = []
        for i in range(1, len(ap) - 2, 2):
            #print(ap[i])
            center = PathGenerator.intersection(ap[i], bp[i], ap[i+1], bp[i+1])
            centers.append(center)
            radius = PathGenerator.distance(center, arc[i])
            radiuses.append(radius)

            angle = PathGenerator.vectorAngle(center, arc[i])
            print(angle)
            angles.append(angle)
            angle = PathGenerator.vectorAngle(center, arc[i+1])
            print(angle)
            angles.append(angle)

        path_arc = []

        print("Angles are: " + str(angles))
            