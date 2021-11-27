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
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    #build distance Matrix
    dist=[[0 for _ in range(facility_count)] for _ in range(customer_count)]
    for customer in customers:
        for facility in facilities:
            dist[customer.index][facility.index]=length(customer.location,facility.location)
    print(dist[-2][:10])

    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]
    hot_spots={}
    try_swap=False #fl_25_2;fl_100_7;fl_100_1
    try_sec_nearest_fac=False
    sec_options={}

    for customer in customers:
        dist_list=dist[customer.index].copy()
        dist_list_sorted=sorted(dist_list)
        while len(dist_list_sorted)>0:
            # pick nearest facility first based on distance matrix
            min_dist=dist_list_sorted.pop(0)
            nearest_facility_index=dist_list.index(min_dist)
            # check capacity
            if capacity_remaining[nearest_facility_index] >= customer.demand:
                solution[customer.index] = nearest_facility_index
                capacity_remaining[nearest_facility_index] -= customer.demand
                min_dist_2=dist_list_sorted.pop(0)
                if min_dist_2<min_dist+facilities[nearest_facility_index].setup_cost:
                    try_sec_nearest_fac=True
                    sec_opt_fac_index=dist_list.index(min_dist_2)
                    sec_options[customer.index]=sec_opt_fac_index
                    # min_dist_2=dist_list_sorted.pop(0)
                break
            else:
                try_swap=True #fl_50_6;fl_200_7;fl_500_7;fl_1000_2;fl_1000_2
                if nearest_facility_index in hot_spots:
                    hot_spots[nearest_facility_index].append(customer.index)
                else:
                    hot_spots[nearest_facility_index]=[customer.index]
                # print("cap not enough! ",customer.index,capacity_remaining[nearest_facility_index],customer.demand)
    if try_sec_nearest_fac:
        print("possible to reduce obj. - large setup cost")
    if try_swap:
        print("possible to reduce obj. - swap 2 assignments")

    # print(capacity_remaining)
    used=[0]*len(facilities)
    for facility_index in solution:
        used[facility_index]+=1
    if try_sec_nearest_fac:
        for customer_index,sec_opt_fac_index in sec_options.items():
            if used[solution[customer_index]]==1 and \
            used[sec_opt_fac_index]>0 and \
            capacity_remaining[sec_opt_fac_index]>=customers[customer_index].demand:
                capacity_remaining[sec_opt_fac_index]-=customers[customer_index].demand
                capacity_remaining[solution[customer_index]]+=customers[customer_index].demand
                used[solution[customer_index]]-=1
                used[sec_opt_fac_index]+=1
                solution[customer_index]=sec_opt_fac_index
                print("optimize")

    # calculate the cost of the solution
    obj = sum([f.setup_cost for f in facilities if used[f.index]>0])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

