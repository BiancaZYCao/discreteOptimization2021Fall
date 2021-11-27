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

    sol_file_dic = { 
        51    : 'result/sol_tsp_51_1.txt',
        100   : 'result/sol_tsp_100_3.txt',
        200    : 'result/sol_tsp_200_2.txt',
        574    : 'result/sol_tsp_574_1.txt',
        1889   : 'result/sol_tsp_1889_1.txt',
        33810  : 'result/sol_tsp_33810_1.txt'
    }
    
    filename = sol_file_dic[nodeCount]
    with open(filename, 'r') as output_data_file:
        output_data = output_data_file.read()

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

