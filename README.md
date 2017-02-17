# mininet_TCLink
A mininet example for testing packet loss and latency between hosts in the network by TCLink
# Packet loss formula  
        p_{ s }=1-exp(-\lambda M_{ a }(\frac{P_{ b }G_{ max }}{\tau\sigma_N^2}))
        M_a(t) =\frac{\Lambda_a((0,t])}{\lambda}
        \Lambda_a((0,t]) = \lambda \pi C\{D^2[ Q(\frac{\ln{D^{\alpha_l}/t}-m_l}{\sigma_l})-Q(\frac{\ln{D^{\alpha_n}/t}-m_n}{\sigma_n})]+ t^{2/\alpha_l}exp(2\frac{\sigma_l^2}{\alpha_l^2}+2\frac{m_l}{\alpha_l})Q(\frac{\sigma_l^2(2/\alpha_l)-\ln{D^{\alpha_l/t}}+m_l}{\sigma_l})+t^{2/\alpha_n}exp(2\frac{\sigma_n^2}{\alpha_n^2}+2\frac{m_n}{\alpha_n})[\frac{1}{C}-Q(\frac{\sigma_n^2(2/\alpha_n)-\ln{D^{\alpha_n/t}}+m_n}{\sigma_n})]\}

# Usage 
Create network topology in mininet  

        sudo python topo.py  

Testing packet loss and latency between hosts 

        h1 ping h2
        h2 ping h3
        ...etc,

# Description
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




