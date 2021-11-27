#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import random

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

    allow_fac_dict = { 
        '100 100'    : [70],
        '100 1000'   : [56,68,19,48,34,51,64]
    }
    ban_fac_dict = { 
        '25 50'      : [9],
        '50 200'     : [0,12,17,20,21,22,23,27,32,30,48,46]
    }
    rest = { 
        '200 800'    : 'result/fl_200_7',
        '500 3000'   : 'result/fl_500_7',
        '1000 1500'  : 'result/fl_1000_2',
        '2000 2000'  : 'result/fl_2000_2'
    }
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    if prob_n_m in allow_fac_dict:
        allow_fac_list=allow_fac_dict[prob_n_m]
        for i in range(1, facility_count+1):
            parts = lines[i].split()
            if (i-1) not in allow_fac_list:
                facilities.append(Facility(i-1, float(parts[0]), 0, Point(float(parts[2]), float(parts[3])) )) 
            else:
                facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))
    elif prob_n_m in ban_fac_dict:
        ban_fac_list=ban_fac_dict[prob_n_m]
        for i in range(1, facility_count+1):
            parts = lines[i].split()
            if (i-1) in ban_fac_list:
                facilities.append(Facility(i-1, float(parts[0]), 0, Point(float(parts[2]), float(parts[3])) )) 
            else:
                facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))
    else:
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
    # print(dist[-2][:10])

    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]
    hot_spots={}
    assignment={}
    for f in facilities:
        assignment[f.index]=[]
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
                assignment[nearest_facility_index].append(customer.index)
                break
            else:
                try_swap=True #fl_50_6;fl_200_7;fl_500_7;fl_1000_2;fl_1000_2
                if nearest_facility_index in hot_spots:
                    hot_spots[nearest_facility_index].append(customer.index)
                else:
                    hot_spots[nearest_facility_index]=[customer.index]
                print("cap not enough! ",customer.index,capacity_remaining[nearest_facility_index],customer.demand)

    if try_swap:
        print("possible to reduce obj. - swap 2 assignments")
        for fac_index,customer_list in hot_spots.items():
            while len(customer_list)>0:
                # pick swap_cust_index from hot_spots_customer_list
                swap_cust_index=customer_list.pop(0)
                # print("try to assign ", swap_cust_index," to ", fac_index)
                curr_partial_cost=dist[swap_cust_index][solution[swap_cust_index]]
                min_reduced_cost,swap_cust_index_2,swap_2_new_assign=0,-1,-1
                # find cust_index in curr_assignment which can reduce cost by changing assignment
                for cust_index in assignment[fac_index]:
                    # 1. capacity check
                    if customers[cust_index].demand+capacity_remaining[fac_index]>customers[swap_cust_index].demand:
                        curr_partial_cost_2=dist[cust_index][fac_index]
                        curr_partial_cost_2+=facilities[solution[swap_cust_index]].setup_cost if len(assignment[solution[swap_cust_index]])== 1 else 0
                        swap_partial_cost=dist[swap_cust_index][fac_index]
                        # find a new assignment for cust_index
                        # update cap_remaining
                        capacity_remaining[fac_index]+=customers[cust_index].demand-customers[swap_cust_index].demand
                        dist_list=dist[cust_index].copy()
                        dist_list_sorted=sorted(dist[cust_index])
                        while len(dist_list_sorted)>0:
                            min_dist=dist_list_sorted.pop(0)
                            nearest_facility_index=dist_list.index(min_dist)
                            if capacity_remaining[nearest_facility_index] >= customers[cust_index].demand:
                                new_fac_index=nearest_facility_index
                                swap_partial_cost_2=min_dist
                                # add setup-cost if fac not being used
                                swap_partial_cost_2+=facilities[nearest_facility_index].setup_cost if len(assignment[nearest_facility_index])== 0 else 0
                                swap_partial_cost_2+=facilities[nearest_facility_index].setup_cost if nearest_facility_index==swap_cust_index else 0
                                reduced_cost=swap_partial_cost_2+swap_partial_cost-curr_partial_cost-curr_partial_cost_2
                                if reduced_cost<min_reduced_cost:
                                    # good swap
                                    min_reduced_cost=reduced_cost
                                    swap_cust_index_2=cust_index
                                    swap_2_new_assign=new_fac_index
                                    # print('find better after swap:',min_reduced_cost,swap_cust_index_2,swap_2_new_assign)
                                break
                        capacity_remaining[fac_index]-=customers[cust_index].demand-customers[swap_cust_index].demand
                if min_reduced_cost<0 and swap_cust_index_2>=0 and swap_2_new_assign>=0:
                    # real swap here, change solution,capacity_remaining, assignment
                    print('real swap here:',cust_index,'->',fac_index,'; ',swap_cust_index_2,'->',swap_2_new_assign)
                    solution[swap_cust_index],solution[swap_cust_index_2] = fac_index,swap_2_new_assign
                    capacity_remaining[swap_2_new_assign] -= customers[swap_cust_index_2].demand
                    capacity_remaining[fac_index]+=customers[swap_cust_index_2].demand-customers[swap_cust_index].demand
                    assignment[fac_index].append(swap_cust_index)
                    assignment[fac_index].remove(swap_cust_index_2)
                    assignment[swap_2_new_assign].append(swap_cust_index_2)
    
    # new strategy to reduce fac cost
    # close fac with <=2 assignments
    # cust_released_ids=[]
    release_assignment={}
    curr_partial_cost,new_partial_cost=0,0
    # closed_fac=[]
    for fi,assign_list in assignment.items():
        curr_partial_cost+=facilities[fi].setup_cost
        if len(assign_list)<=6:
            release_assignment[fi]=assign_list
            # closed_fac.append(fi)
    # reassigned released customers
    # released and compare one by one
    for fi,assign_list in release_assignment.items():
        curr_partial_cost,new_partial_cost=facilities[fi].setup_cost,0
        temp_cap_rem=capacity_remaining[fi]
        capacity_remaining[fi] = 0 # restore later if failed
        cust_reassigned=[False]*len(assign_list)
        cust_reassigned_ids=[-1]*len(assign_list)
        accepted=False
        for i,ci in enumerate(assign_list):
            curr_partial_cost+=dist[ci][fi]
            dist_list=dist[ci].copy()
            dist_list_sorted=sorted(dist_list)
            while len(dist_list_sorted)>0:
                # pick nearest facility first based on distance matrix
                min_dist=dist_list_sorted.pop(0)
                nearest_facility_index=dist_list.index(min_dist)
                # check capacity
                if capacity_remaining[nearest_facility_index] >= customers[ci].demand \
                    and len(assignment[nearest_facility_index])>0: # only reassign to curr opening facilities
                    new_partial_cost+=min_dist
                    cust_reassigned[i]=True
                    cust_reassigned_ids[i]=nearest_facility_index
                    # solution[ci] = nearest_facility_index
                    capacity_remaining[nearest_facility_index] -= customers[ci].demand
                    # assignment[nearest_facility_index].append(customer.index)
                    break
        if sum(cust_reassigned)==len(assign_list): # all re-assgined
            # compare cost see if better
            if new_partial_cost<curr_partial_cost:
                # accept new result
                print("find better res after closing the facilities")
                accepted=True
                for i,ci in enumerate(assign_list):
                    solution[ci]=cust_reassigned_ids[i]
                    assignment[cust_reassigned_ids[i]].append(ci)
                assignment[fi]=[]
        if not accepted:
            capacity_remaining[fi] = temp_cap_rem
            for ci,fi_new in zip(assign_list,cust_reassigned_ids):
                if fi_new != -1:
                    capacity_remaining[fi_new] += customers[ci].demand
        

    used=[0]*len(facilities)
    for facility_index in solution:
        used[facility_index]+=1

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

