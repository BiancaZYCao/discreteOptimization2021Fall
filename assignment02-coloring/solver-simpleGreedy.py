#!/usr/bin/python
# -*- coding: utf-8 -*-


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

    # build a trivial solution
    # every node has its own color
    #solution = range(0, node_count)
    solution = [0]*node_count
    curr_color_id,prev=0,-1
    ban_map={}
    for i in range(0,node_count):
        ban_map[i]=set()
    for u,v in edges:
        if u>prev:
            if solution[u]>=curr_color_id:
                curr_color_id=solution[u]
            prev=u
        ban_map[v].add(solution[u])
        #find min not banned id
        min_possible_color=0
        while True:
            if min_possible_color in ban_map[v]:
                min_possible_color +=1
            else:
                solution[v]=min_possible_color
                break
    print(ban_map)
        
    '''
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
    sorted_map=dict(sorted(map_v.items(),key=lambda v:len(v[1])))
    print("sorted_map: ",sorted_map)
    print([(i%10) for i in range(0,20)])
    curr_color_id=0
    for v,neigh_list in sorted_map.items():
        curr_color_id=max(solution[v],curr_color_id)
        for n in neigh_list:
            if solution[n]==solution[v]:
                 solution[n]=curr_color_id+1
        print(solution)
        '''
    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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

