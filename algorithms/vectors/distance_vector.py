class DistanceVector:

    def __init__(self, router_id):
        self.router_id = router_id

    def handle_vector(self, link, vector):
        raise NotImplementedError

    def give_vector(self):
        raise NotImplementedError

    def remove_link(self, link, time):
        raise NotImplementedError

    def add_link(self, link, time):
        raise NotImplementedError

    def give_link(self, router, links):
        raise NotImplementedError


