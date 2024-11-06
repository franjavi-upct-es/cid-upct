from mininet.topo import Topo
from mininet.node import OVSBridge,Node


class LinuxRouter(Node):
    def config(self,**params):
        super(LinuxRouter,self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter,self).config(**params)


class mitopo(Topo):
    
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        s1 = self.addSwitch('s1',switch='ovsbr')
        s2 = self.addSwitch('s2',switch='ovsbr')
        s3 = self.addSwitch('s3',switch='ovsbr')
        s4 = self.addSwitch('s4',switch='ovsbr')
        s5 = self.addSwitch('s5',switch='ovsbr')

        r1 = self.addNode('r1',cls=LinuxRouter,ip=None)
        r2 = self.addNode('r2',cls=LinuxRouter,ip=None)
        r3 = self.addNode('r3',cls=LinuxRouter,ip=None)

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        self.addLink(r1, s1)
        self.addLink(r1, s2)
        self.addLink(r1, s5) 
        self.addLink(r2, s3)
        self.addLink(r2, s5)
        self.addLink(r3, s5)
        self.addLink(r3, s4)

topos={'mitopo':(lambda: mitopo())}
