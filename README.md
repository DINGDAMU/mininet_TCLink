# mininet_TCLink
A mininet example for testing packet loss and latency between hosts in the network by TCLink



# Probability of success formula  
![](http://latex.codecogs.com/gif.latex?\p_{ s }=1-exp(- \\lambda M_{ a }(\\frac{P_{b}G_{ max }}{\\tau\\sigma_N^2})))  
![](http://latex.codecogs.com/gif.latex?\M_a(t) =\\frac{\\Lambda_a(\(0,t\])}{\\lambda})  
![](http://latex.codecogs.com/gif.latex?\\Lambda_a(\(0,t\]) = \\lambda \\pi C\\{D^2[ Q(\\frac{\\ln{D^{\\alpha_l}/t}-m_l}{\\sigma_l})-Q(\\frac{\\ln{D^{\\alpha_n}/t}-m_n}{\\sigma_n})]+ t^{2/\\alpha_l}exp(2\\frac{\\sigma_l^2}{\\alpha_l^2}+2\\frac{m_l}{\\alpha_l})Q(\\frac{\\sigma_l^2(2/\\alpha_l)-\\ln{D^{\\alpha_l/t}}+m_l}{\\sigma_l})+t^{2/\\alpha_n}exp(2\\frac{\\sigma_n^2}{\\alpha_n^2}+2\\frac{m_n}{\\alpha_n})[\\frac{1}{C}-Q(\\frac{\\sigma_n^2(2/\\alpha_n)-\\ln{D^{\\alpha_n/t}}+m_n}{\\sigma_n})]\\})  

**Ps**: probability of success
Λa:denotes the intensity measure for the corresponding Poisson Point Process (PPP) of the mm-Wave links that incur in a path-loss greater than the threshold t when the path-loss distribution is proven to follow an exponential distribution  
**λ** : the density of mm-Wave links  
**D** : the separating distance between transmitter-receiver pair  
**C** : the fractional LoS area in the model developed  
**Q()** : the standard Gaussian Q-function  
**αl** : the path-loss exponents for LoS condition  
**αn** : the path-loss exponents for NLoS condition  
m_j=-0.1β_jln⁡10  
σ_j=0.1ξ_j  
where **j** is the model parameter, **j** = l or n  
**ξj** : the corresponding path-loss standard deviation.  




# Usage 
1.Modify the needed parameter in topo.py   

2.Create network topology in mininet   

        sudo python topo.py  

3.Testing packet loss and latency between hosts 

        h1 ping h2
        h2 ping h3
        ...etc,

# Description
        net = Mininet(topo, switch=OVSKernelSwitch, controller=RemoteController, link=TCLink)
Set link to TCLink so that we can measure the packet loss and latency.  

        self.addLink(s10, h1, bw=20, delay='5ms', loss=p_loss, use_htb=True)  
        self.addLink(s12, h2, bw=30, delay='5ms', loss=p_loss, use_htb=True)  
        self.addLink(s11, h3, bw=10, delay='10ms', loss=p_loss, use_htb=True) 
**bw** = link bandwidth  
**delay** = packet delay time  
**loss** = packet loss rate   
**use_htb** = use Hierarchical token bucket  
The **hierarchical token bucket (HTB)** is a faster replacement for the class-based queueing (CBQ) queuing discipline in Linux. It is useful to limit a client's download/upload rate so that the limited client cannot saturate the total bandwidth.

In my case, p_loss = (1-Ps)*100   
p_loss must be a integer


