import pandapower as pp
import pandapower.networks as pn
from matplotlib import pyplot as plt
import os
import json
from maxmin import export_fig

#from nan_without_price import nwp_opt

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
list_A = [[170,190,330],[190,200,345],[200,210,400]]
list_B = [[0,250,290],[250,360,320],[360,520,360]]
#list_C = [[0,350,0],[350,500,340],[500,600,390]]
list_C = [[0,10000,0]]
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
    pw_A = net.res_gen.p_mw[0]
    pw_B = net.res_gen.p_mw[1]
    pw_C = net.res_gen.p_mw[2]
    #list_C = [[0,wind_power,0]]

    price_A = piece_wise_linear_price(list_A,pw_A)
    price_B = piece_wise_linear_price(list_B,pw_B)
    #price_C = piece_wise_linear_price(list_C,pw_C)
    #price_C = net.res_gen.cost[2]/net.res_gen.p_mw[2]
    print(price_A,price_B,pw_A,pw_B)
    clearing_price = max(price_A,price_B)
    return clearing_price,pw_A,pw_B,pw_C


record={
    "pw":[],
    "clearing price":[],
    "profit":[],
    "profit_A":[],
    "profit_B":[],
    "profit_C":[],
}



for wind_pw in range(276,650,10):
    clearing_price,pw_A,pw_B,pw_C=run_powerflow_without_massflow(wind_pw)
    #clearing_price_nogrid,pw_A_nogrid,pw_B_nogrid=nwp_opt(1000,price_jz1,ub_jz1,lb_jz1,price_jz2,ub_jz2,lb_jz2,ub_jz3=wind_pw)

    profit=clearing_price*wind_pw
    record["pw"].append(wind_pw)
    record["clearing price"].append(clearing_price)
    record["profit_C"].append(pw_C*clearing_price)
    record["profit_A"].append(pw_A*clearing_price)
    record["profit_B"].append(pw_B*clearing_price)
    record["profit"].append(1000*clearing_price)


record_nogrid = {
    "pw":[],
    "clearing price":[],
    "profit":[],
    "profit_A":[],
    "profit_B":[],
    "profit_C":[],
}
list_C = [[0,350,0],[350,500,340],[500,600,390]]
for wind_pw in range(276,650,10):
    clearing_price,pw_A,pw_B,pw_C=run_powerflow_without_massflow(wind_pw)
    #clearing_price_nogrid,pw_A_nogrid,pw_B_nogrid=nwp_opt(1000,price_jz1,ub_jz1,lb_jz1,price_jz2,ub_jz2,lb_jz2,ub_jz3=wind_pw)

    profit=clearing_price*wind_pw
    record_nogrid["pw"].append(wind_pw)
    record_nogrid["clearing price"].append(clearing_price)
    record_nogrid["profit_C"].append(pw_C*clearing_price)
    record_nogrid["profit_A"].append(pw_A*clearing_price)
    record_nogrid["profit_B"].append(pw_B*clearing_price)
    record_nogrid["profit"].append(1000*clearing_price)



l=1000




xlabel="风电报量/MW·h"
ylabel_map={
    "clearing price":"出清价格/(元/MW·h)",
    "profit_C":"风电收入/元",
    "profit_A":"火电商A收入/元",
    "profit_B":"火电商B收入/元",
    "profit":"社会用电总支出/元",
    }
for key,description in ylabel_map.items():
    x=[]
    y=[]
    legends=[]
    
    x.append(record["pw"])
    x.append(record_nogrid["pw"])
    y.append(record[key])
    y.append(record_nogrid[key])
    legends.append("报量不报价")
    legends.append("报量报价")
    title="风电报量_{}".format(description[:description.find("/")])
    save_path=os.path.join("cache",title+".png")
    export_fig(x,y,xlabel,description,title,legends,save_path)
exit(0)

plt.subplot(3,2,1)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("出清价格")
plt.plot(record["pw"],record["clearing price"])
plt.plot(record["pw"],record_nogrid["clearing price"])
plt.subplot(3,2,2)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("风电收入")
plt.plot(record["pw"],record["profit_C"])
plt.plot(record["pw"],record_nogrid["profit_C"])
plt.subplot(3,2,3)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("火电场A收入")
plt.plot(record["pw"],record["profit_A"])
plt.plot(record["pw"],record_nogrid["profit_A"])
plt.subplot(3,2,4)
plt.title(f"load:{l}")
plt.xlabel("风电报量")
plt.ylabel("火电厂B收入")
plt.plot(record["pw"],record["profit_B"])
plt.plot(record["pw"],record_nogrid["profit_B"])
plt.subplot(3,2,5)
plt.xlabel("风电报量")
plt.ylabel("社会总成本")
plt.plot(record["pw"],record["profit"])
plt.plot(record["pw"],record_nogrid["profit"])
plt.savefig(os.path.join("cache",f"{l}load_nwp.png"),dpi=600)
plt.cla()
plt.clf()