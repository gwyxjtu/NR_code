'''
Author: gwyxjtu 867718012@qq.com
Date: 2022-06-05 13:07:05
LastEditors: gwyxjtu 867718012@qq.com
LastEditTime: 2022-06-05 17:50:09
FilePath: /NR_code/nan_without_price.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import gurobipy as gp
from gurobipy import GRB
from config import load
import pprint

m = gp.Model("lagrange")

def nwp_opt(load,
        price_jz1 = [350,400,450],   # 机组1
        ub_jz1 = [600,100,100],
        lb_jz1 = [200,0,0],
        price_jz2 = [340,420,460],   # 机组2
        ub_jz2 = [700,100,100],
        lb_jz2 = [300,0,0],
        ub_jz3 = 800,
        ):
    
    load=load-ub_jz3
    # ub_jz1 = [600,700,800]
    # lb_jz1 = [200,601,701]    # 每个变量代表一个时段的负荷出力，这里假设第二功率阶段出力价格不影响第一功率阶段出力价格
    
    #amount_jz1 = [0,0,0]
    # price_jz3 = [60,300,390]  # 机组3
    # ub_jz3 = [300,300,200]
    # lb_jz3 = [0,0,0]
    P_G_jz1 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz1_%d" % i) for i in range(3)]  #3是指三个阶段报价，代表每一个报价阶段的出力量。
    P_G_jz2 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz2_%d" % i) for i in range(3)]
    # P_G_jz3 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz3_%d" % i) for i in range(3)]
    P_D = load
    
    l = m.addConstr(gp.quicksum(P_G_jz2)+gp.quicksum(P_G_jz1)>= P_D)

    for i in range(len(P_G_jz1)):
        m.addConstr(P_G_jz1[i] >= lb_jz1[i]+0.1)
        m.addConstr(P_G_jz1[i] <= ub_jz1[i])
        m.addConstr(P_G_jz2[i] >= lb_jz2[i]+0.1)
        m.addConstr(P_G_jz2[i] <= ub_jz2[i])
        # m.addConstr(P_G_jz3[i] >= lb_jz3[i])
        # m.addConstr(P_G_jz3[i] <= ub_jz3[i])
    m.setObjective(gp.quicksum([price_jz1[i]*P_G_jz1[i] +price_jz2[i]*P_G_jz2[i] for i in range(len(P_G_jz1))]),GRB.MINIMIZE)
    m.optimize()
    print("----------------")
    ans = {}
    for v in m.getVars():
        print('%s %g' % (v.VarName, v.X))
        # add to ans
        ans[v.VarName] = v.X
    print('Obj: %g' % m.ObjVal)
    print('dual_price: %g' % l.Pi)
    ans['load'] = load
    ans['Obj'] = m.ObjVal
    ans['dual_price'] = l.Pi
    ans['power_jz1'] = sum([P_G_jz1[i].x for i in range(3)])
    ans['power_jz2'] = sum([P_G_jz2[i].x for i in range(3)])

    return l.Pi,ans['power_jz1'],ans['power_jz2']

if __name__=="__main__":

    # final = []
    # for i in range(len(load)):
    #     final.append(nwp_opt(load[i]))

    # pprint.pprint(final)
    nwp_opt(2100)