import gurobipy as gp
from gurobipy import GRB


m = gp.Model("lagrange")

P_G = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_%d" % i) for i in range(3)]
P_D = 250

#z = m.addVar(vtype=GRB.,name="z")
price = [100,200,300]
ub = [100,200,300]
lb = [0,0,0]
l = m.addConstr(P_G[0] + P_G[1] + P_G[2] >= P_D)


for i in range(len(P_G)):
    m.addConstr(P_G[i] >= lb[i])
    m.addConstr(P_G[i] <= ub[i])

m.setObjective(gp.quicksum([price[i]*P_G[i] for i in range(len(P_G))]),GRB.MINIMIZE)
m.optimize()
print("----------------")
for v in m.getVars():
    print('%s %g' % (v.VarName, v.X))

print('Obj: %g' % m.ObjVal)
print('dual_price: %g' % l.Pi)
