from BuildGraph import adjacency_graph, City
from Dikstra import Dikstra, Node as DikstraNode

# this can be switched to GrassFire node for grassfire algorithm
Node = DikstraNode

start_city = City.VA
end_city = City.AB

target = [start_city, end_city]

heuristics = {}


# We need to create unique nodes for each city
# WE map City: Node(City)
# For instnace: City.VA: Node(City.VA)
def city_to_node(city: City) -> dict[City, Node]:
    """ Convert to {City: Node(City)}"""
    nodes = {}
    for key in city:
        nodes[key] = Node(key)

    return nodes

city_nodes = city_to_node(City)


## We need to create node based tuples of the neigbours
## It will be {Node(City): [(Node(City), value), (Node(City), value)]}
def graph_to_nodes_tuple(graph: dict[City, dict[City, float]]) -> dict[Node, list[tuple[Node, float]]]:
    tuple_based: dict[Node, list[tuple[Node, float]]] = {}
    for key in graph:
        tuple_based[city_nodes.get(key)] = []
        for value in graph.get(key):
            tuple_based[city_nodes.get(key)].append((city_nodes.get(value), graph[key][value]))

    return tuple_based



node_graph = graph_to_nodes_tuple(graph=adjacency_graph)

for key in city_nodes:
    node = city_nodes.get(key)
    node.set_neighbors(*node_graph.get(node))


print(city_nodes.get(City.HO))

start_city = city_nodes.get(City.VA)
end_city = city_nodes.get(City.AB)

algorithm = Dikstra(start=start_city)
algorithm.run()

path = algorithm.reiterate(goal=end_city)

for node in path:
    print(node.id)