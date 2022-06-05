'''
Author: gwyxjtu 867718012@qq.com
Date: 2022-05-31 11:20:33
LastEditors: gwyxjtu 867718012@qq.com
LastEditTime: 2022-06-05 16:05:09
FilePath: /NR_code/test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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

l1 = [0 for i in range(3)]
l2 = [0 for i in range(3)]
for i in range(len(P_G)):
    l1[i] = m.addConstr(P_G[i] >= lb[i])
    l2[i] = m.addConstr(P_G[i] <= ub[i])
print(l1)
m.setObjective(gp.quicksum([price[i]*P_G[i] for i in range(len(P_G))]),GRB.MINIMIZE)
m.optimize()
print("----------------")
for v in m.getVars():
    print('%s %g' % (v.VarName, v.X))

print('Obj: %g' % m.ObjVal)
print('dual_price: %g' % l.Pi)
print([l1[i].Pi for i in range(len(P_G))])
print([l2[i].Pi for i in range(len(P_G))])

