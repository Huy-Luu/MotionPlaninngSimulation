
from UTMmodule import UTMmodule as utm
import math
import numpy as np

class PathGenerator():

    def line(x0, y0, x1, y1):
        a = (y0-y1)/(x0-x1)
        b = y0 - a*x0
        return a,b

    def calcPerpendicular(x,y,a,b):
        a_p = -1/a
        b_p = y - a_p * x
        return a_p, b_p

    def intersection(a1,b1,a2,b2):
        x = (b1-b2)/(a2-a1)
        y = a1 * x + b1
        return x,y

    def distance(x1,y1,x2,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def vectorAngle(center_x, center_y, px, py):
        return math.atan2(py - center_y, px - center_x)

    def generatePath(lat, lon):
        x = []
        y = []

        for i in range (0,len(lat)):
            x_temp, y_temp = utm.fromLatlon(lat[i],lon[i])
            x.append(x_temp)
            y.append(y_temp)
        
        offset_x = x[0]
        offset_y = y[0]
            
        #offset
        for i in range(0,len(x)):
            x[i] = x[i] - offset_x
            y[i] = y[i] - offset_y
        
        print(x,y)

        line_x = []
        line_y = []
        path_x = []
        path_y = []
        ap = []
        bp = []
        end_point_each_segments = []
        arc_x = []
        arc_y = []

        #draw lines
        for i in range(0,len(x)-1):
            a, b = line(x[i], y[i], x[i+1], y[i+1])
            #print(a,b)
            #length = math.sqrt((x[i]-x[i+1])**2 + (y[i]- y[i+1])**2)
            length = distance(x[i], y[i], x[i+1], y[i+1])
            segments = int(length * 10)
            x_delta = (x[i+1] - x[i])/ segments
            y_delta = (y[i+1] - y[i])/ segments
            for j in range(0,segments):
                #line_y.append(a*line_x[j] + b)
                line_x.append(x[i] + j * x_delta)
                line_y.append(y[i] + j * y_delta)

            path_y = np.append(path_y, line_y)
            path_x = np.append(path_x, line_x)
            end_point_each_segments.append(len(path_x))

            a_p, b_p = calcPerpendicular(line_x[10], line_y[10], a, b)
            ap.append(a_p)
            bp.append(b_p)
            arc_x.append(line_x[10])
            arc_y.append(line_y[10])
            a_p, b_p = calcPerpendicular(line_x[len(line_x)-10], line_y[len(line_y)-10], a, b)
            ap.append(a_p)
            bp.append(b_p)
            arc_x.append(line_x[len(line_x)-10])
            arc_y.append(line_y[len(line_y)-10])

            #print(line_x[10], line_y[10])
            #print(line_x[len(line_x)-10], line_y[len(line_y)-10])

            line_y.clear()
            line_x.clear()


        #print(ap, bp)
        #draw arc
        centers_x = []
        centers_y = []
        radiuses = []
        angles = []
        for i in range(1,len(ap)-2,2):
            center_x, center_y = intersection(ap[i], bp[i], ap[i+1], bp[i+1])
            centers_x.append(center_x)
            centers_y.append(center_y)
            radius = distance(center_x, center_y, arc_x[i], arc_y[i])
            radiuses.append(radius)

            angle = vectorAngle(center_x, center_y,arc_x[i], arc_y[i])
            angles.append(angle)
            angle = vectorAngle(center_x, center_y,arc_x[i+1], arc_y[i+1])
            angles.append(angle)

        path_arc_x = []
        path_arc_y = []

        print(angles)

        for i in range(0,len(angles),2):
            delta = angles[i+1] - angles[i]

            if(abs(delta)>math.radians(180)):
                if(angles[i]>0):
                    angles[i+1] = angles[i+1] + math.radians(360)
                    delta = angles[i+1] - angles[i]

                if(angles[i]<0):
                    angles[i+1] = angles[i+1] - math.radians(360)
                    delta = angles[i+1] - angles[i]

            segment = delta/20

            current_step = angles[i]
            for j in range(0,20):
                p_arc_x = radiuses[int(i/2)]*math.cos(current_step) + centers_x[int(i/2)]
                p_arc_y = radiuses[int(i/2)]*math.sin(current_step) + centers_y[int(i/2)]
                path_arc_x.append(p_arc_x)
                path_arc_y.append(p_arc_y)
                current_step = current_step + segment

        for i in range(0,len(end_point_each_segments)-1):
            path_x[end_point_each_segments[i]-10:end_point_each_segments[i]+10] = path_arc_x[20*i:20*i+20]
            path_y[end_point_each_segments[i]-10:end_point_each_segments[i]+10] = path_arc_y[20*i:20*i+20]

        yaw = []
        for i in range(0,len(path_x)-1):
            yaw_temp = math.atan2(path_y[i+1]-path_y[i], path_x[i+1] - path_x[i])
            yaw.append(yaw_temp)

        yaw_temp = yaw[len(yaw)-1]
        yaw.append(yaw_temp)

        return path_x, path_y, yaw
