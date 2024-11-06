from mininet.topo import Topo

class mitopo (Topo):
    
    def build(self):

        s1=self.addSwitch('s1',switch='ovsbr')

        h1=self.addHost('h1')
        h2=self.addHost('h2')
        h3=self.addHost('h3')
        h4=self.addHost('h4')

        self.addLink('h1','s1')
        self.addLink('h2','s1')
        self.addLink('h3','s1')
        self.addLink('h4','s1')

topos={'mitopo':(lambda: mitopo())}
