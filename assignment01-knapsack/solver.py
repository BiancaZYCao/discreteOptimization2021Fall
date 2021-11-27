#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from collections import deque
import time
Item = namedtuple("Item", ['index', 'value', 'weight'])
# define class Node
class Node(object):
    def __init__(self,value,room,taken,depth):
        self.value=value
        self.room=room
        self.taken=taken
        self.depth=depth

def solve_it(input_data):
    # Modify this code to run your optimization algorithm - BB
    # parse the input
    start_time = time.time()
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

    if item_count>5000:
           output_abandon = str(0)+ ' ' + str(0) + '\n'
           output_abandon += ' '.join(map(str, [0]*len(items)))
           return output_abandon
    #sort items based on value density:=value/weight
    #print(items)

    
    root=Node(0,capacity,0,0)
    # also start from highest value density node
    # depth first approach
    stack=deque()
    max_value=0
    taken_items=list()
    curr_taken_list=[0]*len(items)
    stack.append(root)

    while len(stack)>0:
        curr_node=stack.pop()
        if curr_node.depth<item_count:
            child_node_right=Node(
                    curr_node.value,    curr_node.room,
                    0,    curr_node.depth+1)
            stack.append(child_node_right)

            if curr_node.room>=items[curr_node.depth].weight:
                child_node_left=Node(
                    curr_node.value+items[curr_node.depth].value,
                    curr_node.room-items[curr_node.depth].weight,
                        1,    curr_node.depth+1)
                stack.append(child_node_left)
            if curr_node.depth>0:
                curr_taken_list[items[curr_node.depth-1].index]=curr_node.taken
        elif curr_node.depth==item_count:
            if curr_node.value>max_value:
                max_value=curr_node.value
                curr_taken_list[items[curr_node.depth-1].index]=curr_node.taken
                taken = curr_taken_list.copy()
                #print('find one ',max_value,curr_taken_list,taken)

    # prepare the solution in the specified output format
    result=max_value
    output_data = str(result)+ ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))

    print("time cost: %s seconds" % (time.time()-start_time))
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

