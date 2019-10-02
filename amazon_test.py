# coding:utf-8
# @Time : 2019-10-02 17:45 
# @Author : Andy.Zhang
# @Desc :


def ClosestXdestinations(numDestinations, allLocations, numDeliveries):
    import math
    # WRITE YOUR CODE HERE
    allDistance = {}
    for i in range(numDestinations):
        currentDistance = math.sqrt(math.pow(allLocations[i][0],2) + math.pow(allLocations[i][1],2))
        allDistance[currentDistance] = i

    output = sorted(allDistance.keys())
    for i in range(numDeliveries):
        print(i)
        print(allLocations[allDistance[output[i]]])


ClosestXdestinations(3, [[1,-3], [1,2], [3,4]], 1)