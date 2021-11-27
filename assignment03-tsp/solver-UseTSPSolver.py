#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import pandas as pd
from concorde.tsp import TSPSolver

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    a = []
    b = []
    for line in lines[1:-1]:  # skipping last line which is blank in data files
        node1, node2 = line.split()
        a.append(float(node1))
        b.append(float(node2))
    data = pd.DataFrame({"A": a, "B": b})
    # data.index += 1

    # Instantiate solver
    solver = TSPSolver.from_data(
        data.A,
        data.B,
        norm="EUC_2D"
    )

    tour_data = solver.solve()
    assert tour_data.success
    
    solution = data.iloc[tour_data.tour]
    out = ' '.join(str(solution.index[i]) for i in range(len(solution)))
    output_data = f"{tour_data.optimal_value} {0}\n"
    output_data += f"{out}"
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

