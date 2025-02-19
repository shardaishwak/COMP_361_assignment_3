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


class DistanceBuilder:
    def __init__(self):
        self.distance_map: dict[tuple[City, City], float] = {}

    def generate_cities_key(self, city1: City, city2: City)-> tuple[City, City]:
        return  (city1, city2) if city1.value < city2.value else (city2, city1)

    def add_distance(self, city1: City, city2: City, distance: float):
        if (city1 == city2):
            raise Exception("city1 and city2 cannot be same cities.")
        key = self.generate_cities_key(city1, city2)
        self.distance_map[key] = distance

    def get_distance(self, city1: City, city2: City)-> float:
        return self.distance_map.get(self.generate_cities_key(city1, city2))


db = DistanceBuilder()
db.add_distance(City.VA, City.AB, 20)


## Build the distance between all the citites for heuristics
db.add_distance(City.WV, City.NV, 6.6)
db.add_distance(City.WV, City.VA, 8.2)
db.add_distance(City.WV, City.RI, 24.1)
db.add_distance(City.WV, City.BU, 23.2)
db.add_distance(City.WV, City.NW, 35.1)
db.add_distance(City.WV, City.SU, 43.7)
db.add_distance(City.WV, City.DE, 33.2)
db.add_distance(City.WV, City.LA, 59.5)
db.add_distance(City.WV, City.AB, 81.3)
db.add_distance(City.WV, City.MI, 77.1)
db.add_distance(City.WV, City.CH, 112)
db.add_distance(City.WV, City.HO, 160)

db.add_distance(City.NV, City.VA, 10.5)
db.add_distance(City.NV, City.RI, 30.1)
db.add_distance(City.NV, City.BU, 15.6)
db.add_distance(City.NV, City.NW, 27.4)
db.add_distance(City.NV, City.SU, 36)
db.add_distance(City.NV, City.DE, 35.2)
db.add_distance(City.NV, City.LA, 52)
db.add_distance(City.NV, City.AB, 73)
db.add_distance(City.NV, City.MI, 69)
db.add_distance(City.NV, City.CH, 104)
db.add_distance(City.NV, City.HO, 154)

db.add_distance(City.VA, City.RI, 16.2)
db.add_distance(City.VA, City.BU, 14)
db.add_distance(City.VA, City.NW, 20.5)
db.add_distance(City.VA, City.SU, 34)
db.add_distance(City.VA, City.DE, 25)
db.add_distance(City.VA, City.LA, 52.5)
db.add_distance(City.VA, City.AB, 73.9)
db.add_distance(City.VA, City.MI, 69.7)
db.add_distance(City.VA, City.CH, 104)
db.add_distance(City.VA, City.HO, 154)

db.add_distance(City.RI, City.BU, 21.3)
db.add_distance(City.RI, City.NW, 21.6)
db.add_distance(City.RI, City.SU, 30)
db.add_distance(City.RI, City.DE, 14.2)
db.add_distance(City.RI, City.LA, 44.7)
db.add_distance(City.RI, City.AB, 73.9)
db.add_distance(City.RI, City.MI, 72.7)
db.add_distance(City.RI, City.CH, 110)
db.add_distance(City.RI, City.HO, 160)

db.add_distance(City.BU, City.NW, 7.4)
db.add_distance(City.BU, City.SU, 21.5)
db.add_distance(City.BU, City.DE, 28.2)
db.add_distance(City.BU, City.LA, 37.4)
db.add_distance(City.BU, City.AB, 59.1)
db.add_distance(City.BU, City.MI, 54.9)
db.add_distance(City.BU, City.CH, 90)
db.add_distance(City.BU, City.HO, 140)

db.add_distance(City.NW, City.SU, 17.4)
db.add_distance(City.NW, City.DE, 28.5)
db.add_distance(City.NW, City.LA, 30.5)
db.add_distance(City.NW, City.AB, 54.3)
db.add_distance(City.NW, City.MI, 50.5)
db.add_distance(City.NW, City.CH, 65.3)
db.add_distance(City.NW, City.HO, 135)

db.add_distance(City.SU, City.DE, 25.5)
db.add_distance(City.SU, City.LA, 24.3)
db.add_distance(City.SU, City.AB, 45.3)
db.add_distance(City.SU, City.MI, 47.5)
db.add_distance(City.SU, City.CH, 76.3)
db.add_distance(City.SU, City.HO, 126)

db.add_distance(City.DE, City.LA, 32.5)
db.add_distance(City.DE, City.AB, 58.5)
db.add_distance(City.DE, City.MI, 68.5)
db.add_distance(City.DE, City.CH, 89.3)
db.add_distance(City.DE, City.HO, 150)

db.add_distance(City.LA, City.AB, 31.9)
db.add_distance(City.LA, City.MI, 42.5)
db.add_distance(City.LA, City.CH, 62.3)
db.add_distance(City.LA, City.HO, 112)

db.add_distance(City.AB, City.MI, 12.3)
db.add_distance(City.AB, City.CH, 34.2)
db.add_distance(City.AB, City.HO, 84.2)

db.add_distance(City.MI, City.CH, 43.5)
db.add_distance(City.MI, City.HO, 93.3)

db.add_distance(City.CH, City.HO, 52.5)








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