import pandas as pd
import random
from typing import List, Dict
import hashlib

# Load service center and shipment data
def load_network_data():
    centers = pd.read_csv("data/service_centers.csv")
    shipments = pd.read_csv("data/sample_shipments.csv")
    return centers, shipments

# Generate deterministic route with minimum 4 locations
def compute_deterministic_route(origin: str, destination: str, centers: List[str], seed_str: str = "") -> List[str]:
    if origin == destination:
        return [origin]

    route = [origin]
    available = [c for c in centers if c not in {origin, destination}]
    seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10 ** 8)
    random.seed(seed)
    intermediates = random.sample(available, min(2, len(available)))
    route += intermediates
    route.append(destination)
    return route

# Correct bypass logic: previous center has enough freight to skip the next center

def evaluate_bypass(route: List[str], centers_df: pd.DataFrame, all_shipments: pd.DataFrame,
                    current_shipment: Dict[str, str], trailer_cube_capacity: float = 100.0) -> List[Dict[str, str]]:
    destination = current_shipment["destination"]
    current_cube = float(current_shipment["cube"])
    bypass_info = []

    for i in range(1, len(route) - 1):  # Look at pairs: prev -> current -> next
        prev_center = route[i - 1]
        current_center = route[i]

        # Check if the previous center has shipments directly to the final destination
        matching = all_shipments[
            (all_shipments["origin"] == prev_center) &
            (all_shipments["destination"] == destination)
        ]

        if not matching.empty:
            total_cube = matching["cube"].sum() + current_cube
            if 0 < total_cube <= trailer_cube_capacity:
                matching_shipments = matching.to_dict(orient="records")
                bypass_info.append({
                    "center": current_center,
                    "combined_cube": round(total_cube, 2),
                    "matching_shipments": matching_shipments
                })

    return bypass_info

# Full shipment routing pipeline
def route_shipment(shipment: Dict[str, str]) -> Dict:
    centers_df, shipments_df = load_network_data()
    center_codes = centers_df["code"].tolist()
    distance_matrix = generate_distance_matrix(centers_df)

    seed_str = f"{shipment['origin']}_{shipment['destination']}_{shipment['weight']}_{shipment['cube']}"
    route = compute_deterministic_route(shipment["origin"], shipment["destination"], center_codes, seed_str=seed_str)

    bypass_data = evaluate_bypass(route, centers_df, shipments_df, shipment)
    bypassed = [b["center"] for b in bypass_data]

    final_route = [stop for stop in route if stop not in bypassed] if bypassed else route.copy()

    total_distance = sum(
        distance_matrix[final_route[i]][final_route[i + 1]]
        for i in range(len(final_route) - 1)
    )

    return {
        "original_route": route,
        "bypassed_centers": bypassed,
        "final_route": final_route,
        "estimated_distance": total_distance,
        "shipment": shipment,
        "bypass_details": bypass_data
    }

# Generate consistent distance matrix
def generate_distance_matrix(centers: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    codes = centers["code"].tolist()
    matrix = {}
    for src in codes:
        matrix[src] = {}
        for dst in codes:
            if src != dst:
                matrix[src][dst] = 1000 + abs(hash(f"{src}-{dst}")) % 1000  # consistent range: 1000–1999
    return matrix

# Example usage
if __name__ == "__main__":
    test_shipment = {
        "origin": "BOS",
        "destination": "LAX",
        "weight": 2800,
        "cube": 45.0
    }
    result = route_shipment(test_shipment)
    from pprint import pprint
    pprint(result)

