"""
Visualization utilities for ACO algorithm
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional


def plot_graph(
    G: nx.Graph,
    path: Optional[List[int]] = None,
    title: str = "Graph",
    figsize: tuple = (10, 8),
    node_size: int = 500,
    save_path: Optional[str] = None
):
    """
    Vẽ đồ thị NetworkX với tùy chọn highlight đường đi.

    Parameters:
    -----------
    G : networkx.Graph
        Đồ thị cần vẽ
    path : List[int], optional
        Đường đi cần highlight (màu đỏ)
    title : str
        Tiêu đề của biểu đồ
    figsize : tuple
        Kích thước figure (width, height)
    node_size : int
        Kích thước của nodes
    save_path : str, optional
        Đường dẫn để lưu hình ảnh
    """
    plt.figure(figsize=figsize)

    # Tạo layout cho đồ thị
    pos = nx.spring_layout(G, seed=42)

    # Vẽ tất cả các edges (màu xám)
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        width=1,
        alpha=0.5
    )

    # Vẽ edges trong path (màu đỏ, đậm hơn)
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color='red',
            width=3,
            alpha=0.8
        )

    # Vẽ nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color='lightblue',
        node_size=node_size,
        edgecolors='black',
        linewidths=2
    )

    # Highlight start và end nodes nếu có path
    if path:
        # Start node (màu xanh lá)
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[0]],
            node_color='green',
            node_size=node_size,
            edgecolors='black',
            linewidths=2
        )
        # End node (màu đỏ)
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[path[-1]],
            node_color='red',
            node_size=node_size,
            edgecolors='black',
            linewidths=2
        )

    # Vẽ labels cho nodes
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold'
    )

    # Vẽ trọng số trên các edges
    edge_labels = nx.get_edge_attributes(G, 'weight')
    # Format edge labels to 1 decimal place
    edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=10
    )

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to {save_path}")

    plt.show()


def plot_convergence(
    history: List[float],
    title: str = "ACO Convergence",
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None
):
    """
    Vẽ biểu đồ hội tụ của thuật toán ACO.

    Parameters:
    -----------
    history : List[float]
        Lịch sử best_distance qua các iterations
    title : str
        Tiêu đề của biểu đồ
    figsize : tuple
        Kích thước figure (width, height)
    save_path : str, optional
        Đường dẫn để lưu hình ảnh
    """
    plt.figure(figsize=figsize)

    iterations = range(1, len(history) + 1)
    plt.plot(iterations, history, 'b-', linewidth=2, label='Best Distance')

    plt.xlabel('Iteration', fontsize=12, fontweight='bold')
    plt.ylabel('Best Distance Found', fontsize=12, fontweight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Thêm annotation cho giá trị cuối cùng
    final_value = history[-1]
    plt.annotate(
        f'Final: {final_value:.2f}',
        xy=(len(history), final_value),
        xytext=(len(history) * 0.7, final_value * 1.1),
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3')
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Convergence plot saved to {save_path}")

    plt.show()


def plot_comparison(
    histories: dict,
    title: str = "ACO Algorithm Comparison",
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
):
    """
    So sánh nhiều lần chạy thuật toán ACO với các tham số khác nhau.

    Parameters:
    -----------
    histories : dict
        Dictionary {label: history_list}
        Ví dụ: {'Alpha=1.0': [10, 9, 8, ...], 'Alpha=2.0': [12, 10, 9, ...]}
    title : str
        Tiêu đề của biểu đồ
    figsize : tuple
        Kích thước figure (width, height)
    save_path : str, optional
        Đường dẫn để lưu hình ảnh
    """
    plt.figure(figsize=figsize)

    for label, history in histories.items():
        iterations = range(1, len(history) + 1)
        plt.plot(iterations, history, linewidth=2, label=label, marker='o', markersize=3)

    plt.xlabel('Iteration', fontsize=12, fontweight='bold')
    plt.ylabel('Best Distance Found', fontsize=12, fontweight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Comparison plot saved to {save_path}")

    plt.show()
