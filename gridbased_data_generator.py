import random
import math
from testing import circleTesting


class GridBasedCAreaMaker:
    """
    nCAreas: number of cAreas to place in the fArea
    itemsPArea: n items per cArea
    itemValue: value of each item 
    rCircles: radius of each of the cAreas placed
    xMin, xMax, yMin, yMax: fArea definition 
    maxPlacementAttempts: max successive failures for placing cAreas
    gridSweeperMaxPlacements: max successive failures for final gridsweep
    dictPreProcessing: 
        if we set dictPreProcessing to True, then the list of nearest neighbours for the
        whole grid is calculated before any circle placement attempts are made. This can
        get very demanding on memory, especially if the grid is large and the radius of the
        circles is small (large number of grid tiles). This reduces the time to place a 
        single circle.
    """
       
    def __init__(self, 
                 nCAreas,
                 itemsPArea,
                 itemValue,
                 rCircles, 
                 xMin, xMax, 
                 yMin, yMax, 
                 maxPlacementAttempts, 
                 gridSweeperMaxPlacements,
                 dictPreProcessing = False):
        
        
        self.dictPreProcessing = dictPreProcessing
        
        #placement vars
        self.maxPlacementAttempts = maxPlacementAttempts
        self.gridSweeperMaxPlacements = gridSweeperMaxPlacements
        self.nPlacedCAreas = 0
        
        #geometry vars
        self.nCAreas = nCAreas
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
        
        # item info
        self.itemsPArea = itemsPArea
        self.itemValue = itemValue
        
        # we round the number of grid divisions up, but still restrict placement
        # of cAreas to within the range defined by the fArea
        self.nXDivs = math.ceil(self.xRange / self.widthXDiv)
        self.nYDivs = math.ceil(self.yRange / self.widthYDiv)
        
        #create outputs
        self.gridDict = {}
        self.cAreaList = []
        self.gridIndexs = []
        #run methods
        self.create_blank_dict_structure()
        self.generate_data()
        self.grid_sweeper()
               
        
    def generate_cArea(self, xMin, xMax, yMin, yMax):
        x = random.uniform(xMin, xMax)
        y = random.uniform(yMin, yMax)
        cAreaHash = random.getrandbits(128)
        items = []
        for item in range(self.itemsPArea):
            itemHash = random.getrandbits(128)
            items.append({"itemHash": itemHash, "itemValue": self.itemValue})
        
        return {"lon": x, "lat":y, "cAreaHash": cAreaHash, "items":items}
    
    def create_blank_dict_structure(self):
        """
        Creates the nested dictionary structure used for the placement and collision
        testing of cAreas. If dictPreProcessing == True then all nn are calculated 
        for all grid positions before any cArea placement attempts are made.
        """
        for i in range(self.nXDivs):
            self.gridDict[i] = {}
    
            for j in range(self.nYDivs):              
                self.gridDict[i][j] = {"xy": [i, j], "cAreas": []}
                
                if self.dictPreProcessing == True:
                    neighbourPairs = self.calculate_nearest_neighbours(i, j)
                    self.gridDict[i][j]["neighbors"] = neighbourPairs
                              
    
    
    def calculate_nearest_neighbours(self, xIndex, yIndex):
        """
        Returns a list of the indices of all nn to gridcell (xIndex, yIndex)
        """

        i_list = [xIndex]
        j_list = [yIndex]
        nearestNeighbourPairs = []
               
        if (xIndex - 1) >= 0:
            i_list.append(xIndex - 1)
        
        if (xIndex + 1) <= self.nXDivs - 1:
            i_list.append(xIndex + 1)
            
        if (yIndex - 1) >= 0:
            j_list.append(yIndex - 1)
        
        if (yIndex + 1) <= self.nYDivs - 1:
            j_list.append(yIndex + 1)
        
        # we exclude the current grid index from its list of neighbours
        for x in i_list:
            for y in j_list:       
                if x == xIndex and y == yIndex:
                    pass
                else:
                    nearestNeighbourPairs.append([x, y])
        
        return nearestNeighbourPairs
    
    def find_grid_tile(self, x, y):
            # we round down to find the grid number we are in
            xGridNo = math.floor(x/self.widthXDiv)
            yGridNo = math.floor(y/self.widthYDiv)
            
            return self.gridDict[xGridNo][yGridNo]
    
    
    def add_point_to_dict(self, cAreaToAdd):
            newX = cAreaToAdd["lon"]
            newY = cAreaToAdd["lat"]
            
            self.cAreaList.append(cAreaToAdd)
            (updateX, updateY) = self.find_grid_tile(newX, newY)["xy"]
            self.gridDict[updateX][updateY]["cAreas"].append(cAreaToAdd)
            self.nPlacedCAreas += 1
    
    def place_single_cArea(self, xMin, xMax, yMin, yMax, maxPlacementAttempts):
        """
        Attempts to place cAreas on the grid until the number of successive failed
        attempts = maxPlacementAttempts, after which placement stops.
        """
        
        breakBool = False
        loopIter = -1
        
        while breakBool == False:
            loopIter += 1
            
            # NOTE: adjust this to include the sweeper, then stop the code.
            if loopIter == self.maxPlacementAttempts: 
                break
            
            # create the point to be collision tested against the other cAreas
            candidateCArea = self.generate_cArea(xMin, xMax, yMin, yMax)
            x = candidateCArea["lon"]
            y = candidateCArea["lat"]
            
            # list of all cAreas we need to test candidateCArea against
            testCAreas = []
                    
            candidateGridTile = self.find_grid_tile(x, y)
            
            # test candidate grid tile for cArea objects
            if len(candidateGridTile["cAreas"]) > 0:
                for singleCArea in candidateGridTile["cAreas"]:    
                    testCAreas.append(singleCArea)
            
            
            (xCandidateGridIndex, yCandidateGridIndex) = candidateGridTile["xy"]
            
            #calculate the list of nn for True/False dictPreProcessing
            if self.dictPreProcessing == True:
                nnList = candidateGridTile["neighbors"]
                
            if self.dictPreProcessing == False:
                    neighbourPairs = self.calculate_nearest_neighbours(xCandidateGridIndex, yCandidateGridIndex)
                    self.gridDict[xCandidateGridIndex][yCandidateGridIndex]["neighbors"] = neighbourPairs
                    nnList = neighbourPairs
            
            # test nn tiles for any cAreas
            for nearestNeighborGridTile in nnList:
                testGridX = nearestNeighborGridTile[0]
                testGridY = nearestNeighborGridTile[1]                   
                testGridCAreas = self.gridDict[testGridX][testGridY]["cAreas"]
                
                if len(testGridCAreas) > 0:   
                    for singleCArea in testGridCAreas:    
                        testCAreas.append(singleCArea)
                    
            # if there are no cAreas in the nn or candidate grid tile, then add the point directly 
            if len(testCAreas) == 0:
                self.add_point_to_dict(candidateCArea)
                break
            
            # if there are cAreas which we could collide with, then we test each for collisions                
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
        
    def generate_data(self):
        
        # add the first cArea - no checking required.
        self.add_point_to_dict(self.generate_cArea(self.xMin, self.xMax, self.yMin, self.yMax))
        # first cArea is placed without any testing required, hence nCAreas - 1
        for _ in range(self.nCAreas - 1):
            self.place_single_cArea(self.xMin, self.xMax, self.yMin, self.yMax, self.maxPlacementAttempts)
        
        
    def grid_sweeper(self):
        """
        Randomly selects a grid positions and tries to place a cArea gridSweeperMaxPlacements times.
        This repeats until every grid position has been tried, or the total number of cAreas required
        have been placed.
        """
        
        for i in range(self.nXDivs):
            for j in range(self.nYDivs):
                self.gridIndexs.append([i, j])
        
        #self.gridIndexs.append([i, j] for i in range(self.nXDivs) for j in range(self.nYDivs))
        
        
        while True:
            
            # if we've reached the number of cAreas we need, then break
            if self.nCAreas - self.nPlacedCAreas == 0:
                print("Grid-sweep finished.")  
                break
                
            # if we've tried every grid location, then break
            if len(self.gridIndexs) == 0:
                print("Grid-sweep finished.")  
                break 
            
            #generate random grid tile and attempt to place a cArea
            randomGridIndex = random.choice(self.gridIndexs)
            self.gridIndexs.remove(randomGridIndex)
            gridXMin = randomGridIndex[0] * self.widthXDiv
            gridYMin = randomGridIndex[1] * self.widthYDiv
            gridXMax = gridXMin + self.widthXDiv
            gridYMax = gridYMin + self.widthYDiv
            self.place_single_cArea(gridXMin, gridXMax, gridYMin, gridYMax, self.gridSweeperMaxPlacements)


            
        

    
        
        
        
        
        
   
        
