from enum import Enum


class City(Enum):
    WV = "WV",
    NV = "NV",
    VA = "VA",
    RI = "RI",
    BU = "BU",
    NW = "NW",
    SU = "SU",
    DE = "DE",
    LA = "LA",
    AB = "AB",
    MI = "MI",
    CH = "CH",
    HO = "HO"



adjacency_graph = {
    City.WV: {City.NV: 6.6, City.VA: 8.2},
    City.NV: {City.WV: 6.6, City.VA: 10.5},
    City.VA: {City.WV: 8.3, City.NV: 20.5, City.RI: 16.2, City.BU: 14.0},
    City.RI: {City.VA: 16.2, City.DE: 24.8, City.BU: 21.3, City.NW: 21.6},
    City.BU: {City.VA: 14.0, City.RI: 21.3, City.NW: 7.4, City.SU: 13.9, City.MI: 54.9},
    City.NW: {City.RI: 21.6, City.BU: 7.4, City.SU: 6.4},
    City.SU: {City.NW: 6.4, City.DE: 23.5, City.LA: 24.3, City.BU: 13.9},
    City.DE: {City.RI: 24.8, City.SU: 23.5, City.LA: 36.5},
    City.LA: {City.DE: 36.5, City.SU: 24.3, City.AB: 31.9},
    City.AB: {City.LA: 31.9, City.MI: 12.3, City.CH: 34.2},
    City.MI: {City.BU: 54.9, City.AB: 12.3},
    City.CH: {City.AB: 34.2, City.HO: 52.5},
    City.HO: {City.CH: 52.5}
}




def graph_to_tuple(graph: dict[City, dict[City, float]]) -> dict[City, list[tuple[City, float]]]:
    """ Convert the graph from dict-based adjency dict to tuple-based adjacency dict"""
    tuple_based: dict[City, list[tuple[City, float]]] = {}
    for key in graph:
        tuple_based[key] = []
        for value in graph[key]:
            tuple_based[key].append((value, graph[key][value]))

    return tuple_based


# it will just take the min distance between the city halls and remove a random value of 5 to 10
# do i need to do this for each city out there??
def naive_heuristics(city: City):
    pass

print(graph_to_tuple(graph=adjacency_graph).get(City.BU))