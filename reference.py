# Without using external python libraries to what we have in python >= 3.7
# The function should take a GPS rectangle (fArea) and place a bunch of circle collection points randomly (cAreas)
# Each cArea will then have a number of items
# Each item should have a sat value of at least 5 sats
# If a small rectangle is submitted the function should limit the amount of collection points so they do not overlap
# The collection points must MOSTLY have a random distance between them, and they must not overlap, so some could be next to each other but most will be apart

import math
import random


def cAreaMaker(someSats, tplon, tplat, btlon, btlat, radiusOfEachCircle):

    # The alogorthym should caluculate close to these, but with the added variable of being based/restricted on the cArea size
    if 10 <= someSats <= 20:
        noAreas = 2
        itemsPArea = 1
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 20 <= someSats <= 50:
        noAreas = 4
        itemsPArea = 2
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 50 <= someSats <= 100:
        noAreas = 5
        itemsPArea = 2
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 100 <= someSats <= 500:
        noAreas = 10
        itemsPArea = 2
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 500 <= someSats <= 1000:
        noAreas = 20
        itemsPArea = 2
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 1000 <= someSats <= 5000:
        noAreas = 30
        itemsPArea = 3
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 5000 <= someSats <= 10000:
        noAreas = 40
        itemsPArea = 3
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if 10000 <= someSats <= 100000:
        noAreas = 50
        itemsPArea = random.randint(2, 4)
        itemValue = math.floor(someSats / (noAreas * itemsPArea))
    if someSats >= 100000:
        noAreas = 100
        itemsPArea = random.randint(2, 6)
        itemValue = math.floor(someSats / (noAreas * itemsPArea))

    # The algorythm loops through and creates the cAreas inside the fArea, each with there collection of items
    cAreas = []
    for areaNo in range(noAreas):
        items = []
        for item in range(itemsPArea):
            itemHash = random.getrandbits(128)
            items.append({"itemHash": itemHash, "itemValue": itemValue})
        cAreaHash = random.getrandbits(128)
        cAreas.append(
            {
                "lon": random.uniform(tplon, btlon),
                "lat": random.uniform(tplat, btlat),
                "areaHash": cAreaHash,
                "items": items,
            }
        )
    print(cAreas)


# This will print 30 cAreas with 3 items each, and a value of 11 for each item
# The issue is a lot of the cAreas overlap, especially as the fArea boundaries get smaller

cAreaMaker(
    1000,
    -0.2568223906894063,
    51.57109501333098,
    0.04943300877719548,
    51.44202475087509,
    10,
)