import json
import re

new_cities = [
    "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Nashik", "Aurangabad", 
    "Kanpur", "Prayagraj", "Gwalior", "Jabalpur", "Ujjain", "Bikaner", 
    "Jaisalmer", "Ajmer", "Kota", "Ludhiana", "Jalandhar", "Gurugram", 
    "Noida", "Gaya", "Jamshedpur", "Dhanbad", "Siliguri", "Raipur", 
    "Bhilai", "Cuttack", "Coimbatore", "Salem", "Trichy", "Mangaluru", 
    "Hubli", "Thiruvananthapuram", "Kozhikode", "Thrissur"
]

new_coords = {
    "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812), "Rajkot": (22.3039, 70.8022),
    "Gandhinagar": (23.2156, 72.6369), "Nashik": (19.9975, 73.7898), "Aurangabad": (19.8762, 75.3433),
    "Kanpur": (26.4499, 80.3319), "Prayagraj": (25.4358, 81.8463), "Gwalior": (26.2124, 78.1772),
    "Jabalpur": (23.1815, 79.9864), "Ujjain": (23.1765, 75.7885), "Bikaner": (28.0229, 73.3119),
    "Jaisalmer": (26.9157, 70.9083), "Ajmer": (26.4499, 74.6399), "Kota": (25.2138, 75.8648),
    "Ludhiana": (30.9010, 75.8573), "Jalandhar": (31.3260, 75.5762), "Gurugram": (28.4595, 77.0266),
    "Noida": (28.5355, 77.3910), "Gaya": (24.7914, 85.0002), "Jamshedpur": (22.8046, 86.2029),
    "Dhanbad": (23.7957, 86.4304), "Siliguri": (26.7271, 88.3953), "Raipur": (21.2514, 81.6296),
    "Bhilai": (21.1938, 81.3509), "Cuttack": (20.4625, 85.8830), "Coimbatore": (11.0168, 76.9558),
    "Salem": (11.6643, 78.1460), "Trichy": (10.7905, 78.7047), "Mangaluru": (12.9141, 74.8560),
    "Hubli": (15.3647, 75.1240), "Thiruvananthapuram": (8.5241, 76.9366), "Kozhikode": (11.2588, 75.7804),
    "Thrissur": (10.5276, 76.2144)
}

new_edges = [
    ("Surat", "Mumbai", 280, 30, 0.6, 0.1, 5.0, 0.8),
    ("Surat", "Vadodara", 150, 20, 0.5, 0.1, 3.0, 0.7),
    ("Vadodara", "Ahmedabad", 110, 15, 0.4, 0.1, 2.0, 0.8),
    ("Vadodara", "Indore", 340, 40, 0.5, 0.1, 6.0, 0.6),
    ("Rajkot", "Ahmedabad", 215, 25, 0.4, 0.1, 4.0, 0.6),
    ("Gandhinagar", "Ahmedabad", 27, 5, 0.3, 0.1, 0.8, 0.5),
    ("Nashik", "Mumbai", 165, 20, 0.5, 0.2, 3.5, 0.7),
    ("Nashik", "Pune", 210, 25, 0.6, 0.2, 4.5, 0.6),
    ("Aurangabad", "Nashik", 180, 20, 0.4, 0.1, 3.5, 0.5),
    ("Aurangabad", "Pune", 235, 25, 0.5, 0.1, 4.5, 0.6),
    ("Kanpur", "Lucknow", 90, 10, 0.6, 0.1, 2.0, 0.8),
    ("Kanpur", "Agra", 275, 30, 0.5, 0.1, 5.0, 0.7),
    ("Prayagraj", "Kanpur", 200, 25, 0.4, 0.1, 4.0, 0.6),
    ("Prayagraj", "Varanasi", 120, 15, 0.5, 0.1, 2.5, 0.8),
    ("Gwalior", "Agra", 120, 15, 0.4, 0.1, 2.5, 0.6),
    ("Gwalior", "Bhopal", 420, 50, 0.5, 0.1, 7.5, 0.5),
    ("Jabalpur", "Bhopal", 300, 35, 0.4, 0.1, 6.0, 0.5),
    ("Jabalpur", "Nagpur", 275, 30, 0.5, 0.1, 5.5, 0.6),
    ("Ujjain", "Indore", 55, 10, 0.3, 0.1, 1.2, 0.7),
    ("Ujjain", "Bhopal", 190, 20, 0.4, 0.1, 3.5, 0.6),
    ("Bikaner", "Jodhpur", 250, 30, 0.3, 0.1, 4.5, 0.5),
    ("Jaisalmer", "Jodhpur", 280, 30, 0.2, 0.1, 5.0, 0.4),
    ("Ajmer", "Jaipur", 135, 15, 0.4, 0.1, 2.5, 0.6),
    ("Ajmer", "Jodhpur", 205, 25, 0.3, 0.1, 4.0, 0.5),
    ("Kota", "Jaipur", 250, 30, 0.4, 0.1, 4.5, 0.6),
    ("Ludhiana", "Chandigarh", 105, 15, 0.5, 0.2, 2.0, 0.7),
    ("Jalandhar", "Ludhiana", 60, 10, 0.4, 0.1, 1.2, 0.6),
    ("Jalandhar", "Amritsar", 80, 10, 0.5, 0.1, 1.5, 0.7),
    ("Gurugram", "Delhi", 30, 5, 0.8, 0.2, 1.0, 0.9),
    ("Noida", "Delhi", 20, 5, 0.8, 0.2, 0.8, 0.9),
    ("Gaya", "Patna", 100, 15, 0.5, 0.1, 2.5, 0.7),
    ("Gaya", "Varanasi", 250, 30, 0.4, 0.1, 5.0, 0.6),
    ("Jamshedpur", "Ranchi", 130, 15, 0.4, 0.1, 3.0, 0.6),
    ("Dhanbad", "Ranchi", 150, 20, 0.5, 0.1, 3.5, 0.6),
    ("Dhanbad", "Jamshedpur", 140, 15, 0.4, 0.1, 3.0, 0.5),
    ("Jamshedpur", "Kolkata", 280, 35, 0.6, 0.2, 6.0, 0.7),
    ("Siliguri", "Darjeeling", 60, 10, 0.5, 0.6, 2.5, 0.8),
    ("Siliguri", "Gangtok", 110, 15, 0.6, 0.7, 4.0, 0.8),
    ("Siliguri", "Guwahati", 470, 55, 0.5, 0.4, 10.0, 0.6),
    ("Siliguri", "Patna", 450, 50, 0.4, 0.3, 9.0, 0.5),
    ("Raipur", "Nagpur", 285, 30, 0.5, 0.1, 5.5, 0.6),
    ("Bhilai", "Raipur", 30, 5, 0.3, 0.1, 0.8, 0.5),
    ("Raipur", "Bhubaneswar", 530, 60, 0.4, 0.2, 10.0, 0.5),
    ("Cuttack", "Bhubaneswar", 25, 5, 0.4, 0.1, 0.5, 0.7),
    ("Coimbatore", "Kochi", 190, 25, 0.6, 0.4, 4.5, 0.7),
    ("Coimbatore", "Ooty", 85, 15, 0.5, 0.5, 2.5, 0.8),
    ("Salem", "Coimbatore", 165, 20, 0.5, 0.2, 3.5, 0.6),
    ("Salem", "Bengaluru", 200, 25, 0.6, 0.2, 4.0, 0.7),
    ("Trichy", "Madurai", 135, 15, 0.4, 0.1, 2.5, 0.6),
    ("Trichy", "Chennai", 330, 40, 0.6, 0.2, 6.0, 0.7),
    ("Mangaluru", "Goa", 360, 45, 0.5, 0.3, 8.0, 0.7),
    ("Mangaluru", "Bengaluru", 350, 40, 0.6, 0.4, 7.5, 0.6),
    ("Hubli", "Goa", 160, 20, 0.4, 0.3, 4.0, 0.6),
    ("Hubli", "Bengaluru", 410, 50, 0.5, 0.2, 7.0, 0.5),
    ("Thiruvananthapuram", "Kochi", 200, 25, 0.6, 0.4, 5.0, 0.7),
    ("Thiruvananthapuram", "Madurai", 260, 35, 0.5, 0.2, 5.5, 0.6),
    ("Kozhikode", "Kochi", 180, 20, 0.6, 0.4, 4.5, 0.7),
    ("Kozhikode", "Mangaluru", 230, 30, 0.5, 0.3, 5.5, 0.6),
    ("Thrissur", "Kochi", 85, 10, 0.6, 0.3, 2.0, 0.7),
    ("Thrissur", "Coimbatore", 115, 15, 0.5, 0.3, 2.5, 0.6)
]

filepath = 'd:/HONORS CLASS/term3/CFAI/project {syam}[10]/backend/datasets/graph_data.py'
with open(filepath, 'r') as f:
    content = f.read()

# Append cities
cities_match = re.search(r'CITIES = \[([\s\S]*?)\]', content)
if cities_match:
    cities_str = cities_match.group(1)
    new_cities_str = cities_str.rstrip() + ",\n    " + ", ".join([f'"{c}"' for c in new_cities])
    content = content.replace(cities_match.group(1), new_cities_str)

# Append coords
coords_match = re.search(r'COORDS = \{([\s\S]*?)\}', content)
if coords_match:
    coords_str = coords_match.group(1)
    new_coords_str = coords_str.rstrip() + ",\n    " + ", ".join([f'"{k}": {v}' for k, v in new_coords.items()])
    content = content.replace(coords_match.group(1), new_coords_str)

# Append edges
edges_match = re.search(r'EDGES = \[([\s\S]*?)\]\n', content)
if edges_match:
    edges_str = edges_match.group(1)
    # Format new edges
    new_edges_formatted = "\n    # Expansion Cities Phase 2\n    " + ",\n    ".join([str(e) for e in new_edges])
    new_edges_str = edges_str.rstrip() + "," + new_edges_formatted + "\n"
    content = content.replace(edges_match.group(1), new_edges_str)

with open(filepath, 'w') as f:
    f.write(content)

print("graph_data.py updated successfully!")
