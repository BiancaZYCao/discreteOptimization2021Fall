#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import gurobipy as gp
from gurobipy import GRB

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

    # Model
    model = gp.Model("facility")

    # fac_range=range(facility_count)
    # cust_range=range(customer_count)

    # decision variables
    used=model.addVars(facility_count,vtype=GRB.BINARY,name="used")
    assignment=model.addVars(customer_count,facility_count,
        vtype=GRB.BINARY,name="assignment")
    # assignment[cust,fac] == 1 means assigned
    print("used: ", used)
    print("assignment: ", assignment)
    model.update()

    # constraints
    # 1 - total demand assigned <= facility capacity (open) / 0 (closed)
    for f in facilities:
        model.addConstr(gp.quicksum(assignment[c.index,f.index] * c.demand for c in customers) <= f.capacity)
    # 2 - one customer <=> one facilities
    model.addConstrs((assignment.sum(c.index)==1 for c in customers))
    # additional constraints to improve performance?
    for f in facilities:
        for c in customers:
            model.addConstr(assignment[c.index,f.index] <= used[f.index])

    # objective
    model.setObjective(
        gp.quicksum(
            f.setup_cost * used[f.index] + 
            gp.quicksum(assignment[c.index,f.index]*dist[c.index][f.index] 
                for c in customers) 
            for f in facilities), 
        GRB.MINIMIZE)
    # Solve
    model.optimize()

    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1]*len(customers)

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index].x for f in facilities])
    for c in customers:
        for f in facilities:
            if assignment[c.index,f.index].x ==1.0:
                solution[c.index]=f.index
                obj+=dist[c.index][f.index]

    # for customer in customers:
    #     obj += length(customer.location, facilities[solution[customer.index]].location)

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

