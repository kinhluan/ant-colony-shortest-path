"""
Ant Colony Optimization Algorithm for Shortest Path Problem
"""

import numpy as np
import networkx as nx
from typing import List, Tuple, Dict, Set


class AntColony:
    """
    Ant Colony Optimization algorithm for finding shortest path in a graph.

    Parameters:
    -----------
    graph : networkx.Graph
        The graph with weighted edges (use 'weight' attribute)
    n_ants : int
        Number of ants per iteration (default: 20)
    n_iterations : int
        Number of iterations to run (default: 100, recommended: 50-200)
    alpha : float
        Pheromone importance factor (default: 1.0)
    beta : float
        Heuristic importance factor (default: 2.0)
    evaporation_rate : float
        Pheromone evaporation rate, range [0,1] (default: 0.5)
    Q : float
        Constant for pheromone update (default: 100)
    """

    def __init__(
        self,
        graph: nx.Graph,
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation_rate: float = 0.5,
        Q: float = 100
    ):
        self.graph = graph
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q

        # Khởi tạo ma trận pheromone
        # Dict {(u, v): pheromone_value}
        self.pheromone = {}
        for u, v in self.graph.edges():
            self.pheromone[(u, v)] = 1.0
            self.pheromone[(v, u)] = 1.0  # Undirected graph

        # Khởi tạo ma trận heuristic (1/distance)
        # Dict {(u, v): heuristic_value}
        self.heuristic = {}
        for u, v, data in self.graph.edges(data=True):
            weight = data.get('weight', 1.0)
            if weight > 0:
                heuristic_value = 1.0 / weight
            else:
                heuristic_value = 1.0
            self.heuristic[(u, v)] = heuristic_value
            self.heuristic[(v, u)] = heuristic_value  # Undirected graph

    def _calculate_probabilities(
        self,
        current_node: int,
        unvisited: Set[int]
    ) -> Dict[int, float]:
        """
        Tính xác suất chọn nút tiếp theo dựa trên pheromone và heuristic.

        Công thức: P(i,j) = [τ(i,j)^α * η(i,j)^β] / Σ[τ(i,k)^α * η(i,k)^β]
        trong đó:
        - τ(i,j): pheromone trên cạnh (i,j)
        - η(i,j): heuristic = 1/distance(i,j)
        - α, β: trọng số

        Parameters:
        -----------
        current_node : int
            Nút hiện tại
        unvisited : Set[int]
            Tập các nút chưa thăm

        Returns:
        --------
        Dict[int, float]
            Dictionary {node: probability}
        """
        probabilities = {}
        attractiveness = {}

        # Tính attractiveness cho mỗi nút có thể đến được
        for next_node in unvisited:
            if self.graph.has_edge(current_node, next_node):
                edge = (current_node, next_node)
                tau = self.pheromone.get(edge, 1.0)
                eta = self.heuristic.get(edge, 1.0)

                # attractiveness = τ^α * η^β
                attractiveness[next_node] = (tau ** self.alpha) * (eta ** self.beta)

        # Nếu không có nút nào có thể đến, return empty dict
        if not attractiveness:
            return {}

        # Chuẩn hóa thành xác suất
        total = sum(attractiveness.values())
        for node, attr in attractiveness.items():
            probabilities[node] = attr / total

        return probabilities

    def _select_next_node(self, probabilities: Dict[int, float]) -> int:
        """
        Chọn nút tiếp theo dựa trên xác suất.

        Parameters:
        -----------
        probabilities : Dict[int, float]
            Dictionary {node: probability}

        Returns:
        --------
        int
            Nút được chọn
        """
        if not probabilities:
            return None

        nodes = list(probabilities.keys())
        probs = list(probabilities.values())

        # Chọn ngẫu nhiên theo xác suất
        selected = np.random.choice(nodes, p=probs)
        return selected

    def _construct_solution(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Xây dựng một giải pháp (đường đi) cho một con kiến.

        Parameters:
        -----------
        start : int
            Nút bắt đầu
        end : int
            Nút đích

        Returns:
        --------
        Tuple[List[int], float]
            (path, total_distance)
            - path: Danh sách các nút trong đường đi
            - total_distance: Tổng khoảng cách của đường đi
        """
        path = [start]
        current = start
        unvisited = set(self.graph.nodes()) - {start}
        total_distance = 0.0

        # Di chuyển cho đến khi đến đích
        while current != end and unvisited:
            # Tính xác suất cho các nút tiếp theo
            probabilities = self._calculate_probabilities(current, unvisited)

            # Nếu không có đường đi nào, break
            if not probabilities:
                # Thử tìm đường đi ngắn nhất còn lại (fallback)
                if end in unvisited and nx.has_path(self.graph, current, end):
                    try:
                        shortest = nx.shortest_path(self.graph, current, end, weight='weight')
                        for node in shortest[1:]:
                            path.append(node)
                            edge_data = self.graph[current][node]
                            total_distance += edge_data.get('weight', 1.0)
                            current = node
                    except nx.NetworkXNoPath:
                        break
                break

            # Chọn nút tiếp theo
            next_node = self._select_next_node(probabilities)

            # Cập nhật đường đi
            path.append(next_node)
            edge_data = self.graph[current][next_node]
            total_distance += edge_data.get('weight', 1.0)

            # Di chuyển đến nút tiếp theo
            unvisited.remove(next_node)
            current = next_node

        # Nếu không đến được đích, trả về đường đi vô cực
        if current != end:
            return (path, float('inf'))

        return (path, total_distance)

    def _update_pheromone(self, all_paths: List[Tuple[List[int], float]]):
        """
        Cập nhật pheromone sau mỗi vòng lặp.

        Công thức:
        1. Bay hơi: τ(i,j) = (1 - ρ) * τ(i,j)
        2. Cập nhật: τ(i,j) = τ(i,j) + Σ(Q / L_k)
           trong đó L_k là độ dài đường đi của kiến k đi qua cạnh (i,j)

        Parameters:
        -----------
        all_paths : List[Tuple[List[int], float]]
            Danh sách các (path, distance) của tất cả kiến
        """
        # Bước 1: Bay hơi pheromone
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.evaporation_rate)

        # Bước 2: Cập nhật pheromone từ các đường đi
        for path, distance in all_paths:
            # Bỏ qua đường đi không hợp lệ
            if distance == float('inf') or distance <= 0:
                continue

            # Lượng pheromone thêm vào
            delta_pheromone = self.Q / distance

            # Cập nhật cho mỗi cạnh trong đường đi
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]

                # Cập nhật cả hai chiều (undirected graph)
                if (u, v) in self.pheromone:
                    self.pheromone[(u, v)] += delta_pheromone
                if (v, u) in self.pheromone:
                    self.pheromone[(v, u)] += delta_pheromone

    def run(self, start: int, end: int) -> Tuple[List[int], float, List[float]]:
        """
        Chạy thuật toán ACO để tìm đường đi ngắn nhất.

        Parameters:
        -----------
        start : int
            Nút bắt đầu
        end : int
            Nút đích

        Returns:
        --------
        Tuple[List[int], float, List[float]]
            (best_path, best_distance, history)
            - best_path: Đường đi ngắn nhất tìm được
            - best_distance: Độ dài đường đi ngắn nhất
            - history: Lịch sử best_distance qua các iterations
        """
        best_path = None
        best_distance = float('inf')
        history = []

        print(f"Starting ACO algorithm...")
        print(f"Parameters: n_ants={self.n_ants}, n_iterations={self.n_iterations}")
        print(f"            alpha={self.alpha}, beta={self.beta}")
        print(f"            evaporation_rate={self.evaporation_rate}, Q={self.Q}")
        print(f"Finding shortest path from {start} to {end}...\n")

        # Chạy thuật toán
        for iteration in range(self.n_iterations):
            all_paths = []

            # Mỗi kiến xây dựng một giải pháp
            for ant in range(self.n_ants):
                path, distance = self._construct_solution(start, end)
                all_paths.append((path, distance))

                # Cập nhật best solution
                if distance < best_distance:
                    best_path = path
                    best_distance = distance

            # Cập nhật pheromone
            self._update_pheromone(all_paths)

            # Lưu lịch sử
            history.append(best_distance)

            # In tiến trình
            if (iteration + 1) % 10 == 0 or iteration == 0:
                print(f"Iteration {iteration + 1}/{self.n_iterations}: "
                      f"Best distance = {best_distance:.2f}")

        print(f"\nAlgorithm completed!")
        print(f"Best path found: {best_path}")
        print(f"Best distance: {best_distance:.2f}")

        return best_path, best_distance, history
