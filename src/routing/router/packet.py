import json
import uuid


class Packet:
    """Abstract packet class"""
    def __init__(self, src, dst):
        self._id  = uuid.uuid4()
        self._src = src
        self._dst = dst
    @property
    def id(self):
        """Returns globally unique id of the packet"""
        return self._id
    @property
    def src(self):
        """Returns address of the source router"""
        return self._src
    @property
    def dst(self):
        """Returns address of the destination router"""
        return self._dst

class MetaPacket(Packet):
    """Packet for routing algorithm communication"""
    def __init__(self, src, dst, payload):
        super().__init__(src, dst)
        self._payload = json.dumps(payload)
    @property
    def payload(self):
        return json.loads(self._payload)