import requests

tests = ['BFS', 'DFS', 'UCS', 'A*']
for algo in tests:
    res = requests.post('http://localhost:8000/api/search', json={'start':'Delhi', 'goal':'Mumbai', 'algorithm':algo})
    if res.status_code == 200:
        data = res.json()
        print(f"{algo}: path={data.get('path')}, dist={data.get('distance')}")
    else:
        print(f"{algo} Error: {res.text}")

res_csp = requests.post('http://localhost:8000/api/search', json={'start':'Delhi', 'goal':'Mumbai', 'algorithm': 'CSP', 'constraints': {'max_budget': 10000, 'max_time': 100}})
if res_csp.status_code == 200:
    data_csp = res_csp.json()
    print(f"CSP: path={data_csp.get('path')}, cost={data_csp.get('cost')}")
else:
    print(f"CSP Error: {res_csp.text}")
