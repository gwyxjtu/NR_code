'''
Author: gwyxjtu 867718012@qq.com
Date: 2022-06-05 16:51:09
@ LastEditors: Yu Zhao
@ LastEditTime: 2022-06-11 18:53:38
FilePath: /NR_code/plot_powerflow.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandapower as pp

import pandapower.networks as pn
from matplotlib import pyplot as plt
import os
import json
from maxmin import export_fig

#from nan_without_price import nwp_opt

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
list_A = [[170,170,330],[170,200,340],[200,210,380]]
list_B = [[0,250,290],[250,350,300],[350,520,360]]
list_C = [[0,350,0],[350,450,340],[450,600,370]]
#list_C = [[0,10000,0]]
def piece_wise_linear_price(piece_wise_linear_price_list, pw):
    #input piecewise linear price
    if len(piece_wise_linear_price_list) == 3:
        if pw < piece_wise_linear_price_list[0][1]:
            return piece_wise_linear_price_list[0][2]
        elif pw < piece_wise_linear_price_list[1][1]:
            return piece_wise_linear_price_list[1][2]
        elif pw < piece_wise_linear_price_list[2][1]:
            return piece_wise_linear_price_list[2][2]
    return 0


def run_powerflow_without_massflow(wind_power):
    #wind_power 276-492
    net = pn.case5()
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
    g2 = pp.create_gen(net, 4, p_mw=466.51, min_p_mw=0, max_p_mw=wind_power,max_q_mvar=450.0,min_q_mvar=-450.0,vm_pu=1.0, controllable=True)
    ext = pp.create_ext_grid(net,3,vm_pu=1.0, max_p_mw = 0, controllable=True)
    #pp.create_pwl_cost(net, 0,et = "ext_grid",points = [[0,500,900]])

    pp.create_pwl_cost(net, 0,et = "gen",points = list_A)
    pp.create_pwl_cost(net, 1,et = "gen",points = list_B)
    pp.create_pwl_cost(net, 2,et = "gen",points = list_C)


    pp.rundcopp(net)

    print(net.res_bus)
    print(net.res_ext_grid)
    print(net.res_line)
    print(net.res_load)
    print(net.res_cost)
    print(net.res_gen)

    net.res_line.to_csv('B_B_res_line.csv')
    net.res_bus.to_csv('B_B_res_bus.csv')
    net.res_gen.to_csv('B_B_res_gen.csv')
    return 0




run_powerflow_without_massflow(600)
