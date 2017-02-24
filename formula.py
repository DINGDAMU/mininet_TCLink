#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: formula1.py
#Author: dingdamu  
#Mail: dingdamu@gmail.com  
#Created Time: 2017-02-16 12:47:49
############################  

from __future__ import division
import math
import json
from numpy import *

pl_model = '28'
d = 10    #the separating distance between transmitter-receiver pair(m)
if cmp(pl_model, '28') == 0:
    alpha = 72.0 #dB
    beta = 2.92
    sigma = 8.7 #dB
    sigma_lin = 10**(sigma/10)
    xsi_lin = sigma_lin**2
    xsi = 10*math.log10(xsi_lin)
    pl = alpha + 10* beta * math.log10(d)
elif cmp(pl_model, '73') == 0:
    alpha = 86.6 #dB
    beta = 2.45
    sigma = 8.0 #dB
    sigma_lin = 10**(sigma/10)
    xsi_lin = sigma_lin**2
    xsi = 10*math.log10(xsi_lin)
    pl = alpha + 10* beta * math.log10(d)
elif cmp(pl_model, '3gpp') == 0:
    fc = 2.5
    pl = 22.7 + 36.7*math.log10(d) + 26*math.log10(fc)
    beta = 3.67
    alpha=70.0 #22.7 + 26*log10(fc)


lamda =100.0 #density of mm-Wave links
B = 2e9 #mmWave bandwidth
C = 0.11 #fractional LoS area in the model developed
D = d
Gmax = 18.0 #db
Gmax_lin = 10**(Gmax/10)

Pb = 30.0 #dBm
Pb_lin = 10**(Pb/10)

pn = -174.0 + 10*(math.log10(B)) + 10 # noise power
pn_lin = 10 ** (pn/10)


pl_lin = 10** (pl/10)

#the unit of pl is dB?
SNR0 = Pb + Gmax -pn
SNR_lin = 10 ** (SNR0/10)
SNR = SNR0 - pl
SNR_lin = 10**(SNR/10)


#xsi corresponding path-loss standard deviation
xsi_l_lin=5.2
#xsi_l_lin = 10^(xsi_l/10)
xsi_n_lin = 7.6
#xsi_n_lin = 10^(xsi_n/10)


#beta_l_n = one_meter_loss #dB
beta_l_n = alpha #dB
beta_l_n_lin = 10**(beta_l_n/10)

# beta_l_lin = beta_l_n_lin
# beta_n_lin = beta_l_n_lin

# ml_db = -0.1*beta_l_lin * log(10)
ml = -math.log(beta_l_n_lin)  # 10^(ml_db/10)
sigma_l = 0.1* xsi_l_lin * math.log(10)

# mn_db = -0.1*beta_n_lin * log(10);
mn = -math.log(beta_l_n_lin)  # 10^(mn_db/10)
sigma_n = 0.1* xsi_n_lin * math.log(10)

tau = 3.0  # pl(i)
tau_lin = 10**(tau/10)

def q_fun(x):
    return 0.5*math.erfc(x/math.sqrt(2))

def factor():
    return SNR_lin/tau_lin #((Pb_lin*Gmax_lin)/(pl_lin*pn_lin))


def pc1_q1(sigma_l,ml):
    return q_fun((math.log(D**beta/factor())-ml)/sigma_l)

def pc1_q2(sigma_n,mn):
    return q_fun((math.log(D**pl/factor())-mn)/sigma_n)

def pc1(sigma_l,ml,sigma_n,mn):
    return D**2*(pc1_q1(sigma_l,ml)-pc1_q2(sigma_n,mn))

def pc_c1(sigma,m):
    return factor()**(2/beta)*math.exp(2*(sigma**2/beta**2)+2*(m/beta))

def pc_c2(sigma,m):
    return q_fun((sigma**2*(2/beta)-math.log(D**beta/factor())+m)/sigma)

def pc2(sigma_l,ml):
     return pc_c1(sigma_l,ml)*pc_c2(sigma_l,ml)

def pc3(sigma_n,mn):
    return pc_c1(sigma_n,mn)*(1/C-pc_c2(sigma_n,mn))

def pc(sigma_l,ml,sigma_n,mn):
    return pc1(sigma_l,ml,sigma_n,mn)+pc2(sigma_l,ml)+pc3(sigma_n,mn)

def Lamda_a(sigma_l,ml,sigma_n,mn):
    return lamda*math.pi*C*pc(sigma_l,ml,sigma_n,mn)

def Ma(sigma_l,ml,sigma_n,mn):
    return Lamda_a(sigma_l,ml,sigma_n,mn)/lamda

def ps(sigma_l,ml,sigma_n,mn):
    return 1-math.exp(-lamda*Ma(sigma_l,ml,sigma_n,mn)*factor())

p_loss =(1-float(ps(sigma_l,ml,sigma_n,mn)))*100

annotation = {
            "apps":{
                "org.onosproject.millimeterwavelink":{
                    "links":[{
                        "src":"of:000000000000000e/5",
                        "dst":"of:000000000000000f/3",
                        "length": "100",
                        "capacity":"200",
                        "technology":"mmwave",
                        "ps": 100 - p_loss
                        }]
                    },
                "org.onosproject.millimeterwaveport":{
                    "ports":[{
                        "technology":"mmwave",
                        "deviceID": "of:000000000000000a",
                        "portnumber":"1",
                        "isEnabled":"true"
                        }]
                    }
                },
            "devices": {
                "of:000000000000000a": {
                    "basic": {
                        "allowed": "true",
                        "owner": "Luigi",
                        "driver": "softrouter"
                        }
                    }
                },
            "links": {
                "of:000000000000000e/5-of:000000000000000f/3": {
                    "basic": {
                        "bandwidth": "2000",
                        "allowed": "true",
                        "metric": "100",
                        "latency": "20"
                        }
                    }
                },
            "hosts": {
                "00:00:00:00:00:01/None": {
                    "basic": {
                        "name":"host1"
                        }
                    }
                },
            "ports": {
                "of:000000000000000a/1": {
                    "interfaces": [
                        {
                            "name":"port1"
                            }
                        ]
                    },
                "of:000000000000000b/2": {
                    "interfaces": [
                        {
                            "name":"port2"
                            }
                        ]
                    }
                }
            }
def onosjson():
    fp = open("cfg.json","w")
    fp.write(json.dumps(annotation,sort_keys=True,indent = 2))
    fp.close()

if __name__ == '__main__':
    onosjson()
