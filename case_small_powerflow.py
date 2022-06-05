import pandapower as pp
import pandapower.networks as pn


net = pn.case5()
#net = pp.networks.example_simple()

# delete generator
#pp.drop_elements_simple(net,0 ,"gen")


#net.poly_cost.to_csv("poly_cost.csv")
# print(net.ext_grid)
# exit(0)
net.gen.drop(0,inplace=True)
net.gen.drop(1,inplace=True)
net.gen.drop(2,inplace=True)
net.sgen.drop(0,inplace=True)
net.ext_grid.drop(0,inplace=True)
net.poly_cost.drop(0,inplace=True)
net.poly_cost.drop(1,inplace=True)
net.poly_cost.drop(2,inplace=True)
net.poly_cost.drop(3,inplace=True)
net.poly_cost.drop(4,inplace=True)

# price_jz1 = [350,400,450]#机组1
# # ub_jz1 = [600,700,800]
# # lb_jz1 = [200,601,701]# 每个变量代表一个时段的负荷出力，这里假设第二功率阶段出力价格不影响第一功率阶段出力价格
# ub_jz1 = [190,210,0]
# lb_jz1 = [170,190,0]
# #amount_jz1 = [0,0,0]
# price_jz2 = [340,420,460]#机组2
# ub_jz2 = [300,60,60]
# lb_jz2 = [0,0,0]
# price_jz3 = [60,300,390]#机组3
# ub_jz3 = [300,200,100]
# lb_jz3 = [0,0,0]

g0 = pp.create_gen(net, 0, p_mw=210.00, min_p_mw=170, max_p_mw=210,max_q_mvar=157.5,min_q_mvar=-157.5,vm_pu=1.0, controllable=True)
g1 = pp.create_gen(net, 2, p_mw=323.49, min_p_mw=0, max_p_mw=520.0,max_q_mvar=390.0,min_q_mvar=-390.0,vm_pu=1.0, controllable=True)
g2 = pp.create_gen(net, 4, p_mw=466.51, min_p_mw=0, max_p_mw=600.0,max_q_mvar=450.0,min_q_mvar=-450.0,vm_pu=1.0, controllable=True)
ext = pp.create_ext_grid(net,3,vm_pu=1.0, max_p_mw = 0, controllable=True)

pp.create_pwl_cost(net, 0,et = "gen",points = [[170,190,300],[190,200,350],[200,210,400]])
pp.create_pwl_cost(net, 1,et = "gen",points = [[0,300,300],[300,360,320],[360,520,340]])
pp.create_pwl_cost(net, 2,et = "gen",points = [[0,300,60],[300,500,400],[500,600,500]])


#    element        et  cp0_eur  cp1_eur_per_mw  cp2_eur_per_mw2  cq0_eur  cq1_eur_per_mvar  cq2_eur_per_mvar2
# 0        0       gen      0.0            14.0              0.0      0.0               0.0                0.0
# 1        0      sgen      0.0            15.0              0.0      0.0               0.0                0.0
# 2        1       gen      0.0            30.0              0.0      0.0               0.0                0.0
# 3        0  ext_grid      0.0            40.0              0.0      0.0               0.0                0.0
# 4        2       gen      0.0            10.0              0.0      0.0               0.0                0.0

# add generator

print(net)

print(net.bus)
print(net.line)
print(net.load)
print(net.gen)
print(net.sgen)
print(net.ext_grid)
print(net.poly_cost)
# exit(0)
# print(net)
pp.rundcopp(net)
# net.bus.to_csv("bus.csv")
# net.line.to_csv("line.csv")
# net.trafo.to_csv("trafo.csv")


print(net.res_bus)
print(net.res_ext_grid)
print(net.res_line)
print(net.res_load)
# print(net.res_sgen)
print(net.res_gen)


# from pandapower.plotting.plotly import simple_plotly
# simple_plotly(net)