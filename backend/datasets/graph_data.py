import random
import networkx as nx

# 50+ Famous Indian Places
CITIES = [
    "Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", 
    "Jaipur", "Agra", "Varanasi", "Kochi", "Goa", "Pune", 
    "Ahmedabad", "Udaipur", "Jodhpur", "Amritsar", "Rishikesh", "Shimla", 
    "Manali", "Darjeeling", "Mysore", "Ooty", "Munnar", "Hampi", 
    "Madurai", "Tirupati", "Bhubaneswar", "Puri", "Guwahati", "Shillong", 
    "Gangtok", "Leh", "Srinagar", "Chandigarh", "Lucknow", "Bhopal", 
    "Indore", "Nagpur", "Patna", "Ranchi",
    "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", 
    "Rajahmundry", "Kakinada", "Kadapa", "Anantapur", "Amaravati",
    "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Nashik", "Aurangabad", "Kanpur", "Prayagraj", "Gwalior", "Jabalpur", "Ujjain", "Bikaner", "Jaisalmer", "Ajmer", "Kota", "Ludhiana", "Jalandhar", "Gurugram", "Noida", "Gaya", "Jamshedpur", "Dhanbad", "Siliguri", "Raipur", "Bhilai", "Cuttack", "Coimbatore", "Salem", "Trichy", "Mangaluru", "Hubli", "Thiruvananthapuram", "Kozhikode", "Thrissur"]

COORDS = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Bengaluru": (12.9716, 77.5946), 
    "Hyderabad": (17.3850, 78.4867), "Chennai": (13.0827, 80.2707), "Kolkata": (22.5726, 88.3639), 
    "Jaipur": (26.9124, 75.7873), "Agra": (27.1767, 78.0081), "Varanasi": (25.3176, 82.9739), 
    "Kochi": (9.9312, 76.2673), "Goa": (15.2993, 74.1240), "Pune": (18.5204, 73.8567), 
    "Ahmedabad": (23.0225, 72.5714), "Udaipur": (24.5854, 73.7125), "Jodhpur": (26.2389, 73.0243), 
    "Amritsar": (31.6340, 74.8723), "Rishikesh": (30.0869, 78.2676), "Shimla": (31.1048, 77.1734), 
    "Manali": (32.2396, 77.1887), "Darjeeling": (27.0410, 88.2663), "Mysore": (12.2958, 76.6394), 
    "Ooty": (11.4102, 76.6950), "Munnar": (10.0889, 77.0595), "Hampi": (15.3350, 76.4600), 
    "Madurai": (9.9252, 78.1198), "Tirupati": (13.6288, 79.4192), "Bhubaneswar": (20.2961, 85.8245), 
    "Puri": (19.8135, 85.8312), "Guwahati": (26.1445, 91.7362), "Shillong": (25.5788, 91.8933), 
    "Gangtok": (27.3314, 88.6138), "Leh": (34.1526, 77.5771), "Srinagar": (34.0837, 74.7973), 
    "Chandigarh": (30.7333, 76.7794), "Lucknow": (26.8467, 80.9462), "Bhopal": (23.2599, 77.4126), 
    "Indore": (22.7196, 75.8577), "Nagpur": (21.1458, 79.0882), "Patna": (25.5941, 85.1376), 
    "Ranchi": (23.3441, 85.3096),
    "Visakhapatnam": (17.6868, 83.2185), "Vijayawada": (16.5062, 80.6480), "Guntur": (16.3067, 80.4365),
    "Nellore": (14.4426, 79.9865), "Kurnool": (15.8281, 78.0373), "Rajahmundry": (17.0005, 81.8040),
    "Kakinada": (16.9891, 82.2475), "Kadapa": (14.4673, 78.8242), "Anantapur": (14.6819, 77.6006),
    "Amaravati": (16.5730, 80.3575),
    "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812), "Rajkot": (22.3039, 70.8022), "Gandhinagar": (23.2156, 72.6369), "Nashik": (19.9975, 73.7898), "Aurangabad": (19.8762, 75.3433), "Kanpur": (26.4499, 80.3319), "Prayagraj": (25.4358, 81.8463), "Gwalior": (26.2124, 78.1772), "Jabalpur": (23.1815, 79.9864), "Ujjain": (23.1765, 75.7885), "Bikaner": (28.0229, 73.3119), "Jaisalmer": (26.9157, 70.9083), "Ajmer": (26.4499, 74.6399), "Kota": (25.2138, 75.8648), "Ludhiana": (30.901, 75.8573), "Jalandhar": (31.326, 75.5762), "Gurugram": (28.4595, 77.0266), "Noida": (28.5355, 77.391), "Gaya": (24.7914, 85.0002), "Jamshedpur": (22.8046, 86.2029), "Dhanbad": (23.7957, 86.4304), "Siliguri": (26.7271, 88.3953), "Raipur": (21.2514, 81.6296), "Bhilai": (21.1938, 81.3509), "Cuttack": (20.4625, 85.883), "Coimbatore": (11.0168, 76.9558), "Salem": (11.6643, 78.146), "Trichy": (10.7905, 78.7047), "Mangaluru": (12.9141, 74.856), "Hubli": (15.3647, 75.124), "Thiruvananthapuram": (8.5241, 76.9366), "Kozhikode": (11.2588, 75.7804), "Thrissur": (10.5276, 76.2144)}

G = nx.Graph()
for city in CITIES:
    G.add_node(city, lat=COORDS[city][0], lng=COORDS[city][1])

# Format: (u, v, distance_km, cost_usd, traffic, weather_risk, travel_time_hours, crowd_level)
EDGES = [
    # North India network
    ("Delhi", "Agra", 233, 30, 0.6, 0.1, 3.5, 0.9),
    ("Delhi", "Jaipur", 281, 40, 0.5, 0.2, 5.0, 0.8),
    ("Delhi", "Chandigarh", 244, 35, 0.4, 0.1, 4.5, 0.5),
    ("Delhi", "Rishikesh", 242, 30, 0.7, 0.4, 6.0, 0.7),
    ("Delhi", "Lucknow", 553, 60, 0.5, 0.2, 8.0, 0.6),
    ("Agra", "Jaipur", 240, 35, 0.4, 0.1, 4.5, 0.8),
    ("Agra", "Lucknow", 336, 40, 0.5, 0.1, 5.0, 0.6),
    ("Jaipur", "Jodhpur", 334, 45, 0.3, 0.1, 6.0, 0.6),
    ("Jaipur", "Udaipur", 393, 50, 0.4, 0.1, 7.0, 0.7),
    ("Jodhpur", "Udaipur", 250, 35, 0.2, 0.1, 4.5, 0.6),
    ("Chandigarh", "Shimla", 113, 20, 0.6, 0.5, 3.5, 0.8),
    ("Chandigarh", "Amritsar", 226, 30, 0.4, 0.2, 4.0, 0.7),
    ("Shimla", "Manali", 248, 40, 0.5, 0.6, 7.0, 0.7),
    ("Manali", "Leh", 473, 80, 0.4, 0.8, 14.0, 0.5),
    ("Srinagar", "Leh", 418, 70, 0.5, 0.7, 10.0, 0.4),
    ("Amritsar", "Srinagar", 432, 65, 0.4, 0.6, 10.0, 0.5),
    
    # West & Central India network
    ("Delhi", "Ahmedabad", 946, 100, 0.4, 0.1, 14.0, 0.6),
    ("Ahmedabad", "Udaipur", 260, 35, 0.5, 0.1, 5.0, 0.6),
    ("Ahmedabad", "Indore", 390, 45, 0.4, 0.1, 7.5, 0.5),
    ("Ahmedabad", "Mumbai", 524, 70, 0.6, 0.2, 9.0, 0.8),
    ("Indore", "Bhopal", 190, 25, 0.5, 0.1, 3.5, 0.6),
    ("Bhopal", "Nagpur", 353, 45, 0.4, 0.1, 6.5, 0.5),
    ("Nagpur", "Hyderabad", 500, 60, 0.5, 0.1, 8.5, 0.6),
    ("Mumbai", "Pune", 150, 25, 0.8, 0.3, 3.0, 0.7),
    ("Mumbai", "Goa", 590, 80, 0.5, 0.4, 11.0, 0.9),
    ("Pune", "Goa", 450, 60, 0.4, 0.5, 9.0, 0.8),
    ("Pune", "Hyderabad", 560, 70, 0.5, 0.2, 10.0, 0.6),
    ("Goa", "Hampi", 314, 45, 0.3, 0.2, 7.0, 0.7),
    
    # South India network
    ("Hyderabad", "Bengaluru", 569, 75, 0.6, 0.2, 9.5, 0.7),
    ("Hyderabad", "Tirupati", 555, 70, 0.4, 0.1, 10.0, 0.8),
    ("Bengaluru", "Chennai", 346, 45, 0.7, 0.3, 6.5, 0.8),
    ("Bengaluru", "Mysore", 143, 20, 0.6, 0.2, 3.0, 0.8),
    ("Bengaluru", "Hampi", 341, 45, 0.4, 0.1, 6.0, 0.6),
    ("Chennai", "Tirupati", 133, 20, 0.6, 0.2, 3.5, 0.9),
    ("Chennai", "Madurai", 462, 60, 0.5, 0.3, 8.0, 0.7),
    ("Mysore", "Ooty", 125, 25, 0.5, 0.5, 3.5, 0.8),
    ("Ooty", "Kochi", 281, 45, 0.4, 0.6, 7.5, 0.7),
    ("Kochi", "Munnar", 130, 25, 0.6, 0.7, 4.0, 0.8),
    ("Kochi", "Madurai", 267, 35, 0.5, 0.3, 6.5, 0.6),
    ("Madurai", "Munnar", 153, 25, 0.4, 0.5, 4.5, 0.7),
    
    # East & North-East network
    ("Lucknow", "Varanasi", 320, 40, 0.6, 0.2, 6.0, 0.8),
    ("Varanasi", "Patna", 253, 35, 0.5, 0.1, 5.5, 0.7),
    ("Patna", "Kolkata", 580, 75, 0.6, 0.3, 11.0, 0.8),
    ("Patna", "Ranchi", 330, 45, 0.4, 0.2, 7.5, 0.5),
    ("Ranchi", "Kolkata", 408, 55, 0.5, 0.2, 8.5, 0.6),
    ("Ranchi", "Bhubaneswar", 442, 60, 0.4, 0.3, 9.0, 0.5),
    ("Kolkata", "Bhubaneswar", 440, 60, 0.5, 0.4, 8.5, 0.6),
    ("Bhubaneswar", "Puri", 63, 10, 0.6, 0.3, 1.5, 0.9),
    ("Kolkata", "Darjeeling", 615, 85, 0.6, 0.6, 14.0, 0.8),
    ("Kolkata", "Guwahati", 983, 120, 0.5, 0.5, 20.0, 0.6),
    ("Darjeeling", "Gangtok", 97, 20, 0.5, 0.7, 4.0, 0.8),
    ("Guwahati", "Shillong", 98, 20, 0.6, 0.6, 3.0, 0.7),

    # Andhra Pradesh Network & Connections
    ("Hyderabad", "Kurnool", 213, 25, 0.4, 0.1, 4.0, 0.6),
    ("Kurnool", "Anantapur", 148, 20, 0.3, 0.1, 2.5, 0.5),
    ("Anantapur", "Bengaluru", 214, 25, 0.5, 0.1, 4.0, 0.7),
    ("Hyderabad", "Vijayawada", 275, 30, 0.6, 0.2, 5.0, 0.8),
    ("Vijayawada", "Amaravati", 33, 5, 0.3, 0.1, 1.0, 0.5),
    ("Vijayawada", "Guntur", 38, 5, 0.4, 0.1, 1.0, 0.6),
    ("Guntur", "Nellore", 236, 25, 0.5, 0.2, 4.0, 0.7),
    ("Nellore", "Tirupati", 136, 15, 0.4, 0.1, 2.5, 0.8),
    ("Nellore", "Chennai", 175, 20, 0.6, 0.2, 3.5, 0.8),
    ("Vijayawada", "Rajahmundry", 159, 20, 0.5, 0.2, 3.0, 0.7),
    ("Rajahmundry", "Kakinada", 64, 10, 0.4, 0.1, 1.5, 0.6),
    ("Rajahmundry", "Visakhapatnam", 190, 25, 0.6, 0.3, 4.0, 0.8),
    ("Visakhapatnam", "Bhubaneswar", 442, 60, 0.5, 0.3, 9.0, 0.6),
    ("Kurnool", "Kadapa", 189, 25, 0.3, 0.1, 3.5, 0.5),
    ("Kadapa", "Tirupati", 142, 20, 0.4, 0.1, 3.0, 0.7),
    
    # Cross-regional connections
    ("Delhi", "Mumbai", 1415, 150, 0.7, 0.2, 24.0, 0.8),
    ("Mumbai", "Bengaluru", 980, 110, 0.6, 0.3, 16.0, 0.7),
    ("Kolkata", "Chennai", 1669, 180, 0.5, 0.5, 28.0, 0.6),
    ("Hyderabad", "Bhubaneswar", 1043, 120, 0.5, 0.4, 18.0, 0.5),
    ("Nagpur", "Kolkata", 1120, 130, 0.4, 0.3, 20.0, 0.5),
    ("Varanasi", "Nagpur", 725, 85, 0.5, 0.1, 14.0, 0.6),
    ("Jaipur", "Ahmedabad", 677, 80, 0.5, 0.1, 11.0, 0.6),
    # Expansion Cities Phase 2
    ('Surat', 'Mumbai', 280, 30, 0.6, 0.1, 5.0, 0.8),
    ('Surat', 'Vadodara', 150, 20, 0.5, 0.1, 3.0, 0.7),
    ('Vadodara', 'Ahmedabad', 110, 15, 0.4, 0.1, 2.0, 0.8),
    ('Vadodara', 'Indore', 340, 40, 0.5, 0.1, 6.0, 0.6),
    ('Rajkot', 'Ahmedabad', 215, 25, 0.4, 0.1, 4.0, 0.6),
    ('Gandhinagar', 'Ahmedabad', 27, 5, 0.3, 0.1, 0.8, 0.5),
    ('Nashik', 'Mumbai', 165, 20, 0.5, 0.2, 3.5, 0.7),
    ('Nashik', 'Pune', 210, 25, 0.6, 0.2, 4.5, 0.6),
    ('Aurangabad', 'Nashik', 180, 20, 0.4, 0.1, 3.5, 0.5),
    ('Aurangabad', 'Pune', 235, 25, 0.5, 0.1, 4.5, 0.6),
    ('Kanpur', 'Lucknow', 90, 10, 0.6, 0.1, 2.0, 0.8),
    ('Kanpur', 'Agra', 275, 30, 0.5, 0.1, 5.0, 0.7),
    ('Prayagraj', 'Kanpur', 200, 25, 0.4, 0.1, 4.0, 0.6),
    ('Prayagraj', 'Varanasi', 120, 15, 0.5, 0.1, 2.5, 0.8),
    ('Gwalior', 'Agra', 120, 15, 0.4, 0.1, 2.5, 0.6),
    ('Gwalior', 'Bhopal', 420, 50, 0.5, 0.1, 7.5, 0.5),
    ('Jabalpur', 'Bhopal', 300, 35, 0.4, 0.1, 6.0, 0.5),
    ('Jabalpur', 'Nagpur', 275, 30, 0.5, 0.1, 5.5, 0.6),
    ('Ujjain', 'Indore', 55, 10, 0.3, 0.1, 1.2, 0.7),
    ('Ujjain', 'Bhopal', 190, 20, 0.4, 0.1, 3.5, 0.6),
    ('Bikaner', 'Jodhpur', 250, 30, 0.3, 0.1, 4.5, 0.5),
    ('Jaisalmer', 'Jodhpur', 280, 30, 0.2, 0.1, 5.0, 0.4),
    ('Ajmer', 'Jaipur', 135, 15, 0.4, 0.1, 2.5, 0.6),
    ('Ajmer', 'Jodhpur', 205, 25, 0.3, 0.1, 4.0, 0.5),
    ('Kota', 'Jaipur', 250, 30, 0.4, 0.1, 4.5, 0.6),
    ('Ludhiana', 'Chandigarh', 105, 15, 0.5, 0.2, 2.0, 0.7),
    ('Jalandhar', 'Ludhiana', 60, 10, 0.4, 0.1, 1.2, 0.6),
    ('Jalandhar', 'Amritsar', 80, 10, 0.5, 0.1, 1.5, 0.7),
    ('Gurugram', 'Delhi', 30, 5, 0.8, 0.2, 1.0, 0.9),
    ('Noida', 'Delhi', 20, 5, 0.8, 0.2, 0.8, 0.9),
    ('Gaya', 'Patna', 100, 15, 0.5, 0.1, 2.5, 0.7),
    ('Gaya', 'Varanasi', 250, 30, 0.4, 0.1, 5.0, 0.6),
    ('Jamshedpur', 'Ranchi', 130, 15, 0.4, 0.1, 3.0, 0.6),
    ('Dhanbad', 'Ranchi', 150, 20, 0.5, 0.1, 3.5, 0.6),
    ('Dhanbad', 'Jamshedpur', 140, 15, 0.4, 0.1, 3.0, 0.5),
    ('Jamshedpur', 'Kolkata', 280, 35, 0.6, 0.2, 6.0, 0.7),
    ('Siliguri', 'Darjeeling', 60, 10, 0.5, 0.6, 2.5, 0.8),
    ('Siliguri', 'Gangtok', 110, 15, 0.6, 0.7, 4.0, 0.8),
    ('Siliguri', 'Guwahati', 470, 55, 0.5, 0.4, 10.0, 0.6),
    ('Siliguri', 'Patna', 450, 50, 0.4, 0.3, 9.0, 0.5),
    ('Raipur', 'Nagpur', 285, 30, 0.5, 0.1, 5.5, 0.6),
    ('Bhilai', 'Raipur', 30, 5, 0.3, 0.1, 0.8, 0.5),
    ('Raipur', 'Bhubaneswar', 530, 60, 0.4, 0.2, 10.0, 0.5),
    ('Cuttack', 'Bhubaneswar', 25, 5, 0.4, 0.1, 0.5, 0.7),
    ('Coimbatore', 'Kochi', 190, 25, 0.6, 0.4, 4.5, 0.7),
    ('Coimbatore', 'Ooty', 85, 15, 0.5, 0.5, 2.5, 0.8),
    ('Salem', 'Coimbatore', 165, 20, 0.5, 0.2, 3.5, 0.6),
    ('Salem', 'Bengaluru', 200, 25, 0.6, 0.2, 4.0, 0.7),
    ('Trichy', 'Madurai', 135, 15, 0.4, 0.1, 2.5, 0.6),
    ('Trichy', 'Chennai', 330, 40, 0.6, 0.2, 6.0, 0.7),
    ('Mangaluru', 'Goa', 360, 45, 0.5, 0.3, 8.0, 0.7),
    ('Mangaluru', 'Bengaluru', 350, 40, 0.6, 0.4, 7.5, 0.6),
    ('Hubli', 'Goa', 160, 20, 0.4, 0.3, 4.0, 0.6),
    ('Hubli', 'Bengaluru', 410, 50, 0.5, 0.2, 7.0, 0.5),
    ('Thiruvananthapuram', 'Kochi', 200, 25, 0.6, 0.4, 5.0, 0.7),
    ('Thiruvananthapuram', 'Madurai', 260, 35, 0.5, 0.2, 5.5, 0.6),
    ('Kozhikode', 'Kochi', 180, 20, 0.6, 0.4, 4.5, 0.7),
    ('Kozhikode', 'Mangaluru', 230, 30, 0.5, 0.3, 5.5, 0.6),
    ('Thrissur', 'Kochi', 85, 10, 0.6, 0.3, 2.0, 0.7),
    ('Thrissur', 'Coimbatore', 115, 15, 0.5, 0.3, 2.5, 0.6)
]

import json
import os

for edge in EDGES:
    u, v, d, c, t, w, tt, cl = edge
    G.add_edge(u, v, distance=d, travel_cost=c, traffic=t, weather_risk=w, travel_time=tt, crowd_level=cl, geometry=None)

# Load real geometries if available
real_roads_path = os.path.join(os.path.dirname(__file__), 'real_roads.json')
if os.path.exists(real_roads_path):
    with open(real_roads_path, 'r') as f:
        real_geom = json.load(f)
        for g in real_geom:
            u = g['source']
            v = g['target']
            geom = g['geometry']
            if G.has_edge(u, v):
                G[u][v]['geometry'] = geom

def get_graph_data():
    nodes = [{"id": n, "lat": data.get("lat", 0), "lng": data.get("lng", 0)} for n, data in G.nodes(data=True)]
    edges = [
        {
            "source": u, 
            "target": v, 
            "distance": d["distance"],
            "travel_cost": d["travel_cost"],
            "traffic": d["traffic"],
            "weather_risk": d["weather_risk"],
            "travel_time": d["travel_time"],
            "crowd_level": d["crowd_level"],
            "geometry": d.get("geometry")
        }
        for u, v, d in G.edges(data=True)
    ]
    return {"nodes": nodes, "edges": edges}

def get_graph():
    return G
