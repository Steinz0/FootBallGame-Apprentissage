from cmath import inf
from math import dist

import numpy as np


# To extract the data in the order file and create a matrix each line represents an order
def extractDataBrut(filename):
    with open(filename, 'r') as f:
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
        # Each line : Tuple Vector Ball, List 
        return matrixBrut

def transform_state(state, id_team, id_player):
    # print(state)
    ballCoord = (state.ball.position._x, state.ball.position._y)
    redCoords = []
    blueCoords = []
    score = tuple(state.score.values())
    actualPlayer = (state.init_states[(id_team, id_player)]._x, state.init_states[(id_team, id_player)]._y)
    if id_team == 1:
        team = 'Red'
    else:
        team = 'Blue'
    for p in state.init_states:
        pos = (state.init_states[p]._x, state.init_states[p]._y)
        if p[0] == 1:
            redCoords.append(pos)
        else:
            blueCoords.append(pos)

    return [[ballCoord, redCoords, blueCoords, score, actualPlayer, team]]

# we take the matrix and generate features for ours ml models
def get_features_y(matrix=None, filename=None, getY=True, normalize=False):
    
    matrixBrut = []
    
    if filename:
        matrixBrut = extractDataBrut(filename)
    elif matrix:
        matrixBrut = matrix
    
    features = []
    y = []
    for x in matrixBrut:
        if getY:
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

        closestAllyFront = +inf
        closestEnnemFront = +inf
        closestAllyBehind = +inf
        closestEnnemBehind = +inf

        if team == "Red":
            distCagesAlly = dist(actualPlayer, redCages)
            distCagesEnnem = dist(actualPlayer, blueCages)

            for a in x[1]:
                d = dist(actualPlayer, a)

                if d != 0:
                    if d < closestAlly:
                        closestAlly = d

                    if a[0] <= actualPlayer[0]:
                        if d < closestAllyBehind:
                            closestAllyBehind = d
                    else:
                        if d < closestAllyFront:
                            closestAllyFront = d
                        
                    if a[0] < 600:
                        nbAllyMyZone += 1
                    else:
                        nbAllynotMyZone += 1

            for a in x[2]:
                d = dist(actualPlayer, a)

                if d < closestEnnem:
                    closestEnnem = d
                
                if a[0] <= actualPlayer[0]:
                    if d < closestEnnemBehind:
                        closestEnnemBehind = d
                else:
                    if d < closestEnnemFront:
                        closestEnnemFront = d

                if a[0] < 600:
                    nbEnnemMyZone += 1
                else:
                    nbEnnemnotMyZone += 1
            
            # if actualPlayer[0] < 600:
            #     nbAllyMyZone -= 1
            # else:
            #     nbAllynotMyZone -= 1

        else:
            distCagesEnnem = dist(actualPlayer, redCages)
            distCagesAlly = dist(actualPlayer, blueCages)           

            for a in x[2]:
                d = dist(actualPlayer, a)
                if d < closestAlly:
                    closestAlly = d
                if a[0] > 600:
                    nbAllyMyZone += 1
                else:
                    nbAllynotMyZone += 1

            for a in x[1]:
                d = dist(actualPlayer, a)
                if d < closestEnnem:
                    closestEnnem = d

                if a[0] > 600:
                    nbEnnemMyZone += 1
                else:
                    nbEnnemnotMyZone += 1

            if actualPlayer[0] > 600:
                nbAllyMyZone -= 1
            else:
                nbAllynotMyZone -= 1

        if closestEnnemFront == +inf:
            closestEnnemFront = 10000
        if closestAllyFront == +inf:
            closestAllyFront = 10000
        if closestEnnemBehind == +inf:
            closestEnnemBehind = 10000
        if closestAllyBehind == +inf:
            closestAllyBehind = 10000

        # features.append(np.array([actualPlayer[0], actualPlayer[1], distBall, distCagesAlly, distCagesEnnem, closestAlly, closestEnnem, nbAllyMyZone, nbEnnemMyZone, nbAllynotMyZone, nbEnnemnotMyZone]))
        features.append(np.array([actualPlayer[0], actualPlayer[1], distBall, distCagesAlly, distCagesEnnem, closestAlly, closestEnnem, closestAllyFront, closestEnnemFront, closestAllyBehind, closestEnnemBehind, nbAllyMyZone, nbEnnemMyZone, nbAllynotMyZone, nbEnnemnotMyZone]))

    features = np.array(features)

    if normalize:
        max = np.max(features, axis=0)
        features = features/max

    return features, np.array(y)


# if __name__ == '__main__':
#     m = extractDataBrut('./order.txt')

#     print(m[0])

#     f, y = get_features_y(matrix=m)
#     max = np.max(f, axis=0)
#     print(f'max: {max}')
#     print(f'f[0]: {f[0]}')
#     nf = f/max
#     print(f'nf[0]: {nf[0]}')