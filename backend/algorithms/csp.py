def get_valid_neighbors(graph, current_node, current_path, constraints, current_cost, current_time):
    valid_neighbors = []
    
    max_budget = constraints.get('max_budget', float('inf'))
    max_time = constraints.get('max_time', float('inf'))
    max_traffic = constraints.get('max_traffic', 1.0)
    max_weather = constraints.get('max_weather', 1.0)
    
    for neighbor in graph.neighbors(current_node):
        if neighbor in current_path:
            continue
            
        edge_data = graph.get_edge_data(current_node, neighbor)
        
        # Check constraints
        if current_cost + edge_data.get('travel_cost', 0) > max_budget:
            continue
        if current_time + edge_data.get('travel_time', 0) > max_time:
            continue
        if edge_data.get('traffic', 0) > max_traffic:
            continue
        if edge_data.get('weather_risk', 0) > max_weather:
            continue
            
        valid_neighbors.append((neighbor, edge_data))
    return valid_neighbors

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

def csp_search(graph, start, goal, constraints):
    explored_nodes = 0
    best_path = None
    best_cost = float('inf')
    
    def backtrack(current_node, current_path, current_cost, current_time):
        nonlocal explored_nodes, best_path, best_cost
        explored_nodes += 1
        
        # Branch and bound: prune if current cost is already worse than the best found
        if current_cost >= best_cost:
            return False
            
        if current_node == goal:
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(current_path)
            return True # Found a better path
            
        neighbors = get_valid_neighbors(graph, current_node, current_path, constraints, current_cost, current_time)
        
        if not neighbors:
            return False
            
        # LCV (Least Constraining Value): pick the neighbor that consumes the least resource ratio
        max_budget = constraints.get('max_budget', float('inf'))
        max_time = constraints.get('max_time', float('inf'))
        
        def lcv_score(neighbor_tuple):
            _, edge_data = neighbor_tuple
            cost_ratio = edge_data.get('travel_cost', 0) / (max_budget if max_budget > 0 and max_budget != float('inf') else 1)
            time_ratio = edge_data.get('travel_time', 0) / (max_time if max_time > 0 and max_time != float('inf') else 1)
            return cost_ratio + time_ratio
            
        # Sort neighbors by LCV to explore promising branches first
        neighbors.sort(key=lcv_score)
        
        for neighbor, edge_data in neighbors:
            current_path.append(neighbor)
            backtrack(
                neighbor, 
                current_path, 
                current_cost + edge_data.get('travel_cost', 0), 
                current_time + edge_data.get('travel_time', 0)
            )
            current_path.pop() # backtrack
            
        return best_path is not None

    backtrack(start, [start], 0, 0)
    
    if best_path:
        return {
            "path": best_path, 
            "explored": explored_nodes, 
            "cost": best_cost,
            "distance": calculate_path_cost(graph, best_path, 'distance')
        }
    else:
        return {"path": [], "explored": explored_nodes, "cost": 0, "distance": 0}
