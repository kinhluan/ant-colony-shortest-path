"""
Complex example of ACO algorithm with large graph (100 nodes) and parameter tuning.
Nodes are distributed evenly in grid pattern with some randomness.
Compares different parameter settings and benchmarks performance.
"""

import sys
import os
import time

# Add parent directory to path to import src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from src.aco import AntColony
from src.visualization import plot_convergence, plot_comparison


def create_complex_graph(n_nodes=100, seed=42):
    """
    Tạo đồ thị phức tạp với 100 nodes phân bố đều theo grid pattern.

    Parameters:
    -----------
    n_nodes : int
        Số lượng nodes trong đồ thị (default: 100)
    seed : int
        Random seed để tái tạo đồ thị

    Returns:
    --------
    G : networkx.Graph
        Đồ thị được tạo
    pos : dict
        Positions của các nodes (để vẽ)
    """
    np.random.seed(seed)
    G = nx.Graph()

    # Tạo grid layout đều
    grid_size = int(np.ceil(np.sqrt(n_nodes)))
    pos = {}

    node_id = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if node_id >= n_nodes:
                break

            # Vị trí grid cơ bản
            x = j * 10
            y = i * 10

            # Thêm random offset nhỏ để không quá đều
            x += np.random.uniform(-1.5, 1.5)
            y += np.random.uniform(-1.5, 1.5)

            pos[node_id] = (x, y)
            G.add_node(node_id)
            node_id += 1

        if node_id >= n_nodes:
            break

    # Tạo edges dựa trên khoảng cách
    # Connect nodes trong radius để tạo mesh network
    connection_radius = 15.0  # Điều chỉnh để có density hợp lý

    for node_a in G.nodes():
        for node_b in G.nodes():
            if node_a >= node_b:
                continue

            # Tính khoảng cách Euclidean
            dist = np.linalg.norm(
                np.array(pos[node_a]) - np.array(pos[node_b])
            )

            # Kết nối nếu trong radius
            if dist <= connection_radius:
                # Trọng số = khoảng cách + random factor
                weight = dist * np.random.uniform(0.8, 1.2)
                G.add_edge(node_a, node_b, weight=weight)

    # Đảm bảo đồ thị liên thông
    if not nx.is_connected(G):
        print("  Graph not connected, adding bridge edges...")
        components = list(nx.connected_components(G))
        print(f"  Found {len(components)} components")

        for i in range(len(components) - 1):
            # Tìm 2 nodes gần nhất giữa 2 components
            comp_a = list(components[i])
            comp_b = list(components[i + 1])

            min_dist = float('inf')
            bridge_nodes = None

            for node_a in comp_a:
                for node_b in comp_b:
                    dist = np.linalg.norm(
                        np.array(pos[node_a]) - np.array(pos[node_b])
                    )
                    if dist < min_dist:
                        min_dist = dist
                        bridge_nodes = (node_a, node_b)

            # Thêm bridge edge
            if bridge_nodes:
                weight = min_dist * np.random.uniform(0.8, 1.2)
                G.add_edge(bridge_nodes[0], bridge_nodes[1], weight=weight)
                print(f"  Added bridge: {bridge_nodes[0]} <-> {bridge_nodes[1]}")

    return G, pos


def plot_complex_graph(G, pos, path=None, title="Complex Graph"):
    """
    Vẽ đồ thị lớn với 100 nodes.
    """
    plt.figure(figsize=(16, 16))

    # Vẽ edges (mờ hơn vì nhiều)
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        width=0.5,
        alpha=0.2
    )

    # Vẽ path edges nếu có
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color='red',
            width=3,
            alpha=0.9
        )

    # Vẽ nodes (nhỏ hơn vì nhiều)
    nx.draw_networkx_nodes(
        G, pos,
        node_color='lightblue',
        node_size=100,
        edgecolors='black',
        linewidths=0.5,
        alpha=0.7
    )

    # Highlight start và end nếu có path
    if path:
        # Start node
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[0]],
            node_color='green',
            node_size=400,
            edgecolors='darkgreen',
            linewidths=3
        )
        # End node
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[-1]],
            node_color='red',
            node_size=400,
            edgecolors='darkred',
            linewidths=3
        )

        # Labels cho start/end only
        labels = {
            path[0]: f"START\n{path[0]}",
            path[-1]: f"END\n{path[-1]}"
        }
        nx.draw_networkx_labels(
            G, pos,
            labels=labels,
            font_size=10,
            font_weight='bold'
        )

    plt.title(title, fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def run_aco_with_params(G, start, end, params, label):
    """
    Chạy ACO với một bộ tham số cụ thể.
    """
    print(f"\n{label}")
    print("-" * 70)

    aco = AntColony(G, **params)

    start_time = time.time()
    best_path, best_distance, history = aco.run(start, end)
    execution_time = time.time() - start_time

    print(f"Execution time: {execution_time:.2f} seconds")

    return best_path, best_distance, history, execution_time


def main():
    print("=" * 70)
    print("ACO Algorithm - Complex Example (100 Nodes)")
    print("=" * 70)

    # Tạo đồ thị phức tạp
    print("\nCreating complex graph with evenly distributed nodes...")
    n_nodes = 100
    G, pos = create_complex_graph(n_nodes=n_nodes, seed=42)

    print(f"\nGraph Statistics:")
    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    print(f"  Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    print(f"  Density: {nx.density(G):.4f}")
    print(f"  Is connected: {nx.is_connected(G)}")

    # Visualize đồ thị
    print("\nVisualizing graph structure...")
    plot_complex_graph(G, pos, title=f"Complex Graph - {n_nodes} Nodes (Grid Layout)")

    # Chọn start và end nodes (xa nhau)
    start_node = 0
    end_node = n_nodes - 1

    # Tính shortest path với NetworkX để so sánh
    print(f"\n{'='*70}")
    print("Calculating optimal path with Dijkstra...")
    print('='*70)
    optimal_path = nx.shortest_path(G, start_node, end_node, weight='weight')
    optimal_distance = nx.shortest_path_length(G, start_node, end_node, weight='weight')
    print(f"Optimal distance: {optimal_distance:.2f}")
    print(f"Optimal path length: {len(optimal_path)} nodes")

    # Test 1: Default parameters
    params1 = {
        'n_ants': 30,
        'n_iterations': 150,
        'alpha': 1.0,
        'beta': 2.0,
        'evaporation_rate': 0.5,
        'Q': 100
    }
    path1, dist1, hist1, time1 = run_aco_with_params(
        G, start_node, end_node, params1,
        "Test 1: Default Parameters (30 ants, 150 iterations)"
    )

    # Test 2: More ants
    params2 = {
        'n_ants': 50,
        'n_iterations': 150,
        'alpha': 1.0,
        'beta': 2.0,
        'evaporation_rate': 0.5,
        'Q': 100
    }
    path2, dist2, hist2, time2 = run_aco_with_params(
        G, start_node, end_node, params2,
        "Test 2: More Ants (50 ants)"
    )

    # Test 3: Higher beta (greedy - more emphasis on heuristic)
    params3 = {
        'n_ants': 30,
        'n_iterations': 150,
        'alpha': 1.0,
        'beta': 4.0,
        'evaporation_rate': 0.5,
        'Q': 100
    }
    path3, dist3, hist3, time3 = run_aco_with_params(
        G, start_node, end_node, params3,
        "Test 3: Higher Beta (4.0 - more greedy)"
    )

    # Test 4: Lower evaporation rate
    params4 = {
        'n_ants': 30,
        'n_iterations': 150,
        'alpha': 1.0,
        'beta': 2.0,
        'evaporation_rate': 0.3,
        'Q': 100
    }
    path4, dist4, hist4, time4 = run_aco_with_params(
        G, start_node, end_node, params4,
        "Test 4: Lower Evaporation (0.3 - pheromone persists longer)"
    )

    # Test 5: More iterations
    params5 = {
        'n_ants': 30,
        'n_iterations': 250,
        'alpha': 1.0,
        'beta': 2.0,
        'evaporation_rate': 0.5,
        'Q': 100
    }
    path5, dist5, hist5, time5 = run_aco_with_params(
        G, start_node, end_node, params5,
        "Test 5: More Iterations (250)"
    )

    # Tổng hợp kết quả
    print("\n" + "=" * 70)
    print("COMPARISON OF RESULTS")
    print("=" * 70)

    results = [
        ("Optimal (Dijkstra)", optimal_distance, None, None),
        ("Test 1 (Default)", dist1, time1, path1),
        ("Test 2 (More Ants)", dist2, time2, path2),
        ("Test 3 (High Beta)", dist3, time3, path3),
        ("Test 4 (Low Evap)", dist4, time4, path4),
        ("Test 5 (More Iter)", dist5, time5, path5),
    ]

    print(f"\n{'Test':<30} {'Distance':<12} {'Time (s)':<12} {'Error %':<10}")
    print("-" * 70)

    for name, distance, exec_time, path in results:
        if exec_time is not None:
            error = ((distance - optimal_distance) / optimal_distance) * 100
            print(f"{name:<30} {distance:<12.2f} {exec_time:<12.2f} {error:<10.2f}")
        else:
            print(f"{name:<30} {distance:<12.2f} {'-':<12} {'-':<10}")

    # Tìm kết quả tốt nhất
    print("\n" + "=" * 70)
    aco_results = [
        (dist1, "Test 1", path1),
        (dist2, "Test 2", path2),
        (dist3, "Test 3", path3),
        (dist4, "Test 4", path4),
        (dist5, "Test 5", path5),
    ]
    best_aco = min(aco_results, key=lambda x: x[0])

    print(f"Best ACO result: {best_aco[1]}")
    print(f"Distance: {best_aco[0]:.2f}")
    print(f"Path length: {len(best_aco[2])} nodes")

    if best_aco[0] == optimal_distance:
        print("\n✓ Best ACO result found the optimal path!")
    else:
        error = ((best_aco[0] - optimal_distance) / optimal_distance) * 100
        print(f"\n⚠ Best ACO result is {error:.2f}% longer than optimal")

    # Visualize best path
    print("\nVisualizing best ACO solution...")
    plot_complex_graph(
        G, pos,
        path=best_aco[2],
        title=f"Best ACO Path - {best_aco[1]} (Distance: {best_aco[0]:.2f})"
    )

    # Visualize optimal path
    print("\nVisualizing optimal solution...")
    plot_complex_graph(
        G, pos,
        path=optimal_path,
        title=f"Optimal Path - Dijkstra (Distance: {optimal_distance:.2f})"
    )

    # So sánh convergence của các tests
    print("\nVisualizing convergence comparison...")
    histories = {
        "Test 1 (Default)": hist1,
        "Test 2 (More Ants)": hist2,
        "Test 3 (High Beta)": hist3,
        "Test 4 (Low Evap)": hist4,
        "Test 5 (More Iter)": hist5,
    }
    plot_comparison(
        histories,
        title="ACO Convergence Comparison - 100 Nodes"
    )

    # Detailed convergence for best result
    print("\nVisualizing detailed convergence for best result...")
    best_idx = aco_results.index(best_aco)
    best_hist = [hist1, hist2, hist3, hist4, hist5][best_idx]
    plot_convergence(
        best_hist,
        title=f"Detailed Convergence - {best_aco[1]}"
    )

    # Statistics
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    print(f"Graph size: {n_nodes} nodes, {G.number_of_edges()} edges")
    print(f"Optimal path: {len(optimal_path)} nodes, distance: {optimal_distance:.2f}")
    print(f"Best ACO path: {len(best_aco[2])} nodes, distance: {best_aco[0]:.2f}")
    print(f"Average ACO distance: {np.mean([dist1, dist2, dist3, dist4, dist5]):.2f}")
    print(f"Best ACO found by: {best_aco[1]}")

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
