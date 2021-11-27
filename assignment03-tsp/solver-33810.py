#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    # parse the input
    lines = input_data.split('\n')
    nodeCount = int(lines[0])
    
    points = []
    solution=[]
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    ptsX={}
    for ind,pt in enumerate(points):
        if pt[0] in ptsX:
            ptsX[pt[0]].append(ind)
        else:
            ptsX[pt[0]]=[ind]
    # print("group in X cord: ",ptsX)
    revVar=False
    while ptsX:
        minX=min(ptsX)
        ptsIds=ptsX.pop(minX)
        pY={}
        for ind in ptsIds:
            pY[ind]=points[ind][1]
        # print("group in Y cord: ",pY)
        pYs=dict(sorted(pY.items(), key=lambda x: x[1],reverse=revVar))
        # print(pYs)
        solution+=list(pYs.keys())
        revVar= not revVar
    # print("solution: ",solution)

    #calc
    sum_dist=length(points[solution[-1]], points[solution[0]])
    for i in range(0,nodeCount-1):
        sum_dist+=length(points[solution[i]], points[solution[i+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % sum_dist + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

