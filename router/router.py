class Link:
    """Abstract inter-router link class"""
    def __init__(self, dst):
        self._dst = dst
    @property
    def dst(self):
        """Returns address of the destination router"""
        return self._dst

    def __hash__(self):
        return hash(self._dst)

class Router:
    """Abstract router class"""
    @property
    def id(self):
        """Returns address of the router"""
        pass
    @property
    def links(self):
        """Returns a list of links available at the router"""
        pass
    @property
    def stored_packets(self):
        """Returns a list of packets stored in the memory of the router"""
        pass
    def drop_packet(self, packet):
        """Drops a packet"""
        pass
    def store_packet(self, packet):
        """Stores a packet in the memory of the router"""
        pass
    def forward_packet(self, link, packet):
        """Forwards a packet over a link"""
        pass

    def __hash__(self):
        return hash(id)

