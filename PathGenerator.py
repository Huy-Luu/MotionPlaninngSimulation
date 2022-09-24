
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

    def vectorAngle(center_x, center_y, px, py):
        return math.atan2(py - center_y, px - center_x)

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
            PathGenerator.printPoint(cv_points[i])
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
                PathGenerator.printPoint(line[j])
            