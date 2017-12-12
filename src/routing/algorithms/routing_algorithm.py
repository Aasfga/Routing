from routing.router import *


class RoutingAlgorithm:
    """Abstract routing algorithm class"""
    def __init__(self, router):
        if not isinstance(router, Router):
            raise ValueError
        self.router = router
    def __call__(self, packets):
        if not isinstance(packets, list):
            raise ValueError
        for src, packet in packets:
            if not isinstance(packet, Packet):
                raise ValueError
            if src is not None and not isinstance(src, Link):
                raise ValueError
        self.route(packets)

    def add_link(self, link):
        """Called when new link is added to router"""
        raise NotImplementedError

    def del_link(self, link):
        """Called when a link is removed from router"""
        raise NotImplementedError

    def route(self, packets):
        """Called in every round of routing algorithm"""
        raise NotImplementedError
