from algorithms.vectors import DistanceVector
import copy


def get_edge(r1, r2):
    return str((min(r1, r2), max(r1, r2)))


def vertexes_to_list(vertexes):
    result = {}
    for r in vertexes:
        result[r] = list(vertexes[r])
    return result


def list_to_vertexes(vertexes):
    result = {}
    for r in vertexes:
        result[r] = set(vertexes[r])
    return result


class GraphVector(DistanceVector):

    def __init__(self, router_id):
        super().__init__(router_id)
        self.vertexes = {router_id: set()}
        self.edges = {}
        self.paths = {router_id: None}
        self.changed = False

    def remove_link(self, link, time):
        edge = get_edge(self.router_id, link.dst)
        self.edges[edge] = (time, False)
        self.vertexes[self.router_id].add(link.dst)
        self.vertexes[link.dst].add(self.router_id)
        self.changed = True

    def add_link(self, link, time):
        edge = get_edge(self.router_id, link.dst)
        self.edges[edge] = (time, True)
        self.vertexes[self.router_id].add(link.dst)
        if link.dst not in self.vertexes:
            self.vertexes[link.dst] = set()
        self.vertexes[link.dst].add(self.router_id)
        self.changed = True

    def _concat_vertexes(self, vertexes):
        change = False
        for r in vertexes:
            if r not in self.vertexes:
                self.vertexes[r] = vertexes[r]
                change = True
            for n in vertexes[r]:
                if n not in self.vertexes[r]:
                    change = True
                    self.vertexes[r].add(n)
        return change

    def _concat_edges(self, edges):
        change = False
        for e in edges:
            if e not in self.edges:
                self.edges[e] = edges[e]
                change = True
            elif self.edges[e][0] < edges[e][0]:
                self.edges[e] = edges[e]
                change = True
        return change

    def handle_vector(self, link, vector):
        change = False
        vertexes, edges = vector
        vertexes = list_to_vertexes(vertexes)
        change = self._concat_vertexes(vertexes) or change
        change = self._concat_edges(edges) or change
        self.changed = change or self.changed
        return change

    #transform set into list
    def init_paths(self, links):
        self.paths = {self.router_id: None}
        for link in links:
            self.paths[link.dst] = link

    def _add_to_paths(self, new_paths):
        for r in new_paths:
            self.paths[r] = new_paths[r]

    def calc_dist(self):
        new_paths = {}
        crr_paths = self.paths.copy()

        while len(crr_paths) > 0:
            for r in crr_paths:
                for n in self.vertexes[r]:
                    if n in self.paths or n in new_paths:
                        continue
                    edge = get_edge(r, n)
                    if self.edges[edge][1]:
                        new_paths[n] = crr_paths[r]
            self._add_to_paths(new_paths)
            crr_paths = new_paths
            new_paths = {}

    def give_link(self, router, links):
        if self.changed:
            self.changed = False
            self.init_paths(links)
            self.calc_dist()
        if router not in self.paths:
            return None
        else:
            return self.paths[router]

    def give_vector(self):
        return vertexes_to_list(self.vertexes), self.edges

#
#
# def list_union(l1, l2):
#     res = l1[:]
#     for r in l2:
#         if r not in res:
#             res.append(r)
#     return res
#
#
# def concat_times(my_t, vec_t):
#     for r in my_t:
#         if r not in vec_t:
#             vec_t[r] = my_t[r]
#     for r in vec_t:
#         if r not in my_t:
#             my_t[r] = vec_t
#
#
# def compare_times(my_t, vec_t):
#     r1, r2 = tuple(my_t.keys())
#     t1, t2 = my_t[r1], my_t[r2]
#     p1, p2 = vec_t[r1], vec_t[r2]
#
#     if t1 > p1 and t2 > p2:
#         return 1
#     elif t1 > p1 and t1 - p1 > p2 - t2:
#         return 1
#     elif t2 > p2 and t2 - p2 > p1 - t1:
#         return 1
#     elif t1 == p1 and t2 == p2:
#         return 0
#     else:
#         return -1
#
#
# def take_max(my_t, vec_t):
#     r1, r2 = tuple(my_t.keys())
#     t1, t2 = my_t[r1], my_t[r2]
#     p1, p2 = vec_t[r1], vec_t[r2]
#
#     my_t[r1] = max(t1, p1)
#     my_t[r2] = max(t2, p2)
#
#
# class GraphVector(DistanceVector):
#
#     def __init__(self, router_id):
#         super().__init__(router_id)
#         self.edges = {}
#         self.vertexes = {router_id: []}
#         self.dist = {router_id: (None, 0)}
#         self.is_changed = True
#
#     def calc_dist(self):
#         pass
#
#     def add_link(self, link, time):
#         if link.dst not in self.vertexes[self.router_id]:
#             self.vertexes[self.router_id].append(link.dst)
#         self.is_changed = True
#         edge = get_edge(self.router_id, link.dst)
#
#         if edge in self.edges:
#             self.edges[edge][0][self.router_id] = time
#             self.edges[edge][1] = True
#         else:
#             self.edges[edge] = ({self.router_id: time}, True)
#
#     def remove_link(self, link, time):
#         self.is_changed = True
#         edge = get_edge(self.router_id, link.dst)
#
#         if edge in self.edges:
#             self.edges[edge][0][self.router_id] = time
#             self.edges[edge][1] = False
#         else:
#             self.edges[edge] = ({self.router_id: time}, False)
#
#     def give_link(self, router):
#         if router in self.vertexes and router not in self.dist:
#             self.calc_dist()
#         if router in self.dist:
#             if self.dist[router] == -1:
#                 return None
#             else:
#                 return self.dist[router]
#         return None
#
#     def give_vector(self):
#         self.is_changed = False
#         return copy.deepcopy(self.vertexes), copy.deepcopy(self.edges)
#
#
#     def _concat_vertexes(self, vec_v):
#         for v in vec_v:
#             if v not in self.vertexes:
#                 self.vertexes[v] = vec_v[v]
#                 self.is_changed = True
#             elif self.vertexes[v] != vec_v[v]:
#                 self.is_changed = True
#                 self.vertexes[v] = list_union(vec_v[v], self.vertexes[v])
#
#     def _concat_edges(self, vec_edges):
#         for e in vec_edges:
#             if e not in self.edges:
#                 self.edges[e] = vec_edges[e]
#             else:
#                 my_t, vec_t = self.edges[e][0], vec_edges[e][0]
#                 concat_times(my_t, vec_t)
#                 if compare_times(my_t, vec_t) < 0:
#                     self.is_changed = True
#                     take_max(my_t, vec_t)
#                     self.edges[e] = (my_t, vec_edges[e][1])
#                 else:
#                     take_max(my_t, vec_t)
#
#     def handle_vector(self, link, vector):
#         v_vertexes, v_edges = vector
#         self._concat_vertexes(v_vertexes)
#         self._concat_edges(v_edges)
#         return self.is_changed
