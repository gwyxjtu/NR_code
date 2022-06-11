import os
import json

from nan_without_price import nwp_opt
list_A = [[170,170,330],[170,200,340],[200,210,380]]
list_B = [[0,250,290],[250,350,300],[350,520,360]]
list_C = [[0,350,0],[350,450,340],[450,600,370]]

record_nogrid = {
    "pw":[],
    "clearing price":[],
    "profit":[],
    "profit_A":[],
    "profit_B":[],
    "profit_C":[],
}
price_jz1 = [list_A[i][2] for i in range(3)]   # 机组1
ub_jz1 = [190,10,10]
lb_jz1 = [170,0,0]
price_jz2 = [list_B[i][2] for i in range(3)]   # 机组2
ub_jz2 = [250,110,160]
lb_jz2 = [0,0,0]
# print(price_jz1,ub_jz1,lb_jz1,price_jz2,ub_jz2,lb_jz2)
# exit(0)
for wind_pw in range(276,650,10):
    
    clearing_price_nogrid,pw_A_nogrid,pw_B_nogrid=nwp_opt(1000,price_jz1,ub_jz1,lb_jz1,price_jz2,ub_jz2,lb_jz2,ub_jz3=wind_pw)
    profit=clearing_price_nogrid*wind_pw
    pw_C_nogrid = 1000 - pw_A_nogrid - pw_B_nogrid
    record_nogrid["pw"].append(wind_pw)
    record_nogrid["clearing price"].append(clearing_price_nogrid)
    record_nogrid["profit_C"].append(pw_C_nogrid*clearing_price_nogrid)
    record_nogrid["profit_A"].append(pw_A_nogrid*clearing_price_nogrid)
    record_nogrid["profit_B"].append(pw_B_nogrid*clearing_price_nogrid)
    record_nogrid["profit"].append(1000*clearing_price_nogrid)


with open("record_nogrid.json", 'w') as f:
    f.write(json.dumps(record_nogrid))