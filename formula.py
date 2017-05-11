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
d1 = 10.0    # the separating distance between transmitter-receiver pair(m)
d2 = 12.0
d3 = 8.0
d4 = 9.0
d5 = 9.5
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


s10_id = '000000000000000a'
s11_id = '000000000000000b'
s12_id = '000000000000000c'
s13_id = '000000000000000d'
s14_id = '000000000000000e'
s15_id = '000000000000000f'
s16_id = '000000000000001a'

sb_se = 4
se_sb = 3
sd_se = 3
se_sd = 4
sd_sf = 4
sf_sd = 4
sd_sa = 2
sa_sd = 3
sa_sg = 4
sg_sa = 2

annotation = {
            "apps": {
                "org.onosproject.millimeterwavelink": {
                    "links": [{
                        "src": "of:"+s11_id+"/"+str(sb_se),
                        "dst": "of:"+s14_id+"/"+str(se_sb),
                        "length": d1,
                        "capacity": "200",
                        "technology": "mmwave",
                        },
                        {
                        "src": "of:"+s13_id+"/"+str(sd_sf),
                        "dst": "of:"+s15_id+"/"+str(sf_sd),
                        "length": d2,
                        "capacity": "200",
                        "technology": "mmwave",
                        },
                        {
                        "src": "of:"+s13_id+"/"+str(sd_se),
                        "dst": "of:"+s14_id+"/"+str(se_sd),
                        "length": d3,
                        "capacity": "200",
                        "technology": "mmwave",
                        },
                        {
                        "src": "of:"+s13_id+"/"+str(sd_sa),
                        "dst": "of:"+s10_id+"/"+str(sa_sd),
                        "length": d4,
                        "capacity": "200",
                        "technology": "mmwave",
                        },
                        {
                        "src": "of:"+s10_id+"/"+str(sa_sg),
                        "dst": "of:"+s16_id+"/"+str(sg_sa),
                        "length": d5,
                        "capacity": "200",
                        "technology": "mmwave",
                        }
                    ]
                    }
                }
            }
band_sa_sd = 100
lat_sa_sd = 10
band_sa_sd2 = 200
lat_sa_sd2 = 8
band_sa_sg = 300
lat_sa_sg = 7
band_sb_se = 150
lat_sb_se = 8
band_sb_se2 = 130
lat_sb_se2 = 10
band_sb_se3 = 120
lat_sb_se3 = 3
band_sc_sf = 80
lat_sc_sf = 6
band_sc_sf2 = 165
lat_sc_sf2 = 8
band_sd_se = 220
lat_sd_se = 13
band_se_sf = 100
lat_se_sf = 9
band_sd_sf = 230
lat_sd_sf = 18
band_sc_sg = 350
lat_sc_sg = 22
band_sd_sg = 170
lat_sd_sg = 12

bandwidthannotation = {
    "links": {
      "of:000000000000000a/2-of:000000000000000d/1": {
        "basic": {
            "bandwidth": band_sa_sd,
            "latency": lat_sa_sd
                }
      },
      "of:000000000000000a/3-of:000000000000000d/2": {
        "basic": {
          "bandwidth": band_sa_sd2,
          "latency": lat_sa_sd2
        }
      },
      "of:000000000000000a/4-of:000000000000001a/2": {
        "basic": {
          "bandwidth": band_sa_sg,
          "latency": lat_sa_sg
        }
      },
      "of:000000000000000b/2-of:000000000000000e/1": {
        "basic": {
          "bandwidth": band_sb_se,
          "latency": lat_sb_se
        }
      },
      "of:000000000000000b/3-of:000000000000000e/2": {
        "basic": {
          "bandwidth": band_sb_se2,
          "latency": lat_sb_se2
        }
      },
      "of:000000000000000b/4-of:000000000000000e/3": {
        "basic": {
          "bandwidth": band_sb_se3,
          "latency": lat_sb_se3
        }
      },
      "of:000000000000000c/2-of:000000000000000f/1": {
        "basic": {
          "bandwidth": band_sc_sf,
          "latency": lat_sc_sf
        }
      },
      "of:000000000000000d/3-of:000000000000000e/4": {
        "basic": {
          "bandwidth": band_sd_se,
          "latency": lat_sd_se
        }
      },
      "of:000000000000000f/3-of:000000000000000e/5": {
        "basic": {
          "bandwidth": band_se_sf,
          "latency": lat_se_sf
        }
      },
      "of:000000000000001a/4-of:000000000000000d/5": {
        "basic": {
          "bandwidth": band_sd_sg,
          "latency": lat_sd_sg
        }
      },
      "of:000000000000000d/4-of:000000000000000f/4": {
        "basic": {
          "bandwidth": band_sd_sf,
          "latency": lat_sd_sf
        }
      },
      "of:000000000000001a/3-of:000000000000000c/4": {
        "basic": {
          "bandwidth": band_sc_sg,
          "latency": lat_sc_sg
        }
      },
      "of:000000000000000f/2-of:000000000000000c/3": {
        "basic": {
          "bandwidth": band_sc_sf2,
          "latency": lat_sc_sf2
        }
      }
    }
   }


def onosjson():
    fp = open("cfg.json", "w")
    fp.write(json.dumps(annotation, indent=4, separators=(',', ': ')))
    fp.close()
    fp1 = open("cfgb.json", "w")
    fp1.write(json.dumps(bandwidthannotation, indent=4, separators=(',', ':')))
    fp1.close()
if __name__ == '__main__':
    onosjson()
