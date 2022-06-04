import pandapower as pp
import pandapower.networks as pn


net = pn.case5()
#net = pp.networks.example_simple()



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
pp.rundcpp(net, trafo_model='t', trafo_loading='current', recycle=None, check_connectivity=True, switch_rx_ratio=2, trafo3w_losses='hv')
# net.bus.to_csv("bus.csv")
# net.line.to_csv("line.csv")
# net.trafo.to_csv("trafo.csv")


print(net.res_bus)
print(net.res_ext_grid)
print(net.res_line)
print(net.res_load)
print(net.res_sgen)
print(net.res_gen)

net.res_line.to_csv("line.csv")

# from pandapower.plotting.plotly import simple_plotly
# simple_plotly(net)