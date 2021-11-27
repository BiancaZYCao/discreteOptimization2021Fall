#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from ortools.sat.python import cp_model

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
    # costs row:workers col:tasks

    dist=[[0 for _ in range(facility_count)] for _ in range(customer_count)]
    for customer in customers:
        for facility in facilities:
            dist[customer.index][facility.index]=int(length(customer.location,facility.location))

    # Model
    model = cp_model.CpModel()

    # decision variables
    assignment = []
    for ci in range(customer_count):
        temp = []
        for fj in range(facility_count):
            temp.append(model.NewBoolVar(f'x[{ci},{fj}]'))
        assignment.append(temp)

    # constraints
    # total demand assigned <= facility capacity (open) / 0 (closed)
    for fj in range(facility_count):
        model.Add(sum(assignment[ci][fj] * customers[ci].demand for ci in range(customer_count)) <= facilities[fj].capacity)
    # Each customer is assigned to exactly one warehouse.
    for ci in range(customer_count):
        model.Add(sum(assignment[ci][fj] for fj in range(facility_count)) == 1)

    # objective
    objective_terms = []
    for fj in range(facility_count):
        objective_terms.append(int(facilities[fj].setup_cost) * sum(assignment[ci][fj] for ci in range(customer_count)))
        for ci in range(customer_count):
            objective_terms.append(assignment[ci][fj]*dist[ci][fj])
    
    model.Minimize(sum(objective_terms))
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    solution = [-1]*len(customers)
    used=[0]*facility_count
    obj=0
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("is Optimal? ", status==cp_model.OPTIMAL)
        for ci in range(customer_count):
            for fj in range(facility_count):
                if solver.BooleanValue(assignment[ci][fj]):
                    solution[ci]=fj
                    used[fj]=1
                    obj+=dist[ci][fj]
        obj += sum([f.setup_cost*used[f.index] for f in facilities])
    else:
        print('No solution found.')

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

