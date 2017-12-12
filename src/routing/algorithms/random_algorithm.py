import random

from routing.algorithms import RoutingAlgorithm


class RandomRouter(RoutingAlgorithm):
    """Routing algorithm that forwards packets in random directions"""

    def del_link(self, link):
        pass

    def add_link(self, link):
        pass

    def route(self, packets):
        for src, packet in packets:
            self.router.store_packet(packet)
        packets = self.router.stored_packets
        random.shuffle(packets)
        links = self.router.links
        random.shuffle(links)
        for link in links:
            if len(packets) > 0:
                self.router.forward_packet(link, packets[-1])
                packets = packets[0:-1]