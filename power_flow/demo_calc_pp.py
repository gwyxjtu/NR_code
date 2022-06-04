import pandapower as pp
import pandapower.networks

net = pandapower.networks.example_simple()
net

pp.rundcpp(net)