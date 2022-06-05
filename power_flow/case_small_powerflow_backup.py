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


g0 = pp.create_gen(net, 0, p_mw=210.00, min_p_mw=170, max_p_mw=210,max_q_mvar=157.5,min_q_mvar=-157.5,vm_pu=1.0, controllable=True)
g1 = pp.create_gen(net, 2, p_mw=323.49, min_p_mw=0, max_p_mw=520.0,max_q_mvar=390.0,min_q_mvar=-390.0,vm_pu=1.0, controllable=True)
g2 = pp.create_gen(net, 4, p_mw=466.51, min_p_mw=0, max_p_mw=600.0,max_q_mvar=450.0,min_q_mvar=-450.0,vm_pu=1.0, controllable=True)
ext = pp.create_ext_grid(net,3,vm_pu=1.0, max_p_mw = 0, controllable=True)

pp.create_pwl_cost(net, 0,et = "gen",points = [[170,190,300],[190,200,350],[200,210,400]])
pp.create_pwl_cost(net, 1,et = "gen",points = [[0,300,300],[300,360,320],[360,520,340]])
pp.create_pwl_cost(net, 2,et = "gen",points = [[0,300,60],[300,500,400],[500,600,500]])



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



plt.subplot(3,2,1)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("出清价格")
plt.plot(record["pw"],record["clearing price"])
plt.subplot(3,2,2)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("风电收入")
plt.plot(record["pw"],record["profit_C"])
plt.subplot(3,2,3)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("火电场A收入")
plt.plot(record["pw"],record["profit_A"])
plt.subplot(3,2,4)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("火电厂B收入")
plt.plot(record["pw"],record["profit_B"])
plt.subplot(3,2,5)
plt.xlabel("风电报量")
plt.ylabel("社会总成本")
plt.plot(record["pw"],record["profit"])
plt.savefig(os.path.join(cache_dir,f"{l}load_nwp.png"),dpi=600)
plt.cla()
plt.clf()