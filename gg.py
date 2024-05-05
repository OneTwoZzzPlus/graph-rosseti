class Node:
    def __init__(self, value):
        self.value = value
        self.edges = set()
        self.parents = dict()


class Edge:
    def __init__(self, adjacent_node, weight):
        self.adjacent_node = adjacent_node
        self.weight = weight


def addOrGetNode(r_graph, value):
    if value == -1:
        return None
    if value not in r_graph:
        r_graph[value] = Node(value)
    return r_graph[value]


def getNode(r_graph, value):
    if value in r_graph and value != -1:
        return r_graph[value]
    return None


def createGraph(data):
    r_graph = {}
    for row in data:
        node = addOrGetNode(r_graph, row[0])
        adjacent_node = addOrGetNode(r_graph, row[1])
        if adjacent_node is None:
            continue

        edge = Edge(adjacent_node, row[2])
        node.edges.add(edge)
        adjacent_node.parents[node] = edge
    return r_graph


def DFS(node, passed):
    print(node.value)
    passed.add(node)
    for edge in node.edges:
        if edge.adjacent_node not in passed:
            return DFS(edge.adjacent_node, passed)
        else:
            return passed


def DFSWrap(r_graph):
    passed = set()
    for node in r_graph.values():
        if node not in passed:
            passed = DFS(node, passed)


def getPath(start: Node, end: Node, passed, path):
    passed.add(start)
    if start == end:
        path.append(start)
        return True
    for edge in start.edges:
        if edge.adjacent_node not in passed:
            if getPath(edge.adjacent_node, end, passed, path):
                path.append(start)
                return True


graph_data = [
    [7, 6, 1],
    [7, 2, 1],
    [7, 5, 1],
    [6, 4, 1],
    [2, 1, 1],
    [5, 9, 1],
    [8, 10, 1]
]

graph = createGraph(graph_data)

print(getPath(getNode(graph, 7), getNode(graph, 8), set(), []))
