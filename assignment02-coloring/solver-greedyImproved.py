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
    for u,v in edges:
        if u in map_v.keys():
            map_v[u].append(v)
        else:
            map_v[u]=[v]
        if v in map_v.keys():
            map_v[v].append(u)
        else:
            map_v[v]=[u]     
    sorted_map=dict(sorted(map_v.items(),key=lambda v:len(v[1]),reverse=True))
    # print("sorted_map: ",sorted_map)
    solution,ban_map = my_greedy_algo(sorted_map,node_count)
    # print('first solution (from max degree vertices) : \n', str(max(solution)+1) ,'\n',solution)
    # shuffling nodes color => changing ban_map => update new color
    # goal is to use less color, so should randomly pick one color and swap with final one
    if max(solution)< 80 :
        iter_time= 2000
        for i in range(iter_time):
            # print('iteration ', i)
            ban_map,solution = node_shuffle(ban_map,solution,sorted_map)

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))+ '\n'

    return output_data

def node_shuffle(ban_map,solution,map_v):
    c1,c2=random.randint(0,max(solution)-1),max(solution)
    #update ban_map & solution -1 : simply swap c1 c2 
    for n,bs in ban_map.items():
        if c1 in bs and c2 in bs: 
            continue
        elif c1 in bs:
            bs.remove(c1)
            bs.add(c2)
        elif c2 in bs: 
            bs.remove(c2)
            bs.add(c1)
    solution = [ -1 if c==c2 else c for c in solution ]
    solution = [ -2 if c==c1 else c for c in solution ]
    solution = [ c1 if c==-1 else c for c in solution ]
    solution = [ c2 if c==-2 else c for c in solution ]
    # greedy again
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
    output_data_new = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data_new += ' '.join(map(str, solution))
    # print(output_data_new)
    return ban_map,solution


def my_greedy_algo(map_v,node_count):
    solution = [0]*node_count
    ban_map={}
    for i in range(0,node_count):
        ban_map[i]=set()
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
    return solution,ban_map

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
