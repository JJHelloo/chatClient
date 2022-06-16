#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.term import makeTerm

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)
 
    info( '*** Add switches\n')
    #move switches ahead
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    
     
    r3 = net.addHost('r3', cls=Node, ip='10.0.4.9/24', defaultRoute='via 192.168.1.1')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    r4 = net.addHost('r4', cls=Node, ip='192.168.1.1/24', defaultRoute='via 192.168.2.2')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r5 = net.addHost('r5', cls=Node, ip='10.0.5.9/24', defaultRoute='via 192.168.2.1')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #add link
    #change add link values

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.4.1/24', defaultRoute='via 192.168.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.4.2/24', defaultRoute='via 192.168.1.1') 
    h4 = net.addHost('h4', cls=Host, ip='10.0.5.2/24', defaultRoute='via 10.0.5.9')
    h3 = net.addHost('h3', cls=Host, ip='10.0.5.1/24', defaultRoute='via 10.0.5.9')

    info( '*** Add links\n')
    net.addLink(r5, s2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(r3, s1)
    net.addLink(s1, h2)
    net.addLink(s1, h1)
    net.addLink( r3, r4, intfName1='r3-eth1', params1={ 'ip' : '192.168.1.2/30' }, intfName2='r4-eth0', params2={ 'ip' : '192.168.1.1/30' }, )
    #net.addLink( r3, r4, intfName1='r3', params1={ 'ip' : '192.168.2.2/30' }, intfName2='r4-eth0', params2={ 'ip' : '192.168.2.5/30' }, )
    net.addLink( r5, r4, intfName1='r5-eth1', params1={ 'ip' : '192.168.2.2/30' }, intfName2='r4-eth1', params2={ 'ip' : '192.168.2.1/30' }, )
    #net.addLink( r5, r4, intfName1='r5', params1={ 'ip' : '192.168.9.2/30' }, intfName2='r4-eth1', params2={ 'ip' : '192.168.9.5/30' }, )

    info( '*** Starting network\n')
    net.build()
    
    
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    info('r3 \n')
    info( net[ 'r3' ].cmd( 'route' ) )
    info('r4 \n')
    info( net[ 'r4' ].cmd( 'route' ) )
    info('r5 \n')
    info( net[ 'r5' ].cmd( 'route' ) )
    CLI(net)
    net.stop()

#add Kernel IP Routing Table / not working
def run():
    "Test linux router"
    topo = myNetwork()
    net = Mininet( topo=topo, waitConnected=True )  # controller is used by s1-s3
    net.start()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
    

