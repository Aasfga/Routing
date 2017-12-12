from routing.algorithms.vectors import DistanceVector


class SimpleVector(DistanceVector):
    def __init__(self, router_id):
        super().__init__(router_id)
        self.paths = {}
        self.changed = False

    def add_link(self, link, time):
        pass

    def remove_link(self, link, time):
        pass

    def give_vector(self):
        vector = {}
        for r in self.paths:
            vector[r] = self.paths[r][1]
        vector[self.router_id] = 0
        return vector

    def handle_vector(self, link, vector):
        change = False
        for r in vector:
            if r in self.paths:
                _, dist = self.paths[r]
                if dist > vector[r] + 1:
                    change = True
                    self.paths[r] = (link, vector[r] + 1)
            else:
                self.paths[r] = (link, vector[r] + 1)
                change = True
        return change

    def give_link(self, router, links):
        if router in self.paths:
            return self.paths[router][0]
        else:
            return None
