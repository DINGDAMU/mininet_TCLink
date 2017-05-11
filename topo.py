#!/usr/bin/python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
import formula


class SingleSwitchTopo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        s10 = self.addSwitch('s10', dpid=formula.s10_id,
                             protocols='OpenFlow13')
        s11 = self.addSwitch('s11', dpid=formula.s11_id,
                             protocols='OpenFlow13')
        s12 = self.addSwitch('s12', dpid=formula.s12_id,
                             protocols='OpenFlow13')
        s13 = self.addSwitch('s13', dpid=formula.s13_id,
                             protocols='OpenFlow13')
        s14 = self.addSwitch('s14', dpid=formula.s14_id,
                             protocols='OpenFlow13')
        s15 = self.addSwitch('s15', dpid=formula.s15_id,
                             protocols='OpenFlow13')
        s16 = self.addSwitch('s16', dpid=formula.s16_id,
                             protocols='OpenFlow13')

        h1 = self.addHost('h1', ip='10.0.0.1', mac='000000000001')
        h2 = self.addHost('h2', ip='10.0.0.2', mac='000000000002')
        h3 = self.addHost('h3', ip='10.0.0.3', mac='000000000003')
        h4 = self.addHost('h4', ip='10.0.0.4', mac='000000000004')

        self.addLink(s10, h1)
        self.addLink(s12, h2)
        self.addLink(s11, h3)
        self.addLink(s16, h4)

        self.addLink(s10, s13, bw=formula.band_sa_sd,
                     delay=str(formula.lat_sa_sd) + "ms")    # sa/2-sd/1
        self.addLink(s10, s13, loss=formula.p_loss(formula.d4),
                     bw=formula.band_sa_sd2,
                     delay=str(formula.lat_sa_sd2) + "ms")    # sa/3-sd/2
        self.addLink(s11, s14, bw=formula.band_sb_se,
                     delay=str(formula.lat_sb_se) + "ms")    # sb/2-se/1
        self.addLink(s11, s14, bw=formula.band_sb_se2,
                     delay=str(formula.lat_sb_se2) + "ms")    # sb/3-se/2
        self.addLink(s11, s14, loss=formula.p_loss(formula.d1),
                     bw=formula.band_sb_se3,
                     delay=str(formula.lat_sb_se3) + "ms")    # sb/4-se/3
        self.addLink(s12, s15,
                     bw=formula.band_sc_sf,
                     delay=str(formula.lat_sc_sf) + "ms")    # sc/2-sf/1
        self.addLink(s12, s15,
                     bw=formula.band_sc_sf2,
                     delay=str(formula.lat_sc_sf2) + "ms")    # sc/3-sf/3
        self.addLink(s13, s14, loss=formula.p_loss(formula.d3),
                     bw=formula.band_sd_se,
                     delay=str(formula.lat_sd_se) + "ms")    # sd/3-se/4
        self.addLink(s14, s15, bw=formula.band_se_sf,
                     delay=str(formula.lat_se_sf) + "ms")    # se/5-sf/3
        self.addLink(s13, s15, loss=formula.p_loss(formula.d2),
                     bw=formula.band_sd_sf,
                     delay=str(formula.lat_sd_sf) + "ms")    # sd/4-sf/4
        self.addLink(s10, s16, loss=formula.p_loss(formula.d5),
                     bw=formula.band_sa_sg,
                     delay=str(formula.lat_sa_sg) + "ms")    # sa/4-sg/2
        self.addLink(s12, s16, bw=formula.band_sc_sg,
                     delay=str(formula.lat_sc_sg) + "ms")    # sc/4-sg/3
        self.addLink(s13, s16, bw=formula.band_sd_sg,
                     delay=str(formula.lat_sd_sg) + "ms")    # sd/5-sg/4


def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo, switch=OVSKernelSwitch, controller=RemoteController,
                  link=TCLink)

    c1 = RemoteController('c1', ip='192.168.56.1')
    net.addController(c1)
    net.start()
#   print "Dumping host connections
    CLI(net)    # waiting for insert command
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
