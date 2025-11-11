"""
TSP Example - European Cities Tour with ACO

Demonstrates Ant Colony Optimization for Traveling Salesman Problem.
Features:
- 30 major European cities
- Elitist strategy
- Max-Min Ant System
- 2-opt local search
- Interactive Folium map
- Comparison với nearest neighbor
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tsp_aco import TSP_AntColony
from src.tsp_utils import load_cities, nearest_neighbor_tsp, get_city_info_summary, random_tour, calculate_tour_distance, calculate_distance_matrix
from src.tsp_visualization import plot_tsp_tour, plot_interactive_tour, plot_tsp_comparison, plot_tour_statistics
from src.visualization import plot_convergence


def main():
    print("=" * 80)
    print("TRAVELING SALESMAN PROBLEM - EUROPEAN CITIES TOUR")
    print("=" * 80)
    print("\nUsing Ant Colony Optimization to find the shortest tour")
    print("visiting 30 major European cities\n")

    # Load cities data
    print("Loading European cities data...")
    cities_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'european_cities.json')
    cities = load_cities(cities_path)

    print(f"\n{get_city_info_summary(cities)}")

    # Visualize cities
    print("Visualizing all cities...")
    plot_tsp_tour(cities, list(cities.keys()) + [list(cities.keys())[0]],
                  title="All European Cities (No Optimized Tour)")

    # Choose starting city
    start_city = 'Paris'
    print(f"\nStarting city: {start_city}")

    # ==========================================
    # BENCHMARK: Nearest Neighbor
    # ==========================================
    print("\n" + "=" * 80)
    print("BENCHMARK: Nearest Neighbor Heuristic")
    print("=" * 80)

    start_time = time.time()
    nn_tour, nn_distance = nearest_neighbor_tsp(cities, start_city)
    nn_time = time.time() - start_time

    print(f"\nNearest Neighbor Results:")
    print(f"  Distance: {nn_distance:.2f} km")
    print(f"  Time: {nn_time:.2f} seconds")
    print(f"  Tour: {' → '.join(nn_tour[:5])} ... → {nn_tour[0]}")

    # ==========================================
    # ACO ALGORITHM
    # ==========================================
    print("\n" + "=" * 80)
    print("ANT COLONY OPTIMIZATION")
    print("=" * 80)

    # Initialize ACO
    aco = TSP_AntColony(
        cities=cities,
        n_ants=50,
        n_iterations=200,
        alpha=1.0,
        beta=5.0,  # High beta - emphasis on distance
        evaporation_rate=0.1,  # Low evaporation - pheromone persists
        Q=1000,
        elitist=True,  # Only top 20% ants update pheromone
        elitist_ratio=0.2,
        local_search=True,  # Apply 2-opt improvement
        max_min=True  # Max-Min Ant System
    )

    # Run ACO
    start_time = time.time()
    aco_tour, aco_distance, aco_history = aco.run(start_city=start_city, verbose=True)
    aco_time = time.time() - start_time

    print(f"\nACO Results:")
    print(f"  Distance: {aco_distance:.2f} km")
    print(f"  Time: {aco_time:.2f} seconds")
    print(f"  Tour: {' → '.join(aco_tour[:5])} ... → {aco_tour[0]}")

    # ==========================================
    # COMPARISON
    # ==========================================
    print("\n" + "=" * 80)
    print("RESULTS COMPARISON")
    print("=" * 80)

    improvement = ((nn_distance - aco_distance) / nn_distance) * 100

    print(f"\n{'Method':<25} {'Distance (km)':<15} {'Time (s)':<12} {'Improvement':<12}")
    print("-" * 80)
    print(f"{'Nearest Neighbor':<25} {nn_distance:<15.2f} {nn_time:<12.2f} {'-':<12}")
    print(f"{'ACO (Optimized)':<25} {aco_distance:<15.2f} {aco_time:<12.2f} {improvement:>10.2f}%")

    if aco_distance < nn_distance:
        print(f"\n✓ ACO found a better tour! {improvement:.2f}% improvement over Nearest Neighbor")
    elif aco_distance == nn_distance:
        print(f"\n✓ ACO matched the Nearest Neighbor solution")
    else:
        print(f"\n⚠ Nearest Neighbor performed better (unusual)")

    # ==========================================
    # VISUALIZATIONS
    # ==========================================

    # 1. ACO Tour
    print("\n" + "=" * 80)
    print("VISUALIZATION 1: ACO Tour")
    print("=" * 80)
    plot_tsp_tour(cities, aco_tour,
                  title=f"ACO Tour - Distance: {aco_distance:.2f} km")

    # 2. Nearest Neighbor Tour
    print("\n" + "=" * 80)
    print("VISUALIZATION 2: Nearest Neighbor Tour")
    print("=" * 80)
    plot_tsp_tour(cities, nn_tour,
                  title=f"Nearest Neighbor Tour - Distance: {nn_distance:.2f} km")

    # 3. Side-by-side comparison
    print("\n" + "=" * 80)
    print("VISUALIZATION 3: Side-by-Side Comparison")
    print("=" * 80)
    plot_tsp_comparison(
        cities,
        tours={'Nearest Neighbor': nn_tour, 'ACO': aco_tour},
        distances={'Nearest Neighbor': nn_distance, 'ACO': aco_distance},
        title="TSP Tour Comparison"
    )

    # 4. Convergence
    print("\n" + "=" * 80)
    print("VISUALIZATION 4: ACO Convergence")
    print("=" * 80)
    plot_convergence(aco_history, title="ACO Convergence - TSP Europe")

    # 5. Tour statistics
    print("\n" + "=" * 80)
    print("VISUALIZATION 5: Tour Statistics")
    print("=" * 80)
    plot_tour_statistics(cities, aco_tour, aco_distance)

    # 6. Interactive map (Folium)
    print("\n" + "=" * 80)
    print("VISUALIZATION 6: Interactive Map (Folium)")
    print("=" * 80)
    map_path = "tsp_europe_tour.html"
    interactive_map = plot_interactive_tour(cities, aco_tour, aco_distance, save_path=map_path)

    # ==========================================
    # ADVANCED ANALYSIS
    # ==========================================
    print("\n" + "=" * 80)
    print("ADVANCED ANALYSIS")
    print("=" * 80)

    # Test multiple starting cities
    print("\nTesting different starting cities...")
    test_cities = ['Paris', 'London', 'Berlin', 'Rome', 'Madrid']
    start_city_results = {}

    for test_start in test_cities:
        print(f"  Testing from {test_start}...", end=" ")
        aco_test = TSP_AntColony(
            cities=cities,
            n_ants=30,
            n_iterations=100,
            alpha=1.0,
            beta=5.0,
            evaporation_rate=0.1,
            Q=1000,
            elitist=True,
            local_search=True,
            max_min=True
        )
        test_tour, test_dist, _ = aco_test.run(start_city=test_start, verbose=False)
        start_city_results[test_start] = test_dist
        print(f"{test_dist:.2f} km")

    print(f"\nBest starting city: {min(start_city_results, key=start_city_results.get)}")
    print(f"Distance: {min(start_city_results.values()):.2f} km")

    # Random tour comparison
    print("\n" + "=" * 80)
    print("COMPARISON WITH RANDOM TOURS")
    print("=" * 80)

    distances_matrix = calculate_distance_matrix(cities)
    random_distances = []
    for i in range(10):
        rand_tour = random_tour(cities, start_city)
        rand_dist = calculate_tour_distance(rand_tour, distances_matrix)
        random_distances.append(rand_dist)

    avg_random = sum(random_distances) / len(random_distances)
    print(f"\nAverage random tour distance: {avg_random:.2f} km")
    print(f"ACO tour distance: {aco_distance:.2f} km")
    print(f"ACO improvement over random: {((avg_random - aco_distance) / avg_random * 100):.2f}%")

    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nProblem: Visit {len(cities)} European cities in shortest tour")
    print(f"\nSolution Methods:")
    print(f"  1. Nearest Neighbor: {nn_distance:.2f} km")
    print(f"  2. ACO Optimized:    {aco_distance:.2f} km")
    print(f"  3. Random Average:   {avg_random:.2f} km")
    print(f"\nBest Solution: ACO")
    print(f"Improvement over NN: {improvement:.2f}%")
    print(f"Improvement over Random: {((avg_random - aco_distance) / avg_random * 100):.2f}%")

    print(f"\nACO Configuration:")
    print(f"  Ants: {aco.n_ants}, Iterations: {aco.n_iterations}")
    print(f"  Alpha: {aco.alpha}, Beta: {aco.beta}")
    print(f"  Evaporation: {aco.evaporation_rate}")
    print(f"  Elitist: {aco.elitist}, Local Search: {aco.local_search}")
    print(f"  Max-Min AS: {aco.max_min}")

    print(f"\nFinal Tour:")
    for i, city in enumerate(aco_tour[:-1]):
        country = cities[city]['country']
        print(f"  {i+1:2d}. {city:<15} ({country})")

    print(f"\nInteractive map saved to: {map_path}")
    print("Open this file in your browser to explore the tour!")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
