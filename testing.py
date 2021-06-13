import math

def circleTesting(x1, y1, x2, y2, r):
  
    radialDist = (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)
    
    if radialDist < 4*r*r:
        #True meaning intersecting
        return True
    
    else:
        #False meaning non-intersecting
        return False