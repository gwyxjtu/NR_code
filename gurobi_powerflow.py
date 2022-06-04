import gurobipy as gp
from gurobipy import GRB
import pprint

m = gp.Model("lagrange")


load = [300,300,400] #节点1，2，3的负荷

price_jz1 = [350,400,450]#机组1
# ub_jz1 = [600,700,800]
# lb_jz1 = [200,601,701]# 每个变量代表一个时段的负荷出力，这里假设第二功率阶段出力价格不影响第一功率阶段出力价格
ub_jz1 = [190,210,0]
lb_jz1 = [170,190,0]
#amount_jz1 = [0,0,0]
price_jz2 = [340,420,460]#机组2
ub_jz2 = [300,60,60]
lb_jz2 = [0,0,0]
price_jz3 = [60,300,390]#机组3
ub_jz3 = [300,200,100]
lb_jz3 = [0,0,0]


ub_line = [35.702054, 32.994314, 156.748063, 92.865455, 33.796607, 33.796607]
# line parameters
# c_nf_per_km   df  from_bus  g_us_per_km  in_service  length_km      max_i_ka  ...  name parallel  r_ohm_per_km  std_type to_bus  type x_ohm_per_km
# 0    35.702054  1.0         0          0.0        True        1.0      1.004087  ...  None        1       1.48649      None      1    ol      14.8649
# 1    32.994314  1.0         0          0.0        True        1.0  99999.000000  ...  None        1       1.60816      None      3    ol      16.0816
# 2   156.748063  1.0         0          0.0        True        1.0  99999.000000  ...  None        1       0.33856      None      4    ol       3.3856
# 3    92.865455  1.0         1          0.0        True        1.0  99999.000000  ...  None        1       0.57132      None      2    ol       5.7132
# 4    33.796607  1.0         2          0.0        True        1.0  99999.000000  ...  None        1       1.57113      None      3    ol      15.7113
# 5    33.796607  1.0         3          0.0        True        1.0      0.602452  ...  None        1       1.57113      None      4    ol      15.7113




P_G_jz1 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz1_%d" % i) for i in range(3)]  #at bus 0
P_G_jz2 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz2_%d" % i) for i in range(3)]  #at bus 2
P_G_jz3 = [m.addVar(vtype=GRB.CONTINUOUS,name="P_G_jz3_%d" % i) for i in range(3)]  #at bus 4
P_D = load
P_l = [m.addVar(vtype=GRB.CONTINUOUS,name="P_l_%d" % i) for i in range(6)] # 六条线路传输量

# load balance constraints
l = m.addConstr(gp.quicksum(P_G_jz3)+gp.quicksum(P_G_jz2)+gp.quicksum(P_G_jz1)>= P_D)

# power line constraints
# line 0 form bus 0 to bus 1
m.addConstr(P_l[0] == gp.quicksum(P_G_jz1) )



# 机组容量上下限约束
for i in range(len(P_G_jz1)):
    m.addConstr(P_G_jz1[i] >= lb_jz1[i])
    m.addConstr(P_G_jz1[i] <= ub_jz1[i])
    m.addConstr(P_G_jz2[i] >= lb_jz2[i])
    m.addConstr(P_G_jz2[i] <= ub_jz2[i])
    m.addConstr(P_G_jz3[i] >= lb_jz3[i])
    m.addConstr(P_G_jz3[i] <= ub_jz3[i])




m.setObjective(gp.quicksum([price_jz1[i]*P_G_jz1[i] +price_jz2[i]*P_G_jz2[i]+price_jz3[i]*P_G_jz3[i] for i in range(len(P_G_jz3))]),GRB.MINIMIZE)
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



final = []
for i in range(len(load)):
    final.append(opt(load[i]))

pprint.pprint(final)