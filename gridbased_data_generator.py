import random
import math
from testing import circleTesting


class GridBasedCAreaMaker:
    
    def __init__(self, nCircles, rCircles, xMin, xMax, yMin, yMax, maxPlacementAttempts = 10000):
        self.nCircles = nCircles
        self.rCircles = rCircles
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.xRange = xMax - xMin
        self.yRange = yMax - yMin
        self.maxPlacementAttempts = maxPlacementAttempts
        self.widthXDiv = 2*self.rCircles
        self.widthYDiv = 2*self.rCircles
        
        # we round the number of grid divisions up, but still restrict placement
        # of cAreas to within the range defined by the fArea
        self.nXDivs = math.ceil(self.xRange / self.widthXDiv)
        self.nYDivs = math.ceil(self.yRange / self.widthYDiv)
        
        self.gridDict = {}
        self.outputData = []
        
        self.create_blank_dict_structure()
        self.generate_data()
        
        
    def generate_cArea(self):
        x = random.uniform(self.xMin, self.xMax)
        y = random.uniform(self.yMin, self.yMax)
        areaHash = 0
        items = 0
        
        return {"lon": x, "lat":y, "areaHash":areaHash, "items":items}
    
    def create_blank_dict_structure(self):
        
        # creat the base structure for the nested dictionaries used for the 
        # grid information
        for i in range(self.nXDivs):
            self.gridDict[i] = {}
            for j in range(self.nYDivs):
                # first we calculate the neighbours for use in the colision checks    
                i_list = [i]
                j_list = [j]
                neighbourPairs = []
                       
                if (i-1) >= 0:
                    i_list.append(i-1)
                
                if (i+1) <= self.nXDivs - 1:
                    i_list.append(i+1)
                    
                if (j-1) >= 0:
                    j_list.append(j-1)
                
                if (j+1) <= self.nYDivs - 1:
                    j_list.append(j+1)
                
                # we exclude the current grid index from its list of neighbours
                for x in i_list:
                    for y in j_list:       
                        if x == i and y == j:
                            pass
                        else:
                            neighbourPairs.append([x, y])
        
                self.gridDict[i][j] = {"xy": [i, j], "cAreas": [], "neighbors": neighbourPairs}
    
    def find_grid_tile(self, x, y, inputDict):
            
            # we round down to find the grid number we are in
            xGridNo = math.floor(x/self.widthXDiv)
            yGridNo = math.floor(y/self.widthYDiv)
            
            return inputDict[xGridNo][yGridNo]
    
    
    def add_point_to_dict(self, cAreaToAdd):
            newX = cAreaToAdd["lon"]
            newY = cAreaToAdd["lat"]
            
            self.outputData.append(cAreaToAdd)
            (updateX, updateY) = self.find_grid_tile(newX, newY, self.gridDict)["xy"]
            self.gridDict[updateX][updateY]["cAreas"].append(cAreaToAdd)
 
    
        
    def generate_data(self):
        # add the first cArea - no checking required. 
        self.add_point_to_dict(self.generate_cArea())
        
        # first cArea is placed without any testing required, hence nCircles - 1
        for circleNumb in range(self.nCircles - 1):
            
            breakBool = False
            loopIter = -1
            
            while breakBool == False:
                loopIter += 1
                
                # NOTE: adjust this to include the sweeper, then stop the code.
                if loopIter == self.maxPlacementAttempts:
                    raise NameError("Max placement attempts reached")

                
                # create the point to be collision tested against the other cAreas
                candidateCArea = self.generate_cArea()
                x = candidateCArea["lon"]
                y = candidateCArea["lat"]
                
                # list of all cAreas we need to test candidateCArea against
                testCAreas = []
                        
                candidateGridTile = self.find_grid_tile(x, y, self.gridDict)
                
                #dont append blank arrays
                if len(candidateGridTile["cAreas"]) > 0:
                    for singleCArea in candidateGridTile["cAreas"]:    
                        testCAreas.append(singleCArea)
                
                for nearestNeighborGridTile in candidateGridTile["neighbors"]:
                    
                    testGridX = nearestNeighborGridTile[0]
                    testGridY = nearestNeighborGridTile[1]                   
                    testGridCAreas = self.gridDict[testGridX][testGridY]["cAreas"]
                    
                    if len(testGridCAreas) > 0:   
                        for singleCArea in testGridCAreas:    
                            testCAreas.append(singleCArea)
                        
                # if there are no cAreas in the nn, then add the point directly 
                if len(testCAreas) == 0:
                    print("no test cAreas to collision check, circleNumb = {}".format(circleNumb))
                    self.add_point_to_dict(candidateCArea)                    
                    break
                
                print("testCAreas: {}".format(testCAreas))
                
                for testCArea in testCAreas:    
                    testX = testCArea["lon"]
                    testY = testCArea["lat"]
                    
                    # if circles do overlap, then break and retry with new test point
                    if circleTesting(x, y, testX, testY, self.rCircles) == True:
                        break
                                       
                    else:
                        # we are checking to see if the current testCArea is the
                        # last testCArea in the list
                        if testCArea == testCAreas[-1]:
                            self.add_point_to_dict(candidateCArea)
                            
                            # cArea is placed, breaking the while loop and starting the placement for the next point
                            breakBool = True
                            break
        
        
        