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

        self.addLink(s10, s13)    # sa/2-sd/1
        self.addLink(s10, s13, loss=formula.p_loss(formula.d4))    # sa/3-sd/2
        self.addLink(s11, s14)    # sb/2-se/1
        self.addLink(s11, s14)    # sb/3-se/2
        self.addLink(s11, s14, loss=formula.p_loss(formula.d1))    # sb/4-se/3
        self.addLink(s12, s15)    # sc/2-sf/1
        self.addLink(s12, s15)    # sc/3-sf/3
        self.addLink(s13, s14, loss=formula.p_loss(formula.d3))    # sd/3-se/4
        self.addLink(s14, s15)    # se/5-sf/3
        self.addLink(s13, s15, loss=formula.p_loss(formula.d2))    # sd/4-sf/4
        self.addLink(s10, s16, loss=formula.p_loss(formula.d5))    # sa/4-sg/2
        self.addLink(s12, s16)    # sc/4-sg/3
        self.addLink(s13, s16)    # sd/5-sg/4

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
