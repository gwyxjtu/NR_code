from nan import nan_opt
from nan_without_price import nwp_opt
from config import load,cache_dir
import os
from matplotlib import pyplot as plt

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)

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