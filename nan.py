'''
Author: gwyxjtu 867718012@qq.com
Date: 2022-06-04 20:01:50
@ LastEditors: Yu Zhao
@ LastEditTime: 2022-06-11 18:54:31
FilePath: /NR_code/nan.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import gurobipy as gp
from gurobipy import GRB
import pprint
from config import load

m = gp.Model("lagrange")

def nan_opt(load,   # 机组负载
        price_jz1 = [300,380,430],   # 机组1分段价格
        ub_jz1 = [500,200,100], # 机组1分段出力
        lb_jz1 = [200,0,0], # 机组1分段出力下限
        
        price_jz2 = [290,400,450],  # 机组2
        ub_jz2 = [600,200,100],
        lb_jz2 = [300,0,0],
        
        price_jz3 = [60,250,390],   # 机组3
        ub_jz3 = [300,200,300],
        lb_jz3 = [0,0,0],
        ):
    
    # ub_jz1 = [600,700,800]
    # lb_jz1 = [200,601,701]# 每个变量代表一个时段的负荷出力，这里假设第二功率阶段出力价格不影响第一功率阶段出力价格
    
    #amount_jz1 = [0,0,0]
    P_G_jz1 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz1_%d" % i) for i in range(3)]  #3是指三个阶段报价，代表每一个报价阶段的出力量。
    P_G_jz2 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz2_%d" % i) for i in range(3)]
    P_G_jz3 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz3_%d" % i) for i in range(3)]
    P_D = load

    l = m.addConstr(gp.quicksum(P_G_jz3)+gp.quicksum(P_G_jz2)+gp.quicksum(P_G_jz1)>= P_D)
    l1 = []
    l2 = []
    l3 = []
    for i in range(len(P_G_jz1)):
        l1.append(m.addConstr(P_G_jz1[i] >= lb_jz1[i]+0.1))
        l1.append(m.addConstr(P_G_jz1[i] <= ub_jz1[i]))
        l2.append(m.addConstr(P_G_jz2[i] >= lb_jz2[i]+0.1))
        l2.append(m.addConstr(P_G_jz2[i] <= ub_jz2[i]))
        l3.append(m.addConstr(P_G_jz3[i] >= lb_jz3[i]+0.1))
        l3.append(m.addConstr(P_G_jz3[i] <= ub_jz3[i]))
    m.setObjective(gp.quicksum([price_jz1[i]*P_G_jz1[i] +price_jz2[i]*P_G_jz2[i]+price_jz3[i]*P_G_jz3[i]for i in range(len(P_G_jz3))]),GRB.MINIMIZE)
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
    ans['l1_dual'] = [l1[i].pi for i in range(len(l1))]
    ans['l2_dual'] = [l2[i].pi for i in range(len(l2))]
    ans['l3_dual'] = [l3[i].pi for i in range(len(l3))]
    return ans

if __name__=="__main__":

    final = []
    for i in range(len(load)):
        final.append(nan_opt(load[i]))

    pprint.pprint(final)