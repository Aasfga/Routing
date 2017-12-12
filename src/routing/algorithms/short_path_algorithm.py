from routing.algorithms.routing_algorithm import RoutingAlgorithm
from routing.router import MetaPacket

from routing.algorithms.vectors import GraphVector, DistanceVector


class ShortPathRouter(RoutingAlgorithm):
    """Distance vector type routing algorithm"""

    vector_class = GraphVector

    @staticmethod
    def set_vector(cls):
        if issubclass(cls, DistanceVector):
            ShortPathRouter.vector_class = cls
        else:
            raise ValueError

    def __init__(self, router):
        super().__init__(router)
        self.time = 0
        self.paths = self.vector_class(self.router.id)
        self.is_changed = True

    def add_link(self, link):
        self.paths.add_link(link, self.time)
        self.is_changed = True

    def del_link(self, link):
        self.paths.remove_link(link, self.time)
        self.is_changed = True

    def handle_vector(self, link, vector):
        return self.paths.handle_vector(link, vector)

    def give_vector(self):
        return self.paths.give_vector()

    def send_vector(self, used=None):
        links = self.router.links
        if used is None:
            used = {}
        for link in links:
            if link not in used:
                self.router.forward_packet(link,
                                           MetaPacket(self.router.id, link.dst, self.give_vector()))

    def route(self, packets):
        for src, packet in packets:
            if isinstance(packet, MetaPacket):
                # logging.debug('Time: {}  Router {} received vector {} from {}'.format(self.time, self.router.id, packet.payload, src.dst))
                self.is_changed = self.handle_vector(src, packet.payload) or self.is_changed
            else:
                self.router.store_packet(packet)
        if self.is_changed and self.time % 5 == 0:  # SEND my distance vector to neighbors every 5-th round
            # logging.debug('Router {} sending vector {} to neighbors'.format(self.router.id, self.give_vector()))
            self.send_vector()
            self.is_changed = False
        else:
            used = {}
            for packet in self.router.stored_packets:
                dst = packet.dst
                link = self.paths.give_link(dst, self.router.links)
                if link is not None and link not in used:
                    used[link] = True
                    self.router.forward_packet(link, packet)
            if self.is_changed:
                self.send_vector(used)
        self.time = self.time + 1
