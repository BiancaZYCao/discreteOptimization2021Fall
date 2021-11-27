#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    if capacity>1000000 or item_count>5000:
           output_abandon = str(0)+ ' ' + str(0) + '\n'
           output_abandon += ' '.join(map(str, [0]*len(items)))
           return output_abandon
    
    # 2 dict to store all state data. key=rest_capacity, value=max
    rest_map_value={capacity:0}
    rest_map_taken={capacity:[]}
    
    for item in items:
        rest_map_value_temp={}
        rest_map_taken_temp={}
        for rest_capacity,value in rest_map_value.items():
            last_taken=rest_map_taken[rest_capacity]
            if rest_capacity >= item.weight:
                if rest_capacity-item.weight in rest_map_value.keys() and value+item.value<=rest_map_value[rest_capacity-item.weight]:
                    continue
                else:
                    rest_map_value_temp[rest_capacity-item.weight]=value+item.value
                    new_taken=last_taken.copy()
                    new_taken.append(item.index)
                    rest_map_taken_temp[rest_capacity-item.weight]=new_taken
                #print(rest_capacity-item.weight,rest_map_taken_temp[rest_capacity-item.weight])
        #print(rest_map_value,rest_map_taken)
        rest_map_value.update(rest_map_value_temp)
        rest_map_taken.update(rest_map_taken_temp)
 #               rest_map_taken[rest_capacity-item.weight][item.index]=1

    # prepare the solution in the specified output format
    result_rest_capacity = max(rest_map_value,key=rest_map_value.get)
    taken_items=rest_map_taken[result_rest_capacity]
    taken=[0]*len(items)
    for i in taken_items:
        taken[i]=1
    result=rest_map_value[result_rest_capacity]
    output_data = str(result)+ ' ' + str(0) + '\n'
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

