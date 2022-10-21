
class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX():
        return self.x

    def getY():
        return self.y

class OriginalPoint(object):
    def __init__(self, latlon):
        data = latlon.split(",")
        self.lat = float(data[0])
        self.lon = float(data[1])

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon