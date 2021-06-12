import time

from vis import Visualiser




#tplon, tplat, btlon, btlat



xMin, yMin = 0, 0

xMax, yMax = 10, 10
nCircles = 2
rCircles = 4


from vis import Visualiser
from data_generator import DataGenerator, DataGeneratorV2
#vis = Visualiser(data.brute_force_point_allocation(), xMin, xMax, yMin, yMax, rCircles, plotEvery = False)  


from data_vis import Visualiser
from gridbased_data_generator import GridBasedCAreaMaker
data = GridBasedCAreaMaker(nCircles, rCircles, xMin, xMax, yMin, yMax)
Visualiser(data)
       
        







#time testing, averaging over a number of tests.
"""
nTests = 100
startTime = time.time()
for i in range(nTests):
    
    dummy_data = DataGenerator(nCircles, xMin, xMax, yMin, yMax)
    vis = Visualiser(dummy_data, xMin, xMax, yMin, yMax, rCircles, plotEvery = True)
    
    
endTime = time.time()

totalTime = (endTime - startTime)/nTests




print("average time for single run: {}".format(totalTime))
"""