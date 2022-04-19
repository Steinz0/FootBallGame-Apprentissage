from cmath import inf
from math import dist
from tkinter import Y

import numpy as np


# To extract the data in the order file and create a matrix each line represents an order
def extractDataBrut():
    with open('order.txt', 'r') as f:
        lines = f.readlines()

        matrixBrut = []

        for l in lines:
            elements = l.split(';')
            
            ballCoord = (float(elements[0].split(',')[0]),float(elements[0].split(',')[1]))
            
            redCoords = []
            tmp_elem = elements[1].split(',')
            values = []
            for ind in range(0,len(tmp_elem),2):
                values.append((float(tmp_elem[ind])))
                redCoords.append((float(tmp_elem[ind]), float(tmp_elem[ind+1])))

            blueCoords = []
            tmp_elem = elements[2].split(',')
            values = []
            for ind in range(0,len(tmp_elem),2):
                values.append((float(tmp_elem[ind])))
                blueCoords.append((float(tmp_elem[ind]), float(tmp_elem[ind+1])))
    
            score = (int(elements[3].split(',')[0]),int(elements[3].split(',')[1]))

            actualPlayer = (float(elements[4].split(',')[0]),float(elements[4].split(',')[1]))

            team = elements[-2]
            order = elements[-1][:-1]

            matrixBrut.append([ballCoord, redCoords, blueCoords, score, actualPlayer, team, order])
        
        return matrixBrut


# we take the matrix and generate features for ours ml models
def get_features_Y(matrixBrut):
    features = []
    y = []
    for x in matrixBrut:
    
        y.append(x[-1])

        redCages = (0,350)
        blueCages = (1200,350)
        actualPlayer = x[4]
        team = x[5]

        distBall = dist(actualPlayer, x[0])
        distCagesAlly = 0
        distCagesEnnem = 0
        closestAlly = +inf
        closestEnnem = +inf
        nbAllyMyZone = 0
        nbAllynotMyZone = 0
        nbEnnemMyZone = 0
        nbEnnemnotMyZone = 0

        if team == "Red":
            distCagesAlly = dist(actualPlayer, redCages)
            distCagesEnnem = dist(actualPlayer, blueCages)

            for a in x[1]:
                d = dist(actualPlayer, a)
                if d < closestAlly:
                    closestAlly == d
                if a[0] < 600:
                    nbAllyMyZone += 1
                else:
                    nbAllynotMyZone += 1

            for a in x[2]:
                d = dist(actualPlayer, a)
                if d < closestEnnem:
                    closestEnnem == d

                if a[0] < 600:
                    nbEnnemMyZone += 1
                else:
                    nbEnnemnotMyZone += 1
            
            if actualPlayer[0] < 600:
                nbAllyMyZone -= 1
            else:
                nbAllynotMyZone -= 1

        else:
            distCagesEnnem = dist(actualPlayer, redCages)
            distCagesAlly = dist(actualPlayer, blueCages)           

            for a in x[2]:
                d = dist(actualPlayer, a)
                if d < closestAlly:
                    closestAlly == d
                if a[0] > 600:
                    nbAllyMyZone += 1
                else:
                    nbAllynotMyZone += 1

            for a in x[1]:
                d = dist(actualPlayer, a)
                if d < closestEnnem:
                    closestEnnem == d

                if a[0] > 600:
                    nbEnnemMyZone += 1
                else:
                    nbEnnemnotMyZone += 1

            if actualPlayer[0] > 600:
                nbAllyMyZone -= 1
            else:
                nbAllynotMyZone -= 1

        features.append(np.array([actualPlayer[0], actualPlayer[0], distBall, distCagesAlly, distCagesEnnem, nbAllyMyZone, nbEnnemMyZone, nbAllynotMyZone, nbEnnemnotMyZone]))

    return np.array(features), np.array(y)

mat = extractDataBrut()
features,y = get_features_Y(mat)
for f in features:
    print(f)

print(y)