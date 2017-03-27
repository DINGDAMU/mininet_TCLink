# mininet_TCLink
A mininet example for testing packet loss and latency between hosts in the network by TCLink



# Probability of success formula  

<img src="http://latex.codecogs.com/gif.latex?p_%7B%20s%20%7D=1-exp(-%20%5Clambda%20M_%7B%20a%20%7D(%5Cfrac%7BP_%7Bb%7DG_%7B%20max%20%7D%7D%7B%5Ctau%5Csigma_N%5E2%7D))"/>
<img src="http://latex.codecogs.com/gif.latex?M_a(t)%20=%5Cfrac%7B%5CLambda_a((0,t%5D)%7D%7B%5Clambda%7D"/>
<img src="http://latex.codecogs.com/gif.latex?%5CLambda_a((0,t%5D)%20=%20%5Clambda%20%5Cpi%20C%5C%7BD%5E2%5B%20Q(%5Cfrac%7B%5Cln%7BD%5E%7B%5Calpha_l%7D/t%7D-m_l%7D%7B%5Csigma_l%7D)-Q(%5Cfrac%7B%5Cln%7BD%5E%7B%5Calpha_n%7D/t%7D-m_n%7D%7B%5Csigma_n%7D)%5D+%20t%5E%7B2/%5Calpha_l%7Dexp(2%5Cfrac%7B%5Csigma_l%5E2%7D%7B%5Calpha_l%5E2%7D+2%5Cfrac%7Bm_l%7D%7B%5Calpha_l%7D)Q(%5Cfrac%7B%5Csigma_l%5E2(2/%5Calpha_l)-%5Cln%7BD%5E%7B%5Calpha_l/t%7D%7D+m_l%7D%7B%5Csigma_l%7D)+t%5E%7B2/%5Calpha_n%7Dexp(2%5Cfrac%7B%5Csigma_n%5E2%7D%7B%5Calpha_n%5E2%7D+2%5Cfrac%7Bm_n%7D%7B%5Calpha_n%7D)%5B%5Cfrac%7B1%7D%7BC%7D-Q(%5Cfrac%7B%5Csigma_n%5E2(2/%5Calpha_n)-%5Cln%7BD%5E%7B%5Calpha_n/t%7D%7D+m_n%7D%7B%5Csigma_n%7D)%5D%5C%7D"/>

**Ps**: probability of success  
**Λa**:denotes the intensity measure for the corresponding Poisson Point Process (PPP) of the mm-Wave links that incur in a path-loss greater than the threshold t when the path-loss distribution is proven to follow an exponential distribution  
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
1.Modify the needed parameter in formula.py, and it can create a Json file to be adopted in ONOS automatically    

        sudo python formula.py

2.Create network topology in mininet   

        sudo python topo.py  

3.Testing packet loss and latency between hosts 

        h1 ping h2
        h2 ping h3
        ...etc,

# Description
        net = Mininet(topo, switch=OVSKernelSwitch, controller=RemoteController, link=TCLink)
Set link to TCLink so that we can measure the packet loss and latency.  

        self.addLink(s10, h1, bw=20, delay='5ms', loss=formula.p_loss(10), use_htb=True)  
        self.addLink(s12, h2, bw=30, delay='5ms', loss=formula.p_loss(8), use_htb=True)  
        self.addLink(s11, h3, bw=10, delay='10ms', loss=formula.p_loss(6), use_htb=True) 
**bw** = link bandwidth  
**delay** = packet delay time  
**loss** = packet loss rate   
**use_htb** = use Hierarchical token bucket  
The **hierarchical token bucket (HTB)** is a faster replacement for the class-based queueing (CBQ) queuing discipline in Linux. It is useful to limit a client's download/upload rate so that the limited client cannot saturate the total bandwidth.


        
        p_loss(d) = (1-Ps(d))*100 
        
**p_loss** must be an integer from 0 to 100  
**d** is the separating distance between transmitter-receiver pair(m), and it's called **link length** in our case.  
The long distance leads the high packet loss, which may cause the link to be indirectional.  
For this reason, it's highly recommended to set the distance lower than 15m, otherwise the link will not work.


# A json example:  
    {
     "apps" : {
    "org.onosproject.millimeterwavelink" : {
      "links" : [{
        "src":"of:000000000000000e/5",
        "dst":"of:000000000000000f/3",
        "length": formula.d,
        "capacity":"100",
        "technology":"mmwave",
        "ps": 100-p_loss(d)
      }]
    },
    "org.onosproject.millimeterwaveport" : {
      "ports" : [{
        "technology":"mmwave",
        "deviceID": "of:000000000000000a",
        "portnumber":"1",
        "isEnabled":"true"
      }]
     }
    }


