"""
Example with sparse graph - nhiều nodes phân bố rời rạc để dễ visualize.
Tạo đồ thị với các clusters và connections rõ ràng.
"""

import sys
import os

# Add parent directory to path to import src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
import matplotlib.pyplot as plt
from src.aco import AntColony
from src.visualization import plot_graph, plot_convergence


def create_sparse_graph():
    """
    Tạo đồ thị phân bố rời rạc với 15 nodes chia thành các clusters.

    Cấu trúc:
    - Cluster A (top-left): nodes 0-4
    - Cluster B (top-right): nodes 5-9
    - Cluster C (bottom): nodes 10-14
    - Connections giữa các clusters
    """
    G = nx.Graph()

    # ==========================================
    # Cluster A (top-left) - nodes 0-4
    # ==========================================
    cluster_a_edges = [
        (0, 1, 3.0),
        (0, 2, 4.0),
        (1, 3, 2.0),
        (2, 3, 3.5),
        (3, 4, 2.5),
    ]

    # ==========================================
    # Cluster B (top-right) - nodes 5-9
    # ==========================================
    cluster_b_edges = [
        (5, 6, 2.5),
        (5, 7, 3.0),
        (6, 8, 2.0),
        (7, 8, 3.5),
        (8, 9, 2.5),
    ]

    # ==========================================
    # Cluster C (bottom) - nodes 10-14
    # ==========================================
    cluster_c_edges = [
        (10, 11, 3.0),
        (10, 12, 4.0),
        (11, 13, 2.5),
        (12, 13, 3.0),
        (13, 14, 2.0),
    ]

    # ==========================================
    # Inter-cluster connections
    # ==========================================
    # A to B
    inter_cluster_edges = [
        (4, 5, 8.0),    # A -> B
        (2, 7, 9.0),    # A -> B (alternative)

        # A to C
        (0, 10, 10.0),  # A -> C
        (4, 12, 7.0),   # A -> C (alternative)

        # B to C
        (9, 14, 6.0),   # B -> C
        (6, 11, 8.5),   # B -> C (alternative)
    ]

    # Add all edges
    all_edges = cluster_a_edges + cluster_b_edges + cluster_c_edges + inter_cluster_edges
    for u, v, weight in all_edges:
        G.add_edge(u, v, weight=weight)

    # ==========================================
    # Set positions manually for better visualization
    # ==========================================
    pos = {
        # Cluster A (top-left)
        0: (0, 10),
        1: (2, 11),
        2: (1, 9),
        3: (3, 9),
        4: (4, 10),

        # Cluster B (top-right)
        5: (10, 10),
        6: (12, 11),
        7: (11, 9),
        8: (13, 9),
        9: (14, 10),

        # Cluster C (bottom)
        10: (3, 2),
        11: (5, 3),
        12: (6, 1),
        13: (8, 2),
        14: (10, 3),
    }

    return G, pos


def plot_sparse_graph(G, pos, path=None, title="Sparse Graph"):
    """
    Vẽ sparse graph với positions được định sẵn.
    """
    plt.figure(figsize=(14, 10))

    # Định nghĩa màu cho các clusters
    node_colors = []
    for node in G.nodes():
        if node <= 4:
            node_colors.append('lightcoral')    # Cluster A
        elif node <= 9:
            node_colors.append('lightblue')     # Cluster B
        else:
            node_colors.append('lightgreen')    # Cluster C

    # Vẽ tất cả các edges (màu xám)
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        width=1.5,
        alpha=0.5
    )

    # Vẽ edges trong path (màu đỏ, đậm hơn)
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color='red',
            width=4,
            alpha=0.8
        )

    # Vẽ nodes với màu theo cluster
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=700,
        edgecolors='black',
        linewidths=2.5
    )

    # Highlight start và end nodes nếu có path
    if path:
        # Start node (màu xanh đậm)
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[0]],
            node_color='darkgreen',
            node_size=700,
            edgecolors='black',
            linewidths=3
        )
        # End node (màu đỏ đậm)
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[-1]],
            node_color='darkred',
            node_size=700,
            edgecolors='black',
            linewidths=3
        )

    # Vẽ labels cho nodes (lớn hơn)
    nx.draw_networkx_labels(
        G, pos,
        font_size=14,
        font_weight='bold',
        font_color='white'
    )

    # Vẽ trọng số trên các edges
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
    )

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightcoral', edgecolor='black', label='Cluster A (0-4)'),
        Patch(facecolor='lightblue', edgecolor='black', label='Cluster B (5-9)'),
        Patch(facecolor='lightgreen', edgecolor='black', label='Cluster C (10-14)'),
    ]
    if path:
        legend_elements.extend([
            Patch(facecolor='darkgreen', edgecolor='black', label=f'Start ({path[0]})'),
            Patch(facecolor='darkred', edgecolor='black', label=f'End ({path[-1]})'),
        ])
    plt.legend(handles=legend_elements, loc='upper right', fontsize=11)

    plt.title(title, fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 70)
    print("ACO Algorithm - Sparse Graph Example (15 nodes, 3 clusters)")
    print("=" * 70)

    # Tạo đồ thị
    print("\nCreating sparse graph with 3 clusters...")
    G, pos = create_sparse_graph()
    print(f"Graph created:")
    print(f"  - Nodes: {G.number_of_nodes()}")
    print(f"  - Edges: {G.number_of_edges()}")
    print(f"  - Cluster A (red): nodes 0-4")
    print(f"  - Cluster B (blue): nodes 5-9")
    print(f"  - Cluster C (green): nodes 10-14")

    # Visualize đồ thị ban đầu
    print("\nVisualizing sparse graph structure...")
    plot_sparse_graph(G, pos, title="Sparse Graph - 3 Clusters (15 nodes)")

    # Test case 1: Cross-cluster path (A to C)
    print("\n" + "=" * 70)
    print("TEST 1: Cross-cluster path (Cluster A to Cluster C)")
    print("=" * 70)

    start_node = 0  # Cluster A
    end_node = 14   # Cluster C

    print(f"\nFinding path from node {start_node} (Cluster A) to node {end_node} (Cluster C)...")

    # Khởi tạo ACO
    aco1 = AntColony(
        graph=G,
        n_ants=25,
        n_iterations=80,
        alpha=1.0,
        beta=2.5,
        evaporation_rate=0.5,
        Q=100
    )

    # Chạy thuật toán
    best_path1, best_distance1, history1 = aco1.run(start_node, end_node)

    # So sánh với NetworkX
    nx_path1 = nx.shortest_path(G, start_node, end_node, weight='weight')
    nx_distance1 = nx.shortest_path_length(G, start_node, end_node, weight='weight')

    print("\n" + "-" * 70)
    print("RESULTS - Test 1:")
    print("-" * 70)
    print(f"ACO path:     {' -> '.join(map(str, best_path1))}")
    print(f"ACO distance: {best_distance1:.2f}")
    print(f"\nOptimal path: {' -> '.join(map(str, nx_path1))}")
    print(f"Optimal dist: {nx_distance1:.2f}")

    if best_distance1 == nx_distance1:
        print("\n✓ ACO found the optimal path!")
    else:
        error = ((best_distance1 - nx_distance1) / nx_distance1) * 100
        print(f"\n⚠ ACO path is {error:.2f}% longer than optimal")

    # Visualize solution
    print("\nVisualizing ACO solution for Test 1...")
    plot_sparse_graph(
        G, pos,
        path=best_path1,
        title=f"ACO Solution: {start_node}→{end_node} (Distance: {best_distance1:.2f})"
    )

    # Test case 2: Another cross-cluster path (B to A)
    print("\n" + "=" * 70)
    print("TEST 2: Cross-cluster path (Cluster B to Cluster A)")
    print("=" * 70)

    start_node = 9  # Cluster B
    end_node = 0    # Cluster A

    print(f"\nFinding path from node {start_node} (Cluster B) to node {end_node} (Cluster A)...")

    # Khởi tạo ACO
    aco2 = AntColony(
        graph=G,
        n_ants=25,
        n_iterations=80,
        alpha=1.0,
        beta=2.5,
        evaporation_rate=0.5,
        Q=100
    )

    # Chạy thuật toán
    best_path2, best_distance2, history2 = aco2.run(start_node, end_node)

    # So sánh với NetworkX
    nx_path2 = nx.shortest_path(G, start_node, end_node, weight='weight')
    nx_distance2 = nx.shortest_path_length(G, start_node, end_node, weight='weight')

    print("\n" + "-" * 70)
    print("RESULTS - Test 2:")
    print("-" * 70)
    print(f"ACO path:     {' -> '.join(map(str, best_path2))}")
    print(f"ACO distance: {best_distance2:.2f}")
    print(f"\nOptimal path: {' -> '.join(map(str, nx_path2))}")
    print(f"Optimal dist: {nx_distance2:.2f}")

    if best_distance2 == nx_distance2:
        print("\n✓ ACO found the optimal path!")
    else:
        error = ((best_distance2 - nx_distance2) / nx_distance2) * 100
        print(f"\n⚠ ACO path is {error:.2f}% longer than optimal")

    # Visualize solution
    print("\nVisualizing ACO solution for Test 2...")
    plot_sparse_graph(
        G, pos,
        path=best_path2,
        title=f"ACO Solution: {start_node}→{end_node} (Distance: {best_distance2:.2f})"
    )

    # Visualize convergence comparison
    print("\nVisualizing convergence comparison...")
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(history1) + 1), history1, 'b-', linewidth=2)
    plt.xlabel('Iteration', fontsize=12, fontweight='bold')
    plt.ylabel('Best Distance', fontsize=12, fontweight='bold')
    plt.title(f'Test 1: {best_path1[0]}→{best_path1[-1]}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(history2) + 1), history2, 'r-', linewidth=2)
    plt.xlabel('Iteration', fontsize=12, fontweight='bold')
    plt.ylabel('Best Distance', fontsize=12, fontweight='bold')
    plt.title(f'Test 2: {best_path2[0]}→{best_path2[-1]}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Test 1 ({best_path1[0]}→{best_path1[-1]}): Distance = {best_distance1:.2f}, Optimal = {nx_distance1:.2f}")
    print(f"Test 2 ({best_path2[0]}→{best_path2[-1]}): Distance = {best_distance2:.2f}, Optimal = {nx_distance2:.2f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
