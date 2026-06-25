import time
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from datasets.graph_data import get_graph_data, get_graph
from algorithms.search import bfs_search, dfs_search, ucs_search, astar_search, dijkstra_search, gbfs_search, bidirectional_search
from algorithms.csp import csp_search
from algorithms.uncertainty import simulate_uncertainty
from algorithms.minimax import minimax_decision

router = APIRouter()

class SearchRequest(BaseModel):
    start: str
    goal: str
    algorithm: str
    constraints: dict = {}
    preferences: dict = {}

class CompareRequest(BaseModel):
    start: str
    goal: str
    constraints: dict = {}
    preferences: dict = {}

# Simple in-memory cache for repeated route requests
route_cache = {}

@router.get("/graph")
async def get_graph_endpoint():
    return await run_in_threadpool(get_graph_data)

def run_algorithm(algo, graph, start, goal, req):
    if algo == "CSP":
        return csp_search(graph, start, goal, req.constraints)
    elif algo == "Minimax":
        return minimax_decision(graph, start, goal, depth_limit=5, preferences=req.preferences)
    elif algo == "BFS":
        return bfs_search(graph, start, goal)
    elif algo == "DFS":
        return dfs_search(graph, start, goal)
    elif algo == "UCS":
        return ucs_search(graph, start, goal)
    elif algo == "A*":
        return astar_search(graph, start, goal)
    elif algo == "Dijkstra":
        return dijkstra_search(graph, start, goal)
    elif algo == "GBFS":
        return gbfs_search(graph, start, goal)
    elif algo == "Bidirectional":
        return bidirectional_search(graph, start, goal)
    else:
        raise ValueError("Unknown algorithm")

@router.post("/search")
async def search_endpoint(req: SearchRequest):
    cache_key = f"{req.start}-{req.goal}-{req.algorithm}-{str(req.constraints)}-{str(req.preferences)}"
    if cache_key in route_cache:
        return route_cache[cache_key]

    graph = get_graph()
    if req.start not in graph or req.goal not in graph:
        raise HTTPException(status_code=400, detail="Start or goal node not in graph")
        
    start_time = time.time()
    
    try:
        result = await run_in_threadpool(run_algorithm, req.algorithm, graph, req.start, req.goal, req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    execution_time = time.time() - start_time
    
    if not result or not result.get("path"):
        return {
            "success": False,
            "message": "No path found",
            "execution_time_ms": round(execution_time * 1000, 2)
        }
        
    # Simulate uncertainty
    uncertainty_results = await run_in_threadpool(simulate_uncertainty, graph, result["path"])
    
    # Calculate utility score
    base_cost = result.get("cost", 0)
    utility = 10000 / (base_cost + 1) * uncertainty_results["success_probability"]
    if req.algorithm == "Minimax":
        utility = result.get("utility", utility)
    
    response_data = {
        "success": True,
        "path": result["path"],
        "explored_nodes": result.get("explored", 0),
        "cost": result.get("cost", 0),
        "distance": result.get("distance", 0),
        "execution_time_ms": round(execution_time * 1000, 2),
        "uncertainty": uncertainty_results,
        "utility_score": round(utility, 2),
        "algorithm": req.algorithm
    }
    
    route_cache[cache_key] = response_data
    return response_data


@router.post("/compare")
async def compare_endpoint(req: CompareRequest):
    graph = get_graph()
    if req.start not in graph or req.goal not in graph:
        raise HTTPException(status_code=400, detail="Start or goal node not in graph")
    
    algorithms = ["BFS", "DFS", "UCS", "A*", "Dijkstra", "GBFS", "Bidirectional", "CSP", "Minimax"]
    results = []
    
    for algo in algorithms:
        start_time = time.time()
        try:
            # We mock a request object for run_algorithm
            mock_req = SearchRequest(start=req.start, goal=req.goal, algorithm=algo, constraints=req.constraints, preferences=req.preferences)
            res = await run_in_threadpool(run_algorithm, algo, graph, req.start, req.goal, mock_req)
            exec_time = time.time() - start_time
            if res and res.get("path"):
                results.append({
                    "algorithm": algo,
                    "execution_time_ms": round(exec_time * 1000, 2),
                    "nodes_explored": res.get("explored", 0),
                    "distance": res.get("distance", 0),
                    "cost": res.get("cost", 0),
                    "path_length": len(res["path"]) - 1
                })
            else:
                results.append({
                    "algorithm": algo,
                    "execution_time_ms": round(exec_time * 1000, 2),
                    "error": "No path found"
                })
        except Exception as e:
            results.append({
                "algorithm": algo,
                "error": str(e)
            })
            
    # Find winners
    valid_results = [r for r in results if "error" not in r]
    if valid_results:
        fastest = min(valid_results, key=lambda x: x["execution_time_ms"])["algorithm"]
        least_nodes = min(valid_results, key=lambda x: x["nodes_explored"])["algorithm"]
        lowest_cost = min(valid_results, key=lambda x: x["cost"])["algorithm"]
        
        for r in results:
            r["is_fastest"] = (r["algorithm"] == fastest)
            r["is_least_nodes"] = (r["algorithm"] == least_nodes)
            r["is_lowest_cost"] = (r["algorithm"] == lowest_cost)
            
    return {"comparisons": results}

@router.get("/recommendations")
async def get_recommendations(destination: str):
    # Mocking recommendations based on destination
    import random
    
    hotels = [
        {"name": f"Grand {destination} Hotel", "rating": round(random.uniform(3.5, 5.0), 1), "type": "Hotel"},
        {"name": f"{destination} Palace Resort", "rating": round(random.uniform(4.0, 5.0), 1), "type": "Hotel"},
    ]
    restaurants = [
        {"name": f"Taste of {destination}", "rating": round(random.uniform(3.8, 5.0), 1), "type": "Restaurant"},
        {"name": f"{destination} Spice Route", "rating": round(random.uniform(4.1, 4.9), 1), "type": "Restaurant"},
    ]
    attractions = [
        {"name": f"{destination} Museum", "rating": round(random.uniform(4.0, 4.8), 1), "type": "Attraction"},
        {"name": f"Historic Fort {destination}", "rating": round(random.uniform(4.2, 5.0), 1), "type": "Attraction"},
    ]
    
    return {
        "destination": destination,
        "recommendations": hotels + restaurants + attractions
    }
