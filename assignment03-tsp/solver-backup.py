#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple
from typing import Set

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
        sum_dist,solution,dist_list=strategyConnNeareastPoint(nodeCount,points)
        # print('old: ', sum_dist,solution)
        # key_max_dist=max(dist_list)
        # print('intersection: dist ', key_max_dist,dist_list[key_max_dist])
        # swap_vert_01,_=dist_list.pop(key_max_dist)[0]
        # key_max_dist=max(dist_list)
        # swap_vert_02,_=dist_list.pop(key_max_dist)[0]
        # print('intersection: dist ', key_max_dist)
        # new_sum_dist,new_solution=try2Opt(solution,nodeCount,points,sum_dist,swap_vert_01,swap_vert_02)
        # print('new: ',new_sum_dist,new_solution)
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
    isVisited = set()
    solution=[]
    sum_dist=0
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
        sum_dist+=min_dist
        curr_pt_id=min_dist_pt_id
    
    # add dist betwen final point to first point
    sum_dist+=length(points[solution[0]],points[solution[-1]])
    return sum_dist,solution,dist_list

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

def isBetterOptionToSwap(init_sol,points,swap_vert_01,swap_vert_02):
    edge1=length(points[init_sol[swap_vert_01]],points[init_sol[swap_vert_01+1]])
    edge2=length(points[init_sol[swap_vert_02]],points[init_sol[swap_vert_02+1]])
    new_edge1=length(points[init_sol[swap_vert_01]],points[init_sol[swap_vert_02]])
    new_edge2=length(points[init_sol[swap_vert_01+1]],points[init_sol[swap_vert_02+1]])
    if edge1+edge2>new_edge1+new_edge2:
        return True

def try2Opt(init_sol,nodeCount,points,sum_dist,swap_vert_01,swap_vert_02):
    # find 2 edges to exchange e1:=v1e1-v2e1 e2:=v1e2-v2e2
    # exchange and calc new sum_dist
    # if better than old one, update the list
    #       ..->..se1->ee1..->..se2->ee2..->.. 
    # =>    ..->..se1->se2..->..ee1->ee2...
    # swap_vert_01,swap_vert_02=generate2OptVert(nodeCount)
    print('try to swap: ', swap_vert_01,swap_vert_02)
    edge1=length(points[init_sol[swap_vert_01]],points[init_sol[swap_vert_01+1]])
    edge2=length(points[init_sol[swap_vert_02]],points[init_sol[swap_vert_02+1]])
    new_edge1=length(points[init_sol[swap_vert_01]],points[init_sol[swap_vert_02]])
    new_edge2=length(points[init_sol[swap_vert_01+1]],points[init_sol[swap_vert_02+1]])
    print('compare: ', edge1+edge2,new_edge1+new_edge2)
    if edge1+edge2>new_edge1+new_edge2:
        print('find better: ')
        #update solution
        new_sol=getSolutionAftSwap(nodeCount,init_sol,swap_vert_01,swap_vert_02)
        sum_dist += new_edge1+new_edge2-edge1-edge2
        return sum_dist,new_sol
    else:
        return sum_dist,init_sol
    
def getSolutionAftSwap(nodeCount,init_sol,swap_vert_01,swap_vert_02):
    new_sol=[]
    init_id=0
    while init_id<=swap_vert_01:
        new_sol.append(init_sol[init_id])
        init_id+=1
    init_id=swap_vert_02
    while init_id>swap_vert_01:
        new_sol.append(init_sol[init_id])
        init_id-=1
    init_id=swap_vert_02+1
    while init_id<nodeCount:
        new_sol.append(init_sol[init_id])
        init_id+=1
    return new_sol


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

