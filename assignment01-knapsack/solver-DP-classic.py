#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm - DP
    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        if int(parts[0])==0:
            items.append(Item(i-1, int(parts[0]), capacity+1))
        else:
            items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a matrix to store state data. row_id=capacity, col_id=no_of_items_taken, value=max_value_can_get
    mat_value=np.zeros((capacity+1,item_count+1),dtype=np.int)
    
    for j,item in enumerate(items):
        for k in range(1,capacity+1):
            if item.weight<=k:
                mat_value[k][j+1]=max(mat_value[k][j],item.value+mat_value[k-item.weight][j])
            else:
                mat_value[k][j+1]=mat_value[k][j]
    result_value=mat_value[capacity][item_count]
    # find out taken items by checking the matrix
    rest_cap=capacity
    taken=[0]*item_count
    for j in range(item_count,0,-1):
        if mat_value[rest_cap][j]!=mat_value[rest_cap][j-1]:
            taken[j-1]=1
            item=items[j-1]
            rest_cap -= item.weight

    # prepare the solution in the specified output format
    output_data = str(result_value)+ ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

