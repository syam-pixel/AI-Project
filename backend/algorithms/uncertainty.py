import random

def simulate_uncertainty(graph, path):
    if not path or len(path) < 2:
        return {"success_probability": 0, "overall_risk": 0, "base_cost": 0, "simulated_cost": 0, "events": []}
        
    total_base_cost = 0
    simulated_cost = 0
    events = []
    
    success_probability = 1.0
    
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        edge_data = graph.get_edge_data(u, v)
        
        base_cost = edge_data.get('travel_cost', 0)
        total_base_cost += base_cost
        
        traffic = edge_data.get('traffic', 0)
        weather = edge_data.get('weather_risk', 0)
        
        # Probabilistic event: Traffic jam
        # Higher traffic value = higher chance of delay
        if random.random() < traffic:
            delay_cost = base_cost * random.uniform(0.2, 0.8)
            simulated_cost += (base_cost + delay_cost)
            events.append(f"Traffic jam between {u} and {v} (Cost +{int(delay_cost)})")
            success_probability *= (1.0 - traffic * 0.2)
        else:
            simulated_cost += base_cost
            
        # Probabilistic event: Bad weather
        if random.random() < weather:
            weather_delay = base_cost * random.uniform(0.3, 1.0)
            simulated_cost += weather_delay
            events.append(f"Severe weather between {u} and {v} (Cost +{int(weather_delay)})")
            success_probability *= (1.0 - weather * 0.5)
            
    overall_risk = 1.0 - success_probability
    
    return {
        "success_probability": round(success_probability, 2),
        "overall_risk": round(overall_risk, 2),
        "base_cost": int(total_base_cost),
        "simulated_cost": int(simulated_cost),
        "events": events
    }
