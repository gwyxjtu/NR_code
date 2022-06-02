import pandapower as pp
import pandapower.networks as pn


net = pn.case_ieee30()
#net = pp.networks.example_simple()
print(net.bus)
print(net.line)
print(net.trafo)



# from pandapower.plotting.plotly import simple_plotly

# simple_plotly(net)