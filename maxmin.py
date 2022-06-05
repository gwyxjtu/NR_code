from nan import nan_opt
from nan_without_price import nwp_opt
from config import load,cache_dir
import os
from matplotlib import pyplot as plt

plt.style.use('ggplot')

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)

def export_fig(x,y,xlabel,ylabel,title,legends,save_path):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i in range(len(x)):
        plt.plot(x[i],y[i],label=legends[i])
    plt.legend()
    plt.savefig(save_path,dpi=600)
    plt.clf()
    plt.cla()

total_record={}

for l in load:
    record={
        "pw":[],
        "clearing price":[],
        "profit":[],
        "profit_A":[],
        "profit_B":[],
        "profit_C":[],
    }
    lb=l-1700
    ub=min(l-500,800)
    for pw in range(lb,ub,10):
        clearing_price,pw_A,pw_B=nwp_opt(l,ub_jz3=pw)
        profit=clearing_price*pw
        record["pw"].append(pw)
        record["clearing price"].append(clearing_price)
        record["profit_C"].append(profit)
        record["profit_A"].append(pw_A*clearing_price)
        record["profit_B"].append(pw_B*clearing_price)
        record["profit"].append(l*clearing_price)
    total_record[l]=record

load.sort()
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
    for l in load:
        x.append(total_record[l]["pw"])
        y.append(total_record[l][key])
        legends.append(l)
    title="风电报量_{}".format(description[:description.find("/")])
    save_path=os.path.join(cache_dir,title+".png")
    export_fig(x,y,xlabel,description,title,legends,save_path)

 