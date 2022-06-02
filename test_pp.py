import pandapower as pp
import pandapower.networks as pn


net = pn.case_ieee30()
#net = pp.networks.example_simple()
print(net.bus)
print(net.line)
print(net.trafo)

net.bus.to_csv("bus.csv")
net.line.to_csv("line.csv")
net.trafo.to_csv("trafo.csv")

# from pandapower.plotting.plotly import simple_plotly
# simple_plotly(net)