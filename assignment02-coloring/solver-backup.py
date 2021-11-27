#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
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
    
   
    map_v={}
    map_degree={}
    for u,v in edges:
        if u in map_v.keys():
            map_v[u].append(v)
            map_degree[u]+=1
        else:
            map_v[u]=[v]
            map_degree[u]=1
        if v in map_v.keys():
            map_v[v].append(u)
            map_degree[v]+=1
        else:
            map_v[v]=[u]
            map_degree[v]=1
    sorted_map=dict(sorted(map_v.items(),key=lambda v:len(v[1]),reverse=True))
    sorted_degree=dict(sorted(map_degree.items(),key=lambda v:v[1],reverse=True))
    #print("sorted_map: ",sorted_map)
    solution = my_greedy_algo(sorted_map,node_count)

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def my_greedy_algo(map_v,node_count):
    solution = [0]*node_count
    ban_map={}
    for i in range(0,node_count):
        ban_map[i]=set()
    curr_color_id=0
    for v,neigh_list in map_v.items():
        for n in neigh_list:
            ban_map[n].add(solution[v])
            min_possible_color_id=0
            while True:
                if min_possible_color_id in ban_map[n]:
                    min_possible_color_id +=1
                else:
                    solution[n]=min_possible_color_id
                    break
        #print("current coloring:  ",solution)
    return solution

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

