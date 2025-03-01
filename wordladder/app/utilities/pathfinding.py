import networkx as nx
from queue import PriorityQueue
from collections import deque
from .word_graph import build_word_graph

def bfs(graph, start, goal):
    """Breadth-First Search (BFS) to find the shortest path."""
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path  # Found the shortest path
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                queue.append(path + [neighbor])
    
    return None  # No path found

def ucs(graph, start, goal):
    """Uniform Cost Search (UCS) to find the shortest path."""
    pq = PriorityQueue()
    pq.put((0, [start]))
    visited = set()

    while not pq.empty():
        cost, path = pq.get()
        node = path[-1]

        if node == goal:
            return path
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                pq.put((cost + 1, path + [neighbor]))  # Cost is uniform (1)

    return None

def astar(graph, start, goal):
    """A* Search Algorithm using word similarity as heuristic."""
    def heuristic(word1, word2):
        return sum(1 for a, b in zip(word1, word2) if a != b)  # Letter difference heuristic

    pq = PriorityQueue()
    pq.put((heuristic(start, goal), [start]))
    visited = set()

    while not pq.empty():
        _, path = pq.get()
        node = path[-1]

        if node == goal:
            return path
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                cost = len(path) + heuristic(neighbor, goal)
                pq.put((cost, path + [neighbor]))

    return None

def find_next_word(game_mode, start, goal, algorithm):
    """Finds the next word in the shortest path using the selected algorithm."""
    graph = build_word_graph(game_mode)
    
    if algorithm == "BFS":
        path = bfs(graph, start, goal)
    elif algorithm == "UCS":
        path = ucs(graph, start, goal)
    elif algorithm == "A*":
        path = astar(graph, start, goal)
    else:
        return None  # Invalid algorithm
    
    if path and len(path) > 1:
        return path[1]  # Return the next word in the path
    return None  # No valid next step found
