import heapq
from strassen import strassen  

def dijkstra(graph, start, target):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph}
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

        if current_vertex == target:
            return distances[target], predecessors

    return float('infinity'), predecessors

def reconstruct_path(predecessors, start, target):
    path = []
    current = target
    while current != start:
        path.append(current)
        current = predecessors[current]
        if current is None: 
            return []
    path.append(start)
    path.reverse()
    return path

def create_graph(strassen):
    graph = {}
    movements = {}
    for start, end, movement_type, cost in strassen:
        if start not in graph:
            graph[start] = {}
        graph[start][end] = cost
        movements[(start, end)] = movement_type
    return graph, movements




