"""
Simple example of ACO algorithm for shortest path finding.
Creates a small graph and finds the shortest path between two nodes.
"""

import sys
import os

# Add parent directory to path to import src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
from src.aco import AntColony
from src.visualization import plot_graph, plot_convergence


def create_simple_graph():
    """
    Tạo một đồ thị đơn giản với 7 nodes.

    Cấu trúc:
        0 --- 1 --- 2
        |     |     |
        3 --- 4 --- 5
              |
              6
    """
    G = nx.Graph()

    # Thêm các cạnh với trọng số
    edges = [
        (0, 1, 2.0),
        (0, 3, 4.0),
        (1, 2, 3.0),
        (1, 4, 1.0),
        (2, 5, 2.0),
        (3, 4, 2.0),
        (4, 5, 3.0),
        (4, 6, 5.0),
    ]

    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    return G


def main():
    print("=" * 60)
    print("ACO Algorithm - Simple Example")
    print("=" * 60)

    # Tạo đồ thị
    print("\nCreating graph...")
    G = create_simple_graph()
    print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Visualize đồ thị ban đầu
    print("\nVisualizing graph...")
    plot_graph(G, title="Simple Graph (7 nodes)")

    # Thiết lập start và end nodes
    start_node = 0
    end_node = 6

    # Khởi tạo ACO
    print(f"\nInitializing ACO algorithm...")
    aco = AntColony(
        graph=G,
        n_ants=10,
        n_iterations=50,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.5,
        Q=100
    )

    # Chạy thuật toán
    print("\n" + "=" * 60)
    best_path, best_distance, history = aco.run(start_node, end_node)
    print("=" * 60)

    # Hiển thị kết quả
    print(f"\n{'RESULTS':^60}")
    print("=" * 60)
    print(f"Start node: {start_node}")
    print(f"End node: {end_node}")
    print(f"Best path: {' -> '.join(map(str, best_path))}")
    print(f"Best distance: {best_distance:.2f}")
    print("=" * 60)

    # Visualize đường đi tìm được
    print("\nVisualizing solution...")
    plot_graph(
        G,
        path=best_path,
        title=f"Best Path Found (Distance: {best_distance:.2f})"
    )

    # Visualize convergence
    print("\nVisualizing convergence...")
    plot_convergence(
        history,
        title="ACO Convergence - Simple Example"
    )

    # So sánh với shortest path của NetworkX
    print("\n" + "=" * 60)
    print("COMPARISON WITH DIJKSTRA'S ALGORITHM")
    print("=" * 60)
    nx_shortest = nx.shortest_path(G, start_node, end_node, weight='weight')
    nx_distance = nx.shortest_path_length(G, start_node, end_node, weight='weight')

    print(f"NetworkX shortest path: {' -> '.join(map(str, nx_shortest))}")
    print(f"NetworkX distance: {nx_distance:.2f}")
    print(f"\nACO path: {' -> '.join(map(str, best_path))}")
    print(f"ACO distance: {best_distance:.2f}")

    if best_distance == nx_distance:
        print("\n✓ ACO found the optimal path!")
    else:
        difference = ((best_distance - nx_distance) / nx_distance) * 100
        print(f"\n⚠ ACO path is {difference:.2f}% longer than optimal")

    print("=" * 60)


if __name__ == "__main__":
    main()
