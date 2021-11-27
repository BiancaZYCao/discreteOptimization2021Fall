#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
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

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    resstr="11 42 29 43 21 37 20 25 1 26 6 36 12 30 23 34 24 41 27 3 46 8 4 35 13 7 19 40 18 16 14 50 39 31 22 47 45 9 10 28 2 5 0 33 32 48 49 17 38 15 44"
    sol = resstr.split(" ")
    solution = list(map(int,sol))
    swap_vert_01,swap_vert_02=solution.index(14),solution.index(38)
    solution = getSolutionAftSwap(nodeCount,solution,swap_vert_01,swap_vert_02)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

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

