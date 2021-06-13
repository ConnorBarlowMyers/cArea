import matplotlib.pyplot as plt
import matplotlib.patches as patches
from testing import circleTesting
plt.rcParams["figure.figsize"] = (10,10)

    
    
class Visualiser:
    
    def __init__(self, dataObject):
        self.dataObject = dataObject
        
        #geom details
        self.rCircle = dataObject.rCircles
        self.xMin = dataObject.xMin
        self.xMax = dataObject.xMax
        self.yMin = dataObject.yMin
        self.yMax = dataObject.yMax
        self.cAreaList = dataObject.cAreaList
               
        self.xWidth = self.xMax - self.xMin
        self.yWidth = self.yMax - self.yMin
        
        #set up plot objects
        self.plot = plt
        self.ax = plt.gca()
        plt.rcParams["figure.figsize"] = (10,10)
        self.ax.set_xlim((self.xMin, self.xMax))
        self.ax.set_ylim((self.yMin, self.yMax))
        
        #run methods
        self.draw_background()
        
        self.draw_circles()
        self.draw_grid()
        
        self.show()
          
        
    def draw_background(self):
        #remove the axes ticks and lables
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        
        #remove ugly border from the plot
        right = self.ax.spines["right"]
        left = self.ax.spines["left"]
        top = self.ax.spines["top"]
        bottom = self.ax.spines["bottom"]
        right.set_visible(False)
        left.set_visible(False)
        top.set_visible(False)
        bottom.set_visible(False)
        col = "#355C7D"
        #col = "#a8b8d0"
        
        #create the background rect and add it to the image
        rect = patches.Rectangle((self.xMin, self.yMin), self.xWidth, self.yWidth, 
                                 linewidth=100, edgecolor = col, facecolor = col)
        self.ax.add_patch(rect)
        
        
    def draw_grid(self):
        lineWidth = 0.1
        nXDivs = self.dataObject.nXDivs
        nYDivs = self.dataObject.nYDivs
        
        widthXDiv = self.dataObject.widthXDiv
        widthYDiv = self.dataObject.widthYDiv
        
        for i in range(nXDivs+1):
            self.plot.axline((i*widthXDiv, self.yMin), (i*widthXDiv, self.yMax), linewidth = lineWidth, color = "white")
        
        for i in range(nYDivs+1):
            self.plot.axline((self.xMin, i*widthYDiv), (self.xMax, i*widthYDiv), linewidth = lineWidth, color = "white")
        
    def draw_circles(self):
        
        circleNumber  = 0
        for cArea in self.cAreaList:

            x = cArea["lon"]
            y = cArea["lat"]
            r = self.rCircle
            
            
            trimmedCAreaList = self.cAreaList.copy()
            trimmedCAreaList.remove(cArea)
            
            #pink = "#FB9F8B"
            #gryblue = #9DC6CA
            #darkblue = 355C7D
            #purple = #6C5B7B
            
            nonIntersectCols = ('#9DC6CA', '#077B88')
            intersectCols = ('#6C5B7B','#FB9F8B')
            
            isIntersecting = False
            
            for testCArea in trimmedCAreaList:
                
                testX = testCArea["lon"]
                testY = testCArea["lat"]
                               
                if circleTesting(x, y, testX, testY, r) == True:
                    isIntersecting = True
                    
            if isIntersecting == True:
                cols = intersectCols             
            elif isIntersecting == False:
                cols = nonIntersectCols
            else:
                raise ValueError
                
            innerCircle = patches.Circle((x, y), r*0.07, linewidth=5, edgecolor = "white", facecolor = "black")   
            circle = patches.Circle((x, y), r, linewidth=5, edgecolor = cols[0], facecolor = cols[1])
            
            
            circleNumber += 1
            offset = 0.12
            self.ax.add_patch(circle)
            self.ax.add_patch(innerCircle)
            #self.ax.text(x - offset, y - offset, str(circleNumber), fontsize=20, color="white")
        
    def show(self):
        self.plot.show()




