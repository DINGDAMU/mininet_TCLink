# mininet_TCLink
An example for testing packet loss and latency between hosts with TCLink

#Usage 
Create network topology in mininet  

        python topo.py  

Testing packet loss and latency between hosts 

        h1 ping h2
        h2 ping h3
        ...etc,

#Description
        net = Mininet(topo, switch=OVSKernelSwitch, controller=RemoteController, link=TCLink)
Set link to TCLink so that we can measure the packet loss and latency.  

        self.addLink(s10, h1, bw=20, delay='5ms', loss=10, use_htb=True)  
        self.addLink(s12, h2, bw=30, delay='5ms', loss=0, use_htb=True)  
        self.addLink(s11, h3, bw=10, delay='10ms', loss=10, use_htb=True) 
**bw** = link bandwidth  
**delay** = packet delay time  
**loss** = packet loss rate   
**use_htb** = use Hierarchical token bucket  
The **hierarchical token bucket (HTB)** is a faster replacement for the class-based queueing (CBQ) queuing discipline in Linux. It is useful to limit a client's download/upload rate so that the limited client cannot saturate the total bandwidth.




