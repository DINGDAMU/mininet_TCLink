# !/usr/bin/python
# -*- coding:utf-8 -*-
############################
# File Name: formula1.py
# Author: dingdamu
# Mail: dingdamu@gmail.com
# Created Time: 2017-02-16 12:47:49
############################

from __future__ import division
import math
import json

pl_model = '28'
d1 = 10    # the separating distance between transmitter-receiver pair(m)
d2 = 12
d3 = 15
if cmp(pl_model, '28') == 0:
    alpha = 72.0   # dB
    beta = 2.92
    sigma = 8.7    # dB
    sigma_lin = 10**(sigma/10)
    xsi_lin = sigma_lin**2
    xsi = 10*math.log10(xsi_lin)

    def pl(d):
        return alpha + 10 * beta * math.log10(d)
elif cmp(pl_model, '73') == 0:
    alpha = 86.6   # dB
    beta = 2.45
    sigma = 8.0   # dB
    sigma_lin = 10**(sigma/10)
    xsi_lin = sigma_lin**2
    xsi = 10*math.log10(xsi_lin)

    def pl(d):
        return alpha + 10 * beta * math.log10(d)
elif cmp(pl_model, '3gpp') == 0:
    fc = 2.5

    def pl(d):
        return 22.7 + 36.7*math.log10(d) + 26*math.log10(fc)
    beta = 3.67
    alpha = 70.0    # 22.7 + 26*log10(fc)

lamda = 100.0    # density of mm-Wave links
B = 2e9         # mmWave bandwidth
C = 0.11        # fractional LoS area in the model developed


def D(d):
    return d


Gmax = 18.0    # db
Gmax_lin = 10**(Gmax/10)

Pb = 30.0    # dBm
Pb_lin = 10**(Pb/10)

pn = -174.0 + 10*(math.log10(B)) + 10       # noise power
pn_lin = 10 ** (pn/10)


def pl_lin(d):
    return 10 ** (pl(d)/10)

# the unit of pl is dB?
SNR0 = Pb + Gmax - pn
SNR_lin = 10 ** (SNR0/10)


def SNR(d):
    return SNR0 - pl(d)


def SNR_lin(d):
    return 10**(SNR(d)/10)


# xsi corresponding path-loss standard deviation
xsi_l_lin = 5.2
# xsi_l_lin = 10^(xsi_l/10)
xsi_n_lin = 7.6
# xsi_n_lin = 10^(xsi_n/10)


# beta_l_n = one_meter_loss #dB
beta_l_n = alpha    # dB
beta_l_n_lin = 10**(beta_l_n/10)

# beta_l_lin = beta_l_n_lin
# beta_n_lin = beta_l_n_lin

# ml_db = -0.1*beta_l_lin * log(10)
ml = -math.log(beta_l_n_lin)  # 10^(ml_db/10)
sigma_l = 0.1 * xsi_l_lin * math.log(10)

# mn_db = -0.1*beta_n_lin * log(10);
mn = -math.log(beta_l_n_lin)  # 10^(mn_db/10)
sigma_n = 0.1 * xsi_n_lin * math.log(10)

tau = 3.0  # pl(i)
tau_lin = 10**(tau/10)


def q_fun(x):
    return 0.5*math.erfc(x/math.sqrt(2))


def factor(d):
    return SNR_lin(d)/tau_lin   # ((Pb_lin*Gmax_lin)/(pl_lin*pn_lin))


def pc1_q1(d):
    return q_fun((math.log(D(d)**beta/factor(d))-ml)/sigma_l)


def pc1_q2(d):
    return q_fun((math.log(D(d)**pl(d)/factor(d))-mn)/sigma_n)


def pc1(d):
    return D(d)**2*(pc1_q1(d)-pc1_q2(d))


def pc_c1(sigma, m, d):
    return factor(d)**(2/beta)*math.exp(2*(sigma**2/beta**2)+2*(m/beta))


def pc_c2(sigma, m, d):
    return q_fun((sigma**2*(2/beta)-math.log(D(d)**beta/factor(d))+m)/sigma)


def pc2(d):
    return pc_c1(sigma_l, ml, d)*pc_c2(sigma_l, ml, d)


def pc3(d):
    return pc_c1(sigma_n, mn, d)*(1/C-pc_c2(sigma_n, mn, d))


def pc(d):
    return pc1(d)+pc2(d)+pc3(d)


def Lamda_a(d):
    return lamda*math.pi*C*pc(d)


def Ma(d):
    return Lamda_a(d)/lamda


def ps(d):
    return 1-math.exp(-lamda*Ma(d)*factor(d))


def p_loss(d):
    return (1-float(ps(d)))*100


annotation = {
            "apps": {
                "org.onosproject.millimeterwavelink": {
                    "links": [{
                        "src": "of:000000000000000b/4",
                        "dst": "of:000000000000000e/3",
                        "length": d1,
                        "capacity": "200",
                        "technology": "mmwave",
                        "ps": 100 - p_loss(d1)
                        }]
                    }
                }
            }

annotation2 = {
            "apps": {
                "org.onosproject.millimeterwavelink": {
                    "links": [{
                        "src": "of:000000000000000d/4",
                        "dst": "of:000000000000000f/4",
                        "length": d2,
                        "capacity": "200",
                        "technology": "mmwave",
                        "ps": 100 - p_loss(d2)
                        }]
                    }
                }
            }

annotation3 = {
            "apps": {
                "org.onosproject.millimeterwavelink": {
                    "links": [{
                        "src": "of:000000000000000d/3",
                        "dst": "of:000000000000000e/4",
                        "length": d3,
                        "capacity": "200",
                        "technology": "mmwave",
                        "ps": 100 - p_loss(d3)
                        }]
                    }
                }
            }


def onosjson():
    fp1 = open("cfg.json", "w")
    fp1.write(json.dumps(annotation, indent=4, separators=(',', ': ')))
    fp1.close()
    fp2 = open("cfg2.json", "w")
    fp2.write(json.dumps(annotation2,indent=4, separators=(',', ': ')))
    fp2.close()
    fp3 = open("cfg3.json", "w")
    fp3.write(json.dumps(annotation3,indent=4, separators=(',', ': ')))
    fp3.close()

if __name__ == '__main__':
    onosjson()
