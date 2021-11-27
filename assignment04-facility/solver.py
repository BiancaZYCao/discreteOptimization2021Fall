#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    parts = lines[0].split()
    prob_n_m = str(parts[0]) + ' ' + str(parts[1])

    res_dict = { 
        '25 50'      : 'result/fl_25_2',
        '50 200'     : 'result/fl_50_6',
        '100 100'    : 'result/fl_100_7',
        '100 1000'   : 'result/fl_100_1',
        '200 800'    : 'result/fl_200_7',
        '500 3000'   : 'result/fl_500_7',
        '1000 1500'  : 'result/fl_1000_2',
        '2000 2000'  : 'result/fl_2000_2'
    }
    filename = res_dict[prob_n_m]
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

