#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import networkx as nx
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
   
    G=nx.Graph(edges)
    strategies = ['largest_first','random_sequential','smallest_last','independent_set',
    'connected_sequential_bfs','connected_sequential_dfs','saturation_largest_first']
    solution,count = [0]* node_count,node_count
    for s in strategies:
        solution_map=nx.coloring.greedy_color(G, strategy=s)
        num_of_colors_used=max(solution_map.values())+1
        # print('strategy: ', s,' num_of_colors_used: ',num_of_colors_used)
        if num_of_colors_used < count:
            count = num_of_colors_used
            # solution = list(solution_map.values())
            solution = [solution_map[i] for i in range(node_count)]

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))+ '\n'

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


'''
    group the nodes by color_id
    Then randomly pick one group, order the subset by degree in descending order.
Pick another group, sort it and append the sorted list to the previous one.
Finally feed the nodes to your greedy algorithm.
Repeat the procedures on the new solutions for a couple thousand times.e.g. 3000.
        '''