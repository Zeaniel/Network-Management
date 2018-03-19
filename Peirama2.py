# !/usr/bin/python

"""
Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"
http://ieeexplore.ieee.org/document/7859348/ 
"""

import os
import time
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI

import sys
gnet=None

# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here

switch_pkt = 'switch-pkt.vanetdata'
switch_throughput = 'switch-throughput.vanetdata'
c0_pkt = 'c0-pkt.vanetdata'
c0_throughput = 'c0-throughput.vanetdata'
value_=0
timeTask = 20



def graphic():

     f1 = open('./' + switch_pkt, 'r')
     eth0 = f1.readlines()
     f1.close()

     f11 = open('./' + switch_throughput, 'r')
     eth01 = f11.readlines()
     f11.close()

     f2 = open('./' + c0_pkt, 'r')
     wlan0 = f2.readlines()
     f2.close()

     f21 = open('./' + c0_throughput, 'r')
     wlan01 = f21.readlines()
     f21.close()
 

     l1 = []
     l2 = []
     t = []
     ll1 = []
     ll2 = []

     t1 = []
     t2 = []
     tt1 = []
     tt2 = []

     i = 0
     for x in eth0:

             p = x.split()
    
             l1.append(int(p[0]))    

             if len(l1) > 1:

                  ll1.append(l1[i] - l1[i - 1])
    
             i += 1

     i = 0

     for x in eth01:
         
             p = x.split()
         
             t1.append(int(p[0]))
        
             if len(t1) > 1:
             
                  tt1.append(t1[i] - t1[i - 1])

             i += 1
     i = 0
    
     for x in wlan0:
         
            p = x.split()

            l2.append(int(p[0]))
       
            if len(l2) > 1:
             
                 ll2.append(l2[i] - l2[i - 1])
         
            i += 1
     
     i = 0
  
     for x in wlan01:
         
            p = x.split()
         
            t2.append(int(p[0]))

         
            if len(t2) > 1:
             
                 tt2.append(t2[i] - t2[i - 1])
         
            i += 1
     
     i = 0
   
     for x in range(len(ll1)):
         
            t.append(i)
 
            print (i)
         
            i = i + 0.5
     
     fig, ax1 = plt.subplots()
     
     print 'A'

     ax2 = ax1.twinx()

     print 'B'
     
     ax1.plot(t, ll1, color='red', label='Received Data (client)', ls="--", markevery=7, linewidth=1)
     
     print 'C'

     #ax1.plot(t, ll2, color='black', label='Transmited Data (server)', markevery=7, linewidth=1)

     print 'D'
     
     #ax2.plot(t, tt1, color='red', label='Throughput (client)', ls="-.", markevery=7, linewidth=1)

     print 'E'
     
     ax2.plot(t, tt2, color='black', label='Throughput (server)', ls=':', markevery=7, linewidth=1)

     print 'F'
     
     ax1.legend(loc=2, borderaxespad=0., fontsize=12)

     print 'G'
     
     ax2.legend(loc=1, borderaxespad=0., fontsize=12)

     print 'H'
     
     ax2.set_yscale('log')

     print 'I'
     
     ax1.set_ylabel("# Packets (unit)", fontsize=18)

     print 'J'
     
     ax1.set_xlabel("Time (seconds)", fontsize=18)

     print 'K'

     ax2.set_ylabel("Throughput (bytes/sec)", fontsize=18)

     print 'L'

     plt.show() 

def apply_experiment(car,client,switch):
    
    #time.sleep(2)

    CLI(gnet)
    print "Applying first phase"

    ################################################################################ 
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration 
    #           at the beginning of the experiment.
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    
    #
    #               ***************** Insert code below *********************  
    #################################################################################

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl del-flows rsu1')
    os.system('ovs-ofctl del-flows eNodeB2')

    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route add 200.0.10.100 via 200.0.10.150')

    timeout = time.time() + timeTask
    currentTime = time.time()
    i = 1
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_pkt)
            switch.cmd('ifconfig switch-eth4 | grep \"TX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_pkt)
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_throughput)
            switch.cmd('ifconfig switch-eth4 | grep \"bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_throughput)
            i += 0.5

    #os.system('xterm car0')
    #car[0].cmd('iperf -s -u -i -1')
    

    print "Moving nodes"
    car[0].moveNodeTo('150,100,0')
    car[1].moveNodeTo('120,100,0')
    car[2].moveNodeTo('90,100,0')
    car[3].moveNodeTo('70,100,0')

    
    CLI(gnet)
    #time.sleep(2)
    print "Applying second phase"
 
    ################################################################################ 
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration 
    #           you have added before.
    #           Remember that now the car connects to RSU1 and eNodeB2
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below ********************* 
    #################################################################################

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl del-flows eNodeB1')

    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')
    
    timeout = time.time() + timeTask
    currentTime = time.time()
    i = 1
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:

            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_pkt)
            switch.cmd('ifconfig switch-eth4 | grep \"TX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_pkt)
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_throughput)
            switch.cmd('ifconfig switch-eth4 | grep \"bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_throughput)
            i += 0.5

    
    print "Moving nodes"
    car[0].moveNodeTo('190,100,0')
    car[1].moveNodeTo('150,100,0')
    car[2].moveNodeTo('120,100,0')
    car[3].moveNodeTo('90,100,0')

    
    #time.sleep(2)
    print "Applying third phase"
    
    ################################################################################ 
    #   1) Add the flow rules below and routing commands if needed
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below ********************* 
    #################################################################################

    os.system('ovs-ofctl del-flows switch')
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    os.system('ovs-ofctl del-flows rsu1')
    os.system('ovs-ofctl del-flows eNodeB1')

    timeout = time.time() + timeTask
    currentTime = time.time()
    i = 1
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_pkt)
            switch.cmd('ifconfig switch-eth4 | grep \"TX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_pkt)
            car[0].cmd('ifconfig bond0 | grep \"bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % c0_throughput)
            switch.cmd('ifconfig switch-eth4 | grep \"bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % switch_throughput)
            i += 0.5



def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    stas = []
    for x in range(0, 4):
        car.append(x)
        stas.append(x)
    for x in range(0, 4):
        car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1), \
        mac='00:00:00:00:00:0%s' % x, mode='b')

    
    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.vehiclesSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.vehiclesSTA:
        i = 1
        j = 1
        for v2 in net.vehiclesSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    client.cmd('ifconfig client-eth0 200.0.10.2')

    car[0].cmd('ifconfig car0-wlan0 200.0.10.150')
    car[0].cmd('ifconfig car0-wlan1 200.0.10.100')

    client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
    client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

    #net.vehiclesSTA[0].cmd('ip route add 200.0.10.100 via 10.0.0.1')
    net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.1')

    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.150')
    car[0].cmd('ip route add 200.0.10.100 via 192.168.1.2')
    #car[0].cmd('ip route add 200.0.10.2 via 200.0.10.100')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Uncomment and modify the two commands below to stream video using VLC 
    car[0].cmdPrint("vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    client.cmdPrint("vlc rtp://@200.0.10.2:5004 &")

    car[0].moveNodeTo('95,100,0')
    car[1].moveNodeTo('80,100,0')
    car[2].moveNodeTo('65,100,0')
    car[3].moveNodeTo('50,100,0')

    os.system('ovs-ofctl del-flows switch')

    time.sleep(3)

    apply_experiment(car,client,switch)

    # Uncomment the line below to generate the graph that you implemented
    graphic()

    # kills all the xterms that have been opened
    os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
