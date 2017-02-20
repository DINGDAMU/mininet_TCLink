#!/usr/bin/python
from __future__ import division
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch, UserSwitch
from mininet.link import TCLink
import math


pl_model = '28'
d = 10 #the separating distance between transmitter-receiver pair
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
    pl = alpha + 10* beta * log10(d)
elif cmp(pl_model, '3gpp') == 0:
    fc = 2.5
    pl = 22.7 + 36.7*math.log10(d) + 26*math.log10(fc)
    beta = 3.67
    alpha=70 #22.7 + 26*log10(fc)


lamda =100 #density of mm-Wave links
B = 2e9 #mmWave bandwidth
C = 0.11 #fractional LoS area in the model developed
D = d
Gmax = 18 #db
Gmax_lin = 10**(Gmax/10)

Pb = 30 #dBm
Pb_lin = 10**(Pb/10)

pn = -174 + 10*(math.log10(B)) + 10 # noise power
pn_lin = 10 ** (pn/10)
pl_lin = 10 ** (pl/10)

#the unit of pl is dB?
SNR = Pb + Gmax -pn -pl
SNR_lin = 10 ** (SNR/10)

#xsi corresponding path-loss standard deviation
xsi_l_lin=5.2
#xsi_l_lin = 10^(xsi_l/10)
xsi_n_lin = 7.6
#xsi_n_lin = 10^(xsi_n/10)


#beta_l_n = one_meter_loss(alpha) #dB
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

tau = 3  # pl(i)
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

class SingleSwitchTopo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        s10 = self.addSwitch( 's10', dpid = '000000000000000A', protocols='OpenFlow13')
        s11 = self.addSwitch( 's11', dpid = '000000000000000B', protocols='OpenFlow13')
        s12 = self.addSwitch( 's12', dpid = '000000000000000C', protocols='OpenFlow13')
        s13 = self.addSwitch( 's13', dpid = '000000000000000D', protocols='OpenFlow13')
        s14 = self.addSwitch( 's14', dpid = '000000000000000E', protocols='OpenFlow13')
        s15 = self.addSwitch( 's15', dpid = '000000000000000F', protocols='OpenFlow13')

        h1 = self.addHost( 'h1', ip='10.0.0.1', mac='000000000001')
        h2 = self.addHost( 'h2', ip='10.0.0.2', mac='000000000002')
        h3 = self.addHost( 'h3', ip='10.0.0.3', mac='000000000003')


        self.addLink(s10, h1, bw=20, delay='5ms', loss=p_loss, use_htb=True)
        self.addLink(s12, h2, bw=30, delay='5ms', loss=p_loss, use_htb=True)
        self.addLink(s11, h3, bw=10, delay='10ms', loss=p_loss, use_htb=True)


        self.addLink(s10, s13) #sa/2-sd/1
        self.addLink(s10, s13) #sa/3-sd/2
        self.addLink(s11, s14) #sb/2-se/1
        self.addLink(s11, s14) #sb/3-se/2
        self.addLink(s11, s14) #sb/4-se/3
        self.addLink(s12, s15) #sc/2-sf/1
        self.addLink(s12, s15) #sc/3-sf/3
        self.addLink(s13, s14) #sd/3-se/4
        self.addLink(s14, s15) #se/5-sf/3
        self.addLink(s13, s15) #sd/4-sf/4

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo, switch=OVSKernelSwitch, controller=RemoteController, link=TCLink)

    c1 =  RemoteController( 'c1', ip='192.168.56.1' )
    net.addController(c1)
    net.staticArp()
    net.start()
#    h1,h3=net.get('h1','h3')
#   net.iperf((h1,h3))
    #print "Dumping host connections
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
