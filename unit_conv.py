import math

class UnitConversion:
    def __init__(self, lon1, lat1, lon2, lat2):
        self.lon1 = lon1
        self.lat1 = lat1
        self.lon2 = lon2
        self.lat2 = lat2
        self.lon1Rads = math.radians(lon1)
        self.lat1Rads = math.radians(lat1)
        self.lon2Rads = math.radians(lon2)
        self.lat2Rads = math.radians(lat2)
         
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        radOfEarth = 6378.137
        dLat = math.radians(lat2) - math.radians(lat1)
        dLon = math.radians(lon2) - math.radians(lon1) 
        a = math.sin(dLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distanceMetres = radOfEarth * c * 1000 
        return distanceMetres 
    
    def metres_min_maxes(self):
        deltaX = self.haversine_distance(self.lon1Rads, self.lat1Rads, self.lon2Rads, self.lat1Rads)
        deltaY = self.haversine_distance(self.lon1Rads, self.lat1Rads, self.lon1Rads, self.lat2Rads)          
        self.xMin, self.yMin = 0, 0
        self.xMax, self.yMax = deltaX, deltaY
        
        return self.xMin, self.yMin, self.xMax, self.yMax
    
    def relative_xy_to_LongLat(self, x, y):
        deltaLon = (((x - self.xMin) * (self.lon2 - self.lon1)) / (self.xMax - self.xMin)) + self.lon1
        deltaLat = (((y - self.yMin) * (self.lat2 - self.lat1)) / (self.yMax - self.yMin)) + self.lat1
        
        newLon = self.lon1 + deltaLon
        newLat = self.lat1 + deltaLat
        
        return newLon, newLat

