#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple
from typing import Set

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def getDistMat(points,nodeCount,distMat):
    for i in range(nodeCount):
        for j in range(i+1,nodeCount):
            distMat[i][j] = length(points[i],points[j])
            distMat[j][i] = distMat[i][j]
    
    
def calcSumDist(distMat,nodeCount,solution):
    print(solution[0],solution[-1])
    sumDist=distMat[solution[0]][solution[-1]]
    for i in range(0,nodeCount-1):
        sumDist+=distMat[solution[i]][solution[i+1]]
    return sumDist
    
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
    distMat=[[float("inf") for _ in range(nodeCount)] for _ in range(nodeCount)]
    getDistMat(points,nodeCount,distMat)

    sumDist,solution,dist_list=strategyConnNeareastPoint(nodeCount,points)
    print("initial solution: ", solution)

    # params for annealing: initTemp,termTemp,lpTimes,alpha
    t,termTemp,lpTimes,alpha=30,0.00001,50,0.98
    while t>termTemp:
        for i in range(lpTimes):
            # find new sol
            swap_vert_01,swap_vert_02=generate2OptVert(nodeCount)
            trySol=genSolToTrySwap(solution,swap_vert_01,swap_vert_02)
            # if better , accept; else accept by bolzman param
            trySumDist=calcSumDist(distMat,nodeCount,trySol)
            delta=trySumDist-sumDist
            if delta < 0 :
                sumDist,solution=trySumDist,trySol
                print("success: ", delta, trySumDist ,trySol)
            else:
                p=math.exp(-delta/t)
                if p>random.uniform(0, 1):
                    sumDist,solution=trySumDist,trySol
                    print("accept: ", delta, trySumDist ,trySol)
                else: 
                    print("reject: ", trySol)
        t = t * alpha
 
    # prepare the solution in the specified output format
    output_data = '%.2f' % sumDist + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def strategyConnNeareastPoint(nodeCount,points):
    # start from the first point => curr_pt
    #  find nearest point n_pt with curr_pt
    #  n_pt =>  curr_pt ; n_pt visited
    isVisited = set()
    sumDist=0
    curr_pt_id = random.randint(0,nodeCount-1)
    solution=[curr_pt_id]
    isVisited.add(curr_pt_id)
    dist_list={}
    while len(solution)<nodeCount:
        min_dist,min_dist_pt_id = float("inf"),-1
        for p_id,pt in enumerate(points):
            if p_id not in isVisited:
                dist=length(pt, points[curr_pt_id])
                if dist<min_dist:
                    min_dist_pt_id,min_dist=p_id,dist
        solution.append(min_dist_pt_id)
        isVisited.add(min_dist_pt_id)
        if min_dist in dist_list:
            dist_list[min_dist].append([curr_pt_id,min_dist_pt_id])
        else:
            dist_list[min_dist]=[[curr_pt_id,min_dist_pt_id]]
        sumDist+=min_dist
        curr_pt_id=min_dist_pt_id
    
    # add dist betwen final point to first point
    sumDist+=length(points[solution[0]],points[solution[-1]])
    return sumDist,solution,dist_list

def generate2OptVert(nodeCount):
    # generate 2 vert
    swap_vert_01 = random.randint(0,nodeCount-2)
    swap_vert_02 = random.randint(0,nodeCount-2)
    while abs(swap_vert_01-swap_vert_02)<=2:
        swap_vert_02= random.randint(0,nodeCount-1)
    if swap_vert_01 > swap_vert_02:
        temp = swap_vert_01
        swap_vert_01=swap_vert_02
        swap_vert_02=temp
    return swap_vert_01,swap_vert_02

def genSolToTrySwap(solution,swap_vert_01,swap_vert_02):
    newSol=solution.copy()
    # temp = solution[swap_vert_01]
    newSol[swap_vert_01]=solution[swap_vert_02]
    newSol[swap_vert_02]=solution[swap_vert_01]
    return newSol


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

