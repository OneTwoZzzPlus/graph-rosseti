class Node:
    def __init__(self, value: int, x=0, y=0, mass=10):
        self.value = value
        self.edges = set()
        self.x = x
        self.y = y
        self.mass = mass

    def nextEdges(self, pre_edge, brk_edge=None):
        return [edge for edge in self.edges if edge != pre_edge and edge != brk_edge]


class Edge:
    def __init__(self, node1: Node, node2: Node, edge_arg):
        self.node1 = node1
        self.node2 = node2
        lea = len(edge_arg)
        self.rk1 = edge_arg[0] if lea >= 1 else False
        self.rk2 = edge_arg[1] if lea >= 2 else False
        self.close1 = edge_arg[2] if lea >= 3 else False
        self.close2 = edge_arg[3] if lea >= 4 else False
        self.length = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
        self.y_len = self.length * 0.11

    def nextNode(self, node: Node):
        return self.node2 if node == self.node1 else self.node1

    def longRk(self, node: Node):
        return self.rk2 if node == self.node1 else self.rk1

    def thisRk(self, node: Node):
        return self.rk1 if node == self.node1 else self.rk2

    def longClose(self, node: Node):
        return self.close2 if node == self.node1 else self.close1

    def thisClose(self, node: Node):
        return self.close1 if node == self.node1 else self.close2


class Graph:
    def __init__(self, graph_data):
        self.graph = {}
        self.edges = set()
        for row in graph_data:
            node1 = self.addOrGetNode(row[0])
            node2 = self.addOrGetNode(row[1])
            edge = Edge(node1, node2, row[2:])
            node1.edges.add(edge)
            node2.edges.add(edge)
            self.edges.add(edge)
        self.end_nodes = [self.graph[1], self.graph[2]]

    def addOrGetNode(self, value):
        if value not in self.graph:
            self.graph[value] = Node(value)
        return self.graph[value]

    def getNode(self, value):
        return self.graph[value]

    def find_paths(self, node, path, paths, pre_edge, brk_edge=None, rk_ch=True, close_ch=True):
        if pre_edge.longRk(node) and rk_ch and pre_edge.longClose(node) and close_ch:
            path = path + ['RC']
        elif pre_edge.longRk(node) and rk_ch:
            path = path + ['R']
        elif pre_edge.longClose(node) and close_ch:
            path = path + ['C']

        if pre_edge == brk_edge:
            path = path + ['B']

        if pre_edge.thisRk(node) and rk_ch and pre_edge.thisClose(node) and close_ch:
            path = path + ['RC']
        elif pre_edge.thisRk(node) and rk_ch:
            path = path + ['R']
        elif pre_edge.thisClose(node) and close_ch:
            path = path + ['C']

        path = path + [node.value]

        next_edges = node.nextEdges(pre_edge)
        if node in self.end_nodes or len(next_edges) == 0:
            paths.append(path)
            return paths

        for edge in next_edges:
            if edge.nextNode(node).value not in path:
                paths = self.find_paths(edge.nextNode(node), path, paths, edge, brk_edge)
        return paths

    def find_paths_for_edge(self, edge: Edge):
        paths = self.find_paths(edge.node1, [], [], edge, None, edge.rk1, edge.close1)
        paths = self.find_paths(edge.node2, [], paths, edge, None, edge.rk2, edge.close2)
        return paths

    def get_broken_nodes(self, edge: Edge):
        paths = self.find_paths_for_edge(edge)
        broken_nodes = set()
        for path in paths:
            for n in path:
                if n in [1, 2, 'R', 'C'] and path[-1] in [1, 2]:
                    break
                if n not in ['R', 'C']:
                    broken_nodes.add(n)
        return broken_nodes

    def find_paths_for_node(self, node: Node, brk_edge=None):
        paths = []
        if node not in self.end_nodes:
            for edge in node.edges:
                paths.extend(self.find_paths(edge.nextNode(node), [node.value], [], edge, brk_edge))
        return paths

    def check_broken_node(self, node, brk_edge):
        paths = self.find_paths_for_node(node, brk_edge)
        if all('B' in path or path[-1] not in [1, 2] for path in paths):
            return 7
        return -1

    def main(self):
        brk_edge = list(self.getNode(8).edges)[0]
        print('edge', brk_edge.node1.value, brk_edge.node2.value)
        print(paths_edge := self.find_paths_for_edge(brk_edge))
        print(broken_nodes := self.get_broken_nodes(brk_edge))
        print()
        for brk_node_value in broken_nodes:
            brk_node = self.getNode(brk_node_value)
            t = self.check_broken_node(brk_node, brk_edge)
            print('brk node', brk_node.value, 'time', t)
            print(self.find_paths_for_node(brk_node, brk_edge))



print('OneTwoZzz')
data = [[1, 2, 1, 1, 1, 0], [2, 3, 1, 0], [3, 4], [4, 5, 1, 0, 1, 0], [5, 6],
        [6, 1, 0, 1], [3, 7], [4, 7], [5, 8, 1, 0], [8, 9], [9, 10, 1, 0], [10, 11]]
graph = Graph(data)
graph.main()
