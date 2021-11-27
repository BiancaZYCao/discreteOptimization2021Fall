#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyomo.environ import *

v = {'hammer':8, 'wrench':3, 'screwdriver':6, 'towel':11}
w = {'hammer':5, 'wrench':7, 'screwdriver':4, 'towel':3}

limit = 14

M = ConcreteModel()

M.ITEMS = Set(initialize=v.keys())

M.x = Var(M.ITEMS, within=Binary)

M.value = Objective(expr=sum(v[i]*M.x[i] for i in M.ITEMS), sense=maximize)

M.weight = Constraint(expr=sum(w[i]*M.x[i] for i in M.ITEMS) <= limit)

opt = SolverFactory('glpk')
opt.solve(M,tee=True)

print("Print values for each variable explicitly")
for i in M.x:
  print(str(M.x[i]), M.x[i].value)
  print(str(M.value))
  print(str(M.weight))
print("")
