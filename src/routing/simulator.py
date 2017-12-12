#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import logging
import uuid

from routing.router import *

from routing.algorithms import RoutingAlgorithm


class Simulator:
    """Simulator sandbox for routing algorithm experiments"""
    class SimPacket(Packet):
        def __init__(self, src, dst, start_time):
            super().__init__(src, dst)
            self.start_time = start_time
            self.stop_time = None

    class SimLink(Link):
        def __init__(self, dst):
            super().__init__(dst)
            self.packet = None

        def forward_packet(self, packet):
            if self.packet is not None:
                raise RuntimeError
            if not isinstance(packet, Packet):
                raise ValueError
            self.packet = packet

    class SimRouter(Router):
        def __init__(self, algorithm_class, id=None):
            if not issubclass(algorithm_class, RoutingAlgorithm):
                raise ValueError
            super().__init__()
            self._id = id or uuid.uuid4()
            self._links = dict()
            self.store = dict()
            self.packets = dict()
            self.algorithm = algorithm_class(self)

        @property
        def id(self):
            return self._id
        @property
        def links(self):
            return list(self._links.values())
        @property
        def stored_packets(self):
            return list(self.store.values())

        def drop_packet(self, packet):
            if not isinstance(packet, Packet):
                raise ValueError
            if packet.id in self.store:
                del self.store[packet.id]
            if packet.id in self.packets:
                del self.packets[packet.id]
            logging.info("Droped packet [{}] {} -> {}".format(packet.id, packet.src, packet.dst))

        def store_packet(self, packet):
            if not isinstance(packet, Packet):
                raise ValueError
            self.store[packet.id] = packet
            if packet.id in self.packets:
                del self.packets[packet.id]

        def forward_packet(self, link, packet):
            if not isinstance(link, Simulator.SimLink):
                raise ValueError
            if not isinstance(packet, Packet):
                raise ValueError
            if link not in self.links:
                raise ValueError
            if isinstance(packet, Simulator.SimPacket):
                if packet.id not in self.store and packet.id not in self.packets:
                    raise ValueError
            link.forward_packet(packet)
            if packet.id in self.store:
                del self.store[packet.id]
            if packet.id in self.packets:
                del self.packets[packet.id]

    def __init__(self):
        self.routers = dict()
        self.links = set()
        self.time = 0
        self.routable_packets = 0
        self.routed_packets = list()

    @property
    def stats(self):
        response = dict()
        response['packets'] = self.routable_packets
        if self.routable_packets > 0:
            response['delivery_rate'] = len(self.routed_packets) / self.routable_packets
        response['routed'] = len(self.routed_packets)
        if len(self.routed_packets) > 0:
            response['avg_time'] = sum( [p.stop_time - p.start_time for p in self.routed_packets] ) / len(self.routed_packets)
        return response

    def add_router(self, algorithm_class, id=None):
        if id in self.routers:
            raise ValueError
        r = Simulator.SimRouter(algorithm_class, id)
        self.routers[r.id] = r
        return r

    def add_link(self, r1, r2):
        if isinstance(r1, Router):
            r1 = r1.id
        if isinstance(r2, Router):
            r2 = r2.id
        if r1 not in self.routers or r2 not in self.routers:
            raise ValueError
        r1, r2 = (min(r1,r2), max(r1,r2))
        if r1 != r2 and (r1,r2) not in self.links:
            self.links.add( (r1,r2) )
            self.routers[r1]._links[r2] = Simulator.SimLink(r2)
            self.routers[r1].algorithm.add_link(self.routers[r1]._links[r2])
            self.routers[r2]._links[r1] = Simulator.SimLink(r1)
            self.routers[r2].algorithm.add_link(self.routers[r2]._links[r1])

    def del_link(self, r1, r2):
        if isinstance(r1, Router):
            r1 = r1.id
        if isinstance(r2, Router):
            r2 = r2.id
        if r1 not in self.routers or r2 not in self.routers:
            raise ValueError
        r1, r2 = (min(r1,r2), max(r1,r2))
        if (r1,r2) in self.links:
            self.links.remove( (r1,r2) )
            self.routers[r1].algorithm.del_link(self.routers[r1]._links[r2])
            del self.routers[r1]._links[r2]
            self.routers[r2].algorithm.del_link(self.routers[r2]._links[r1])
            del self.routers[r2]._links[r1]

    def add_packet(self, r1, r2):
        if isinstance(r1, Router):
            r1 = r1.id
        if isinstance(r2, Router):
            r2 = r2.id
        if r1 in self.routers:
            if r2 in self.routers:
                self.routable_packets += 1
            router = self.routers[r1]
            packet = Simulator.SimPacket(r1, r2, self.time)
            router.packets[packet.id] = (None, packet)
            return packet

    def route(self):
        self.time += 1
        for id, router in self.routers.items():
            router.algorithm(list(router.packets.values()))
            for src, packet in router.packets.values():
                if packet.dst != router.id:
                    logging.warning("Silently droped packet [{}] {} -> {} at {}".format(packet.id, packet.src, packet.dst, router.id))
            router.packets = dict()
        for id, router in self.routers.items():
            for link in router.links:
                if link.packet is not None:
                    packet = link.packet
                    link.packet = None
                    if link.dst in self.routers:
                        if isinstance(packet, Simulator.SimPacket) and packet.dst == link.dst:
                            packet.stop_time = self.time
                            self.routed_packets.append(packet)
                            logging.info("Routed packet [{}] {} -> {} in {} steps".format(packet.id, packet.src, packet.dst, packet.stop_time - packet.start_time))
                        else:
                            # logging.debug("Forwarded packet [{}] {} -> {} to {}".format(packet.id, packet.src, packet.dst, link.dst))
                            self.routers[link.dst].packets[packet.id] = (self.routers[link.dst]._links[router.id], packet)
