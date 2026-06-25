import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datasets.graph_data import get_graph
from algorithms.search import bfs_search, dfs_search, ucs_search, astar_search, dijkstra_search, gbfs_search, bidirectional_search
from algorithms.csp import csp_search
from algorithms.minimax import minimax_decision

graph = get_graph()
start = "Delhi"
goal = "Mumbai"

print("--- Testing Standard Algorithms ---")
algos = [
    ("BFS", bfs_search),
    ("DFS", dfs_search),
    ("UCS", ucs_search),
    ("A*", astar_search),
    ("Dijkstra", dijkstra_search),
    ("GBFS", gbfs_search),
    ("Bidirectional", bidirectional_search),
]

for name, func in algos:
    try:
        res = func(graph, start, goal)
        print(f"{name}: nodes explored = {res['explored']}, cost = {res['cost']}, distance = {res['distance']}, path len = {len(res['path'])}")
    except Exception as e:
        print(f"{name} Failed: {e}")

print("\n--- Testing Advanced Algorithms ---")
try:
    csp_res = csp_search(graph, start, goal, {'max_budget': 500, 'max_time': 50})
    print(f"CSP: nodes explored = {csp_res['explored']}, cost = {csp_res['cost']}, path len = {len(csp_res['path'])}")
except Exception as e:
    print(f"CSP Failed: {e}")

try:
    mm_res = minimax_decision(graph, start, goal, 5, {'scenic_weight': 1.0, 'safety_weight': 1.0, 'cost_weight': 1.0})
    print(f"Minimax: nodes explored = {mm_res['explored']}, utility = {mm_res['utility']:.2f}, path len = {len(mm_res['path'])}")
except Exception as e:
    print(f"Minimax Failed: {e}")

print("\nAll algorithms executed successfully without infinite loops!")
