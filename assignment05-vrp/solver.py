#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    vehicle_capacities = [vehicle_capacity]*vehicle_count
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 
    dist_mat=[[0 for _ in range(customer_count)] for _ in range(customer_count)]
    for c1 in customers:
        for c2 in customers:
            dist_mat[c1.index][c2.index]=length(c1,c2)

    # index_manager
    manager = pywrapcp.RoutingIndexManager(len(dist_mat),
                                           vehicle_count, 0)
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dist_mat[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return customers[from_node].demand
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        vehicle_capacities,  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    
    # output result
    vehicle_tours = []
    total_distance=0
    if solution:
        for vehicle_id in range(vehicle_count):
            index = routing.Start(vehicle_id)
            vehicle_tour=[]
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                vehicle_tour.append(node_index)
                index = solution.Value(routing.NextVar(index))
            vehicle_tour.append(manager.IndexToNode(index))
            vehicle_tours.append(vehicle_tour)
        
        for v in range(0, vehicle_count):
            vehicle_tour = vehicle_tours[v]
            if len(vehicle_tour) > 2:
                for i in range(0, len(vehicle_tour)-1):
                    total_distance += dist_mat[vehicle_tour[i]][vehicle_tour[i+1]]

    outputData = '%.2f' % total_distance + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += ' '.join([str(node) for node in vehicle_tours[v]]) + '\n'

    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

