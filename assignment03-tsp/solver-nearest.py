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
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    
    solution=range(0,nodeCount)
    sum_dist=length(points[-1], points[0])
    if nodeCount<10000:
        sum_dist,solution,_=strategyConnNeareastPoint(nodeCount,points)
    else:
        for i in range(0,nodeCount-1):
            sum_dist+=length(points[i], points[i+1])
 
    # prepare the solution in the specified output format
    output_data = '%.2f' % sum_dist + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def strategyConnNeareastPoint(nodeCount,points):
    # start from the first point => curr_pt
    #  find nearest point n_pt with curr_pt
    #  n_pt =>  curr_pt ; n_pt visited
    isVisited = [False for i in range(nodeCount)]
    curr_pt_id = random.randint(0,nodeCount-1)
    isVisited[curr_pt_id] =True
    solution = [curr_pt_id]
    sum_dist=0
    dist_list={}
    while len(solution)<nodeCount:
        min_dist,min_dist_pt_id = float("inf"),-1
        for p_id,pt in enumerate(points):
            if not isVisited[p_id]:
                dist=length(pt, points[curr_pt_id])
                if dist<min_dist:
                    min_dist_pt_id,min_dist=p_id,dist
        solution.append(min_dist_pt_id)
        isVisited[min_dist_pt_id]=True
        dist_list(min_dist)=[curr_pt_id,min_dist_pt_id]
        sum_dist+=min_dist
        curr_pt_id=min_dist_pt_id

    # add dist betwen final point to first point
    sum_dist+=length(points[solution[0]],points[solution[-1]])

    return sum_dist,solution,dist_list


    

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

