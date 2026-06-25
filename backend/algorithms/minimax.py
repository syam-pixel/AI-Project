def calculate_utility(edge_data, preferences):
    """
    Calculate a utility score for an edge based on user preferences.
    Higher is better.
    """
    # Base positive scores
    scenic_score = edge_data.get('scenic_score', 0.5) * preferences.get('scenic_weight', 1.0)
    safety_score = edge_data.get('safety_score', 0.8) * preferences.get('safety_weight', 1.0)
    
    # Negative factors (lower is better, so we subtract from utility)
    traffic = edge_data.get('traffic', 0.5) * preferences.get('traffic_weight', 1.0)
    weather_risk = edge_data.get('weather_risk', 0.1) * preferences.get('weather_weight', 1.0)
    crowd_level = edge_data.get('crowd_level', 0.5) * preferences.get('crowd_weight', 1.0)
    cost = edge_data.get('travel_cost', 50) / 100 * preferences.get('cost_weight', 1.0) # Normalize cost
    
    # Simple utility formula (Maximized)
    utility = (scenic_score + safety_score) - (traffic + weather_risk + crowd_level + cost)
    return utility

def minimax_decision(graph, start, goal, depth_limit=5, preferences=None):
    """
    Uses Minimax with Alpha-Beta pruning to find the path that maximizes utility.
    We treat it as a single-player game against 'nature' (traffic/weather), but simplified 
    here to maximize the cumulative utility score.
    """
    if preferences is None:
        preferences = {}
        
    explored_nodes = 0
    
    def max_value(current_node, current_path, depth, alpha, beta, current_utility):
        nonlocal explored_nodes
        explored_nodes += 1
        
        if current_node == goal:
            return current_utility, current_path
            
        if depth >= depth_limit:
            # Use heuristic for remaining utility (simplified: distance based penalty)
            return current_utility - 0.5, current_path
            
        best_utility = float('-inf')
        best_path = []
        has_neighbors = False
        
        for neighbor in graph.neighbors(current_node):
            if neighbor in current_path:
                continue
                
            has_neighbors = True
            edge_data = graph.get_edge_data(current_node, neighbor)
            step_utility = calculate_utility(edge_data, preferences)
            
            # Here we might insert a min_value node if we model nature adversarially,
            # but for route planning, we just accumulate utility and maximize it.
            # To strictly follow minimax structure with alpha-beta, we assume we just maximize.
            # If we want a true adversarial setup: "nature" tries to minimize utility.
            # For simplicity, we just use Alpha-Beta structure on max nodes (Greedy Max).
            
            val, p = min_value(neighbor, current_path + [neighbor], depth + 1, alpha, beta, current_utility + step_utility)
            
            if val > best_utility:
                best_utility = val
                best_path = p
                
            alpha = max(alpha, best_utility)
            if best_utility >= beta:
                break # Beta pruning
                
        if not has_neighbors:
            return current_utility - 1.0, current_path
            
        return best_utility, best_path

    def min_value(current_node, current_path, depth, alpha, beta, current_utility):
        """
        Nature's turn: Nature minimizes our utility by presenting worst-case scenarios.
        """
        nonlocal explored_nodes
        explored_nodes += 1
        
        if current_node == goal:
            return current_utility, current_path
            
        if depth >= depth_limit:
            return current_utility - 0.5, current_path
            
        worst_utility = float('inf')
        worst_path = []
        has_neighbors = False
        
        for neighbor in graph.neighbors(current_node):
            if neighbor in current_path:
                continue
                
            has_neighbors = True
            edge_data = graph.get_edge_data(current_node, neighbor)
            # Nature applies maximum risk penalty
            nature_penalty = edge_data.get('weather_risk', 0) + edge_data.get('traffic', 0)
            step_utility = -nature_penalty
            
            val, p = max_value(neighbor, current_path + [neighbor], depth + 1, alpha, beta, current_utility + step_utility)
            
            if val < worst_utility:
                worst_utility = val
                worst_path = p
                
            beta = min(beta, worst_utility)
            if worst_utility <= alpha:
                break # Alpha pruning
                
        if not has_neighbors:
            return current_utility - 1.0, current_path
            
        return worst_utility, worst_path

    # Start with max turn
    final_utility, best_path = max_value(start, [start], 0, float('-inf'), float('inf'), 0)
    
    # Calculate actual cost/distance of the best path for consistency
    def calculate_path_cost(g, p, w):
        if not p: return 0
        c = 0
        for i in range(len(p)-1):
            e = g.get_edge_data(p[i], p[i+1])
            if e: c += e.get(w, 1)
        return c

    return {
        "path": best_path,
        "explored": explored_nodes,
        "cost": calculate_path_cost(graph, best_path, 'travel_cost'),
        "distance": calculate_path_cost(graph, best_path, 'distance'),
        "utility": final_utility
    }
