import heapq
from collections import deque
import math

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance in kilometers between two points on the earth."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_path_cost(graph, path, weight='travel_cost'):
    if not path: return 0
    cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        edge_data = graph.get_edge_data(u, v)
        if edge_data:
            cost += edge_data.get(weight, 1)
        else:
            cost += 1
    return cost

def bfs_search(graph, start, goal):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
    
    queue = deque([[start]])
    visited = {start}
    explored_nodes = 0
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        explored_nodes += 1
        
        if node == goal:
            return {
                "path": path, 
                "explored": explored_nodes, 
                "cost": calculate_path_cost(graph, path, 'travel_cost'),
                "distance": calculate_path_cost(graph, path, 'distance')
            }
            
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
                
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}

def dfs_search(graph, start, goal):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
    
    stack = [[start]]
    visited = {start}
    explored_nodes = 0
    
    while stack:
        path = stack.pop()
        node = path[-1]
        explored_nodes += 1
        
        if node == goal:
            return {
                "path": path, 
                "explored": explored_nodes, 
                "cost": calculate_path_cost(graph, path, 'travel_cost'),
                "distance": calculate_path_cost(graph, path, 'distance')
            }
            
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(path + [neighbor])
                
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}

def ucs_search(graph, start, goal, weight='travel_cost'):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
        
    queue = [(0, [start])]
    visited = {}
    explored_nodes = 0
    
    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]
        
        if node in visited and visited[node] <= cost:
            continue
            
        visited[node] = cost
        explored_nodes += 1
        
        if node == goal:
            return {
                "path": path, 
                "explored": explored_nodes, 
                "cost": cost,
                "distance": calculate_path_cost(graph, path, 'distance')
            }
            
        for neighbor in graph.neighbors(node):
            edge_data = graph.get_edge_data(node, neighbor)
            step_cost = edge_data.get(weight, 1)
            new_cost = cost + step_cost
            if neighbor not in visited or new_cost < visited[neighbor]:
                heapq.heappush(queue, (new_cost, path + [neighbor]))
                
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}

def dijkstra_search(graph, start, goal, weight='distance'):
    # Dijkstra is basically UCS but we typically use it for distance
    return ucs_search(graph, start, goal, weight)

def astar_search(graph, start, goal, weight='travel_cost'):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
        
    goal_data = graph.nodes[goal]
    
    def heuristic(node):
        node_data = graph.nodes[node]
        dist = haversine(node_data['lat'], node_data['lng'], goal_data['lat'], goal_data['lng'])
        if weight == 'travel_cost':
            return dist * 0.15 # Approx cost per km
        elif weight == 'distance':
            return dist
        return dist * 0.1

    queue = [(heuristic(start), 0, [start])] # (f, g, path)
    visited = {}
    explored_nodes = 0
    
    while queue:
        f, g, path = heapq.heappop(queue)
        node = path[-1]
        
        if node in visited and visited[node] <= g:
            continue
            
        visited[node] = g
        explored_nodes += 1
        
        if node == goal:
            return {
                "path": path, 
                "explored": explored_nodes, 
                "cost": calculate_path_cost(graph, path, 'travel_cost'),
                "distance": calculate_path_cost(graph, path, 'distance')
            }
            
        for neighbor in graph.neighbors(node):
            edge_data = graph.get_edge_data(node, neighbor)
            step_cost = edge_data.get(weight, 1)
            new_g = g + step_cost
            new_f = new_g + heuristic(neighbor)
            
            if neighbor not in visited or new_g < visited[neighbor]:
                heapq.heappush(queue, (new_f, new_g, path + [neighbor]))
                
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}

def gbfs_search(graph, start, goal):
    """Greedy Best First Search"""
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
        
    goal_data = graph.nodes[goal]
    
    def heuristic(node):
        node_data = graph.nodes[node]
        return haversine(node_data['lat'], node_data['lng'], goal_data['lat'], goal_data['lng'])

    queue = [(heuristic(start), [start])]
    visited = {start}
    explored_nodes = 0
    
    while queue:
        h, path = heapq.heappop(queue)
        node = path[-1]
        explored_nodes += 1
        
        if node == goal:
            return {
                "path": path, 
                "explored": explored_nodes, 
                "cost": calculate_path_cost(graph, path, 'travel_cost'),
                "distance": calculate_path_cost(graph, path, 'distance')
            }
            
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(queue, (heuristic(neighbor), path + [neighbor]))
                
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}

def bidirectional_search(graph, start, goal):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": 0, "cost": 0, "distance": 0}
        
    if start == goal:
        return {"path": [start], "explored": 1, "cost": 0, "distance": 0}

    # Queues for BFS from both ends
    q_fwd = deque([start])
    q_bwd = deque([goal])
    
    # Visited dictionaries storing the path from start/goal to the node
    visited_fwd = {start: [start]}
    visited_bwd = {goal: [goal]}
    
    explored_nodes = 0
    intersection_node = None
    
    while q_fwd and q_bwd:
        # Expand forward
        node_fwd = q_fwd.popleft()
        explored_nodes += 1
        
        for neighbor in graph.neighbors(node_fwd):
            if neighbor not in visited_fwd:
                visited_fwd[neighbor] = visited_fwd[node_fwd] + [neighbor]
                q_fwd.append(neighbor)
                if neighbor in visited_bwd:
                    intersection_node = neighbor
                    break
        
        if intersection_node:
            break
            
        # Expand backward
        node_bwd = q_bwd.popleft()
        explored_nodes += 1
        
        for neighbor in graph.neighbors(node_bwd):
            if neighbor not in visited_bwd:
                visited_bwd[neighbor] = visited_bwd[node_bwd] + [neighbor]
                q_bwd.append(neighbor)
                if neighbor in visited_fwd:
                    intersection_node = neighbor
                    break
                    
        if intersection_node:
            break

    if intersection_node:
        path_fwd = visited_fwd[intersection_node]
        path_bwd = visited_bwd[intersection_node]
        # path_bwd is goal -> intersection, so we need to reverse it and remove the duplicate intersection node
        full_path = path_fwd + path_bwd[::-1][1:]
        return {
            "path": full_path,
            "explored": explored_nodes,
            "cost": calculate_path_cost(graph, full_path, 'travel_cost'),
            "distance": calculate_path_cost(graph, full_path, 'distance')
        }
        
    return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}
