from BuildGraph import adjacency_graph, City, db
from Dikstra import Dikstra, Node as DikstraNode
from AStar import AStar, Node as AStarNode
from GrassFire import GrassFire, Node as GrassFireNode

# this can be switched to GrassFire node for grassfire algorithm


algorithm_type = "GrassFire"


if algorithm_type == "Dikstra":
    Node = DikstraNode
elif algorithm_type == "GrassFire":
    Node = GrassFireNode
elif algorithm_type == "AStar":
    Node = AStarNode
else:
    raise ValueError("Invalid algorithm type")

start_city = City.VA
end_city = City.AB

target = [start_city, end_city]


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
    # for grass fire, just add the node.id only
    if algorithm_type == "GrassFire":
        ids = []
        for neighbor in node_graph.get(node):
            ids.append(Node(neighbor[0].id))
        node.set_neighbors(*ids)
    else:
        node.set_neighbors(*node_graph.get(node))


start_city = city_nodes.get(City.VA)
end_city = city_nodes.get(City.AB)

## The heuristic node.h will be the goal city and the current node city, change all of them
for node in city_nodes:
    # db.get_distance(node, end_city) where node and end_city are City

    heuristic = db.get_distance(node, end_city.id)
    # change the heuristics of all the nodes
    node.h = heuristic



if algorithm_type == "AStar":
    algorithm = AStar(start=start_city, goal=end_city)
    algorithm.run()

    path = algorithm.reiterate()
elif algorithm_type == "Dikstra":
    algorithm = Dikstra(start=start_city)
    algorithm.run()

    path = algorithm.reiterate(goal=end_city)
elif algorithm_type == "GrassFire":
    algorithm = GrassFire(start=start_city, end=end_city)
    algorithm.run()

    path = algorithm.reiterate()
else:
    raise ValueError("Invalid algorithm type")



print("FROM: ", start_city.id)
print("TO: ", end_city.id)
print("PATH: ")

 # print as City  ---(value)--> City --- (value) --> City, whre avlue is the cost

for i in range(len(path)-1):
    print(f"{path[i].id} --- {db.get_distance(path[i].id, path[i+1].id)} km ---> ", end="")

print(path[-1].id)
