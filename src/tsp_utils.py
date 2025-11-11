"""
Utility functions for TSP (Traveling Salesman Problem)
"""

import json
import math
import numpy as np
from typing import Dict, List, Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Tính khoảng cách thực tế giữa 2 điểm trên Trái Đất (km).

    Sử dụng công thức Haversine.

    Parameters:
    -----------
    lat1, lon1 : float
        Latitude và longitude của điểm 1 (degrees)
    lat2, lon2 : float
        Latitude và longitude của điểm 2 (degrees)

    Returns:
    --------
    float
        Khoảng cách theo đường chim bay (km)
    """
    # Earth radius in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance


def load_cities(filepath: str) -> Dict:
    """
    Load cities data từ JSON file.

    Parameters:
    -----------
    filepath : str
        Path to JSON file

    Returns:
    --------
    dict
        Dictionary {city_name: {'lat': ..., 'lon': ..., 'country': ...}}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['cities']


def calculate_tour_distance(tour: List[str], distances: Dict[Tuple[str, str], float]) -> float:
    """
    Tính tổng khoảng cách của một tour.

    Parameters:
    -----------
    tour : List[str]
        Danh sách cities (đã bao gồm quay về start)
    distances : Dict
        Distance matrix

    Returns:
    --------
    float
        Tổng khoảng cách (km)
    """
    total = 0.0
    for i in range(len(tour) - 1):
        city_a = tour[i]
        city_b = tour[i + 1]
        total += distances.get((city_a, city_b), distances.get((city_b, city_a), 0))
    return total


def nearest_neighbor_tsp(cities: Dict, start_city: str) -> Tuple[List[str], float]:
    """
    Greedy nearest neighbor heuristic cho TSP.

    Bắt đầu từ start_city, luôn đi đến city gần nhất chưa thăm.

    Parameters:
    -----------
    cities : Dict
        Cities data với coordinates
    start_city : str
        Starting city

    Returns:
    --------
    Tuple[List[str], float]
        (tour, total_distance)
    """
    # Compute all distances
    distances = {}
    city_list = list(cities.keys())

    for city_a in city_list:
        for city_b in city_list:
            if city_a != city_b:
                dist = haversine_distance(
                    cities[city_a]['lat'], cities[city_a]['lon'],
                    cities[city_b]['lat'], cities[city_b]['lon']
                )
                distances[(city_a, city_b)] = dist

    # Nearest neighbor
    tour = [start_city]
    unvisited = set(city_list) - {start_city}
    current = start_city
    total_distance = 0.0

    while unvisited:
        # Find nearest unvisited city
        nearest = None
        nearest_dist = float('inf')

        for city in unvisited:
            dist = distances[(current, city)]
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = city

        tour.append(nearest)
        total_distance += nearest_dist
        unvisited.remove(nearest)
        current = nearest

    # Return to start
    tour.append(start_city)
    total_distance += distances[(current, start_city)]

    return tour, total_distance


def two_opt_improve(tour: List[str], distances: Dict[Tuple[str, str], float], max_iterations: int = 1000) -> Tuple[List[str], float]:
    """
    Cải thiện tour bằng 2-opt local search.

    2-opt: Hoán đổi 2 edges để giảm total distance.

    Parameters:
    -----------
    tour : List[str]
        Tour ban đầu (bao gồm quay về start)
    distances : Dict
        Distance matrix
    max_iterations : int
        Giới hạn số lần lặp

    Returns:
    --------
    Tuple[List[str], float]
        (improved_tour, improved_distance)
    """
    improved = True
    iteration = 0
    best_tour = tour[:]
    best_distance = calculate_tour_distance(best_tour, distances)

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        for i in range(1, len(best_tour) - 2):
            for j in range(i + 1, len(best_tour) - 1):
                # Current edges: (tour[i-1], tour[i]) and (tour[j], tour[j+1])
                # New edges: (tour[i-1], tour[j]) and (tour[i], tour[j+1])

                # Calculate change in distance
                old_edge_1 = (best_tour[i-1], best_tour[i])
                old_edge_2 = (best_tour[j], best_tour[j+1])
                new_edge_1 = (best_tour[i-1], best_tour[j])
                new_edge_2 = (best_tour[i], best_tour[j+1])

                old_dist = (distances.get(old_edge_1, distances.get((old_edge_1[1], old_edge_1[0]), 0)) +
                           distances.get(old_edge_2, distances.get((old_edge_2[1], old_edge_2[0]), 0)))
                new_dist = (distances.get(new_edge_1, distances.get((new_edge_1[1], new_edge_1[0]), 0)) +
                           distances.get(new_edge_2, distances.get((new_edge_2[1], new_edge_2[0]), 0)))

                if new_dist < old_dist:
                    # Perform 2-opt swap: reverse tour[i:j+1]
                    best_tour[i:j+1] = reversed(best_tour[i:j+1])
                    best_distance = calculate_tour_distance(best_tour, distances)
                    improved = True
                    break

            if improved:
                break

    return best_tour, best_distance


def random_tour(cities: Dict, start_city: str = None) -> List[str]:
    """
    Tạo tour ngẫu nhiên.

    Parameters:
    -----------
    cities : Dict
        Cities data
    start_city : str, optional
        Starting city (nếu None thì random)

    Returns:
    --------
    List[str]
        Random tour
    """
    city_list = list(cities.keys())

    if start_city is None:
        start_city = np.random.choice(city_list)

    remaining = [c for c in city_list if c != start_city]
    np.random.shuffle(remaining)

    tour = [start_city] + remaining + [start_city]
    return tour


def calculate_distance_matrix(cities: Dict) -> Dict[Tuple[str, str], float]:
    """
    Tính ma trận khoảng cách cho tất cả cặp cities.

    Parameters:
    -----------
    cities : Dict
        Cities data với coordinates

    Returns:
    --------
    Dict[Tuple[str, str], float]
        Distance matrix {(city_a, city_b): distance_km}
    """
    distances = {}
    city_list = list(cities.keys())

    for i, city_a in enumerate(city_list):
        for city_b in city_list[i+1:]:
            dist = haversine_distance(
                cities[city_a]['lat'], cities[city_a]['lon'],
                cities[city_b]['lat'], cities[city_b]['lon']
            )
            distances[(city_a, city_b)] = dist
            distances[(city_b, city_a)] = dist  # Symmetric

    return distances


def get_city_info_summary(cities: Dict) -> str:
    """
    Tạo summary string cho cities dataset.
    """
    countries = {}
    for city, data in cities.items():
        country = data.get('country', 'Unknown')
        countries[country] = countries.get(country, 0) + 1

    summary = f"Total cities: {len(cities)}\n"
    summary += f"Countries: {len(countries)}\n"
    summary += "Cities per country:\n"
    for country, count in sorted(countries.items(), key=lambda x: -x[1]):
        summary += f"  {country}: {count}\n"

    return summary
