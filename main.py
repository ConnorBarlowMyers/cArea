import time
import math
import random

#from unit_conv import UnitConversion
from data_vis import Visualiser
from gridbased_data_generator import GridBasedCAreaMaker


xMin, yMin = 0, 0
xMax, yMax = 1000, 1000
rCircles = 10
maxPlacementAttemptsPerCArea = 100
maxPlacementForGridSweep = 10

class cAreaMaker:
    
    def __init__(self, 
                 someSats, 
                 xMin, xMax, yMin, yMax, 
                 radiusOfEachCircle,
                 maxPlacementAttemptsPerCArea, 
                 maxPlacementForGridSweep,
                 preProcessing = False):
        
        if 10 <= someSats < 20:
            noAreas = 2
            itemsPArea = 1
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 20 <= someSats < 50:
            noAreas = 4
            itemsPArea = 2
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 50 <= someSats < 100:
            noAreas = 5
            itemsPArea = 2
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 100 <= someSats < 500:
            noAreas = 10
            itemsPArea = 2
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 500 <= someSats < 1000:
            noAreas = 20
            itemsPArea = 2
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 1000 <= someSats < 5000:
            noAreas = 30
            itemsPArea = 3
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 5000 <= someSats < 10000:
            noAreas = 40
            itemsPArea = 3
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if 10000 <= someSats < 100000:
            noAreas = 50
            itemsPArea = random.randint(2, 4)
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        if someSats >= 100000:
            noAreas = 100
            itemsPArea = random.randint(2, 6)
            itemValue = math.floor(someSats / (noAreas * itemsPArea))
        

        
        startTime = time.time()
        self.data = GridBasedCAreaMaker(
                           noAreas, 
                           itemsPArea,
                           itemValue,
                           radiusOfEachCircle, 
                           xMin, xMax, 
                           yMin, yMax, 
                           maxPlacementAttemptsPerCArea, 
                           maxPlacementForGridSweep,
                           dictPreProcessing = preProcessing)
        endTime = time.time()
        
        self.placementTime = (endTime - startTime)
    
        self.return_cAreas()
        
    def return_cAreas(self):
        return self.data
        
    
  
cAreas = cAreaMaker(100001, xMin, xMax, yMin, yMax, rCircles, 
                    maxPlacementAttemptsPerCArea, maxPlacementForGridSweep)

print("Time taken to generate cArea list: {}".format(cAreas.placementTime))
Visualiser(cAreas.return_cAreas())
       
        



