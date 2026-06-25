import json
import time
import requests
import sys
import os

from datasets.graph_data import EDGES, COORDS

all_edges_geom = []
existing_geoms = {}

# Load existing geometries to avoid re-fetching and rate limiting
real_roads_path = 'datasets/real_roads.json'
if os.path.exists(real_roads_path):
    with open(real_roads_path, 'r') as f:
        try:
            data = json.load(f)
            for item in data:
                # Key by source-target pair
                if len(item.get("geometry", [])) > 2:
                    existing_geoms[f"{item['source']}-{item['target']}"] = item['geometry']
        except Exception:
            pass

print("Starting smart fetch...", flush=True)

for edge in EDGES:
    u, v, d, c, t, w, tt, cl = edge
    coord_u = COORDS[u]
    coord_v = COORDS[v]
    
    key = f"{u}-{v}"
    if key in existing_geoms:
        all_edges_geom.append({
            "source": u,
            "target": v,
            "geometry": existing_geoms[key]
        })
        continue
        
    print(f"Fetching geometry for new route: {u} to {v}", flush=True)
    url = f"https://router.project-osrm.org/route/v1/driving/{coord_u[1]},{coord_u[0]};{coord_v[1]},{coord_v[0]}?overview=full&geometries=geojson"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('code') == 'Ok' and data.get('routes'):
            geom = data['routes'][0]['geometry']['coordinates']
            latlngs = [[lat, lng] for lng, lat in geom]
        else:
            latlngs = [coord_u, coord_v]
    except Exception as e:
        print(f"Failed to fetch {u}-{v}: {e}")
        latlngs = [coord_u, coord_v]
        
    all_edges_geom.append({
        "source": u,
        "target": v,
        "geometry": latlngs
    })
    time.sleep(1.0) # 1 second sleep to strictly avoid OSRM rate limits

with open(real_roads_path, 'w') as f:
    json.dump(all_edges_geom, f)
    
print("Done saving real_roads.json", flush=True)
