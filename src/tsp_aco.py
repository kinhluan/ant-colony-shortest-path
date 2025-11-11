"""
Ant Colony Optimization for Traveling Salesman Problem (TSP)
"""

import numpy as np
from typing import Dict, List, Tuple, Set
from .tsp_utils import calculate_distance_matrix, calculate_tour_distance, two_opt_improve


class TSP_AntColony:
    """
    ACO algorithm cho Traveling Salesman Problem.

    Khác biệt với shortest path ACO:
    - Đi qua TẤT CẢ cities (không phải subset)
    - Quay lại start city (cycle/tour)
    - Complete graph (mọi city nối mọi city)

    Parameters:
    -----------
    cities : Dict
        Cities data {city_name: {'lat': ..., 'lon': ...}}
    n_ants : int
        Số kiến mỗi vòng lặp
    n_iterations : int
        Số vòng lặp
    alpha : float
        Trọng số pheromone
    beta : float
        Trọng số heuristic (1/distance)
    evaporation_rate : float
        Tỷ lệ bay hơi pheromone [0,1]
    Q : float
        Hằng số cập nhật pheromone
    elitist : bool
        Sử dụng elitist strategy (chỉ top ants update pheromone)
    elitist_ratio : float
        Tỷ lệ ants được coi là elite [0,1]
    local_search : bool
        Sử dụng 2-opt local search để cải thiện tours
    max_min : bool
        Sử dụng Max-Min Ant System (giới hạn pheromone)
    """

    def __init__(
        self,
        cities: Dict,
        n_ants: int = 50,
        n_iterations: int = 200,
        alpha: float = 1.0,
        beta: float = 5.0,  # High beta cho TSP
        evaporation_rate: float = 0.1,  # Low evaporation cho TSP
        Q: float = 1000,
        elitist: bool = True,
        elitist_ratio: float = 0.2,
        local_search: bool = True,
        max_min: bool = True
    ):
        self.cities = cities
        self.city_list = list(cities.keys())
        self.n_cities = len(self.city_list)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        self.elitist = elitist
        self.elitist_ratio = elitist_ratio
        self.local_search = local_search
        self.max_min = max_min

        # Compute distance matrix (complete graph)
        print("Computing distance matrix...")
        self.distances = calculate_distance_matrix(cities)
        print(f"  {len(self.distances)} distances computed")

        # Initialize pheromone matrix
        print("Initializing pheromone...")
        self.pheromone = {}
        self._initialize_pheromone()

        # Heuristic matrix (1/distance)
        self.heuristic = {}
        for edge, dist in self.distances.items():
            if dist > 0:
                self.heuristic[edge] = 1.0 / dist
            else:
                self.heuristic[edge] = 1.0

        # Max-Min bounds (sẽ được cập nhật sau iteration đầu)
        if self.max_min:
            self.tau_max = 1.0
            self.tau_min = 0.01

    def _initialize_pheromone(self):
        """
        Khởi tạo pheromone ban đầu cho tất cả edges.
        """
        for edge in self.distances.keys():
            self.pheromone[edge] = 1.0

    def _calculate_probabilities(self, current_city: str, unvisited: Set[str]) -> Dict[str, float]:
        """
        Tính xác suất chọn city tiếp theo.

        Chỉ xét các cities chưa thăm.

        Parameters:
        -----------
        current_city : str
            City hiện tại
        unvisited : Set[str]
            Set các cities chưa thăm

        Returns:
        --------
        Dict[str, float]
            {city: probability}
        """
        probabilities = {}
        attractiveness = {}

        # Tính attractiveness cho mỗi unvisited city
        for next_city in unvisited:
            edge = (current_city, next_city)
            tau = self.pheromone.get(edge, 1.0)
            eta = self.heuristic.get(edge, 1.0)

            # attractiveness = τ^α * η^β
            attractiveness[next_city] = (tau ** self.alpha) * (eta ** self.beta)

        # Chuẩn hóa thành xác suất
        if attractiveness:
            total = sum(attractiveness.values())
            if total > 0:
                for city, attr in attractiveness.items():
                    probabilities[city] = attr / total

        return probabilities

    def _select_next_city(self, probabilities: Dict[str, float]) -> str:
        """
        Chọn city tiếp theo theo xác suất.
        """
        if not probabilities:
            return None

        cities = list(probabilities.keys())
        probs = list(probabilities.values())

        # Ensure probabilities sum to 1
        probs = np.array(probs)
        probs = probs / probs.sum()

        selected = np.random.choice(cities, p=probs)
        return selected

    def _construct_tour(self, start_city: str = None) -> Tuple[List[str], float]:
        """
        Xây dựng tour đi qua tất cả cities.

        Parameters:
        -----------
        start_city : str, optional
            Starting city (nếu None thì random)

        Returns:
        --------
        Tuple[List[str], float]
            (tour, total_distance)
        """
        if start_city is None:
            start_city = np.random.choice(self.city_list)

        tour = [start_city]
        unvisited = set(self.city_list) - {start_city}
        current = start_city

        # Đi qua tất cả cities
        while unvisited:
            probabilities = self._calculate_probabilities(current, unvisited)

            if not probabilities:
                # Fallback: chọn random
                next_city = np.random.choice(list(unvisited))
            else:
                next_city = self._select_next_city(probabilities)

            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city

        # Quay về start city
        tour.append(start_city)

        # Tính total distance
        total_distance = calculate_tour_distance(tour, self.distances)

        return tour, total_distance

    def _update_pheromone(self, all_tours: List[Tuple[List[str], float]]):
        """
        Cập nhật pheromone sau mỗi iteration.

        Parameters:
        -----------
        all_tours : List[Tuple[List[str], float]]
            Danh sách các (tour, distance) của tất cả ants
        """
        # Bước 1: Bay hơi pheromone
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.evaporation_rate)

        # Bước 2: Chọn tours để update (elitist hoặc all)
        if self.elitist:
            # Chỉ top N% ants được update pheromone
            n_elite = max(1, int(self.n_ants * self.elitist_ratio))
            sorted_tours = sorted(all_tours, key=lambda x: x[1])
            tours_to_update = sorted_tours[:n_elite]
        else:
            tours_to_update = all_tours

        # Bước 3: Cập nhật pheromone từ tours
        for tour, distance in tours_to_update:
            if distance <= 0 or distance == float('inf'):
                continue

            # Lượng pheromone deposit
            delta_pheromone = self.Q / distance

            # Update tất cả edges trong tour
            for i in range(len(tour) - 1):
                edge = (tour[i], tour[i + 1])
                reverse_edge = (tour[i + 1], tour[i])

                # Update both directions (symmetric)
                if edge in self.pheromone:
                    self.pheromone[edge] += delta_pheromone
                if reverse_edge in self.pheromone:
                    self.pheromone[reverse_edge] += delta_pheromone

        # Bước 4: Apply Max-Min bounds nếu enabled
        if self.max_min:
            for edge in self.pheromone:
                self.pheromone[edge] = max(self.tau_min, min(self.tau_max, self.pheromone[edge]))

    def _update_max_min_bounds(self, best_distance: float):
        """
        Cập nhật tau_max và tau_min cho Max-Min Ant System.
        """
        if best_distance > 0 and best_distance != float('inf'):
            self.tau_max = self.Q / best_distance
            self.tau_min = self.tau_max / (2 * self.n_cities)

    def run(self, start_city: str = None, verbose: bool = True) -> Tuple[List[str], float, List[float]]:
        """
        Chạy ACO algorithm để tìm tour ngắn nhất.

        Parameters:
        -----------
        start_city : str, optional
            Starting city (nếu None thì mỗi ant chọn random)
        verbose : bool
            Print progress

        Returns:
        --------
        Tuple[List[str], float, List[float]]
            (best_tour, best_distance, history)
        """
        best_tour = None
        best_distance = float('inf')
        history = []

        if verbose:
            print(f"\n{'='*80}")
            print("STARTING TSP ACO ALGORITHM")
            print(f"{'='*80}")
            print(f"Cities: {self.n_cities}")
            print(f"Ants: {self.n_ants}, Iterations: {self.n_iterations}")
            print(f"Alpha: {self.alpha}, Beta: {self.beta}")
            print(f"Evaporation: {self.evaporation_rate}, Q: {self.Q}")
            print(f"Elitist: {self.elitist}, Local Search: {self.local_search}")
            print(f"Max-Min AS: {self.max_min}")
            print(f"{'='*80}\n")

        for iteration in range(self.n_iterations):
            all_tours = []

            # Mỗi ant xây dựng tour
            for ant in range(self.n_ants):
                tour, distance = self._construct_tour(start_city)

                # Local search improvement
                if self.local_search and distance < float('inf'):
                    tour, distance = two_opt_improve(tour, self.distances, max_iterations=100)

                all_tours.append((tour, distance))

                # Update best
                if distance < best_distance:
                    best_tour = tour[:]
                    best_distance = distance

                    if verbose and iteration > 0:
                        print(f"  🎯 New best found at iteration {iteration + 1}: {best_distance:.2f} km")

            # Update pheromone
            self._update_pheromone(all_tours)

            # Update Max-Min bounds
            if self.max_min:
                self._update_max_min_bounds(best_distance)

            # Lưu history
            history.append(best_distance)

            # Print progress
            if verbose and (iteration + 1) % 20 == 0:
                avg_distance = np.mean([d for _, d in all_tours if d < float('inf')])
                print(f"Iteration {iteration + 1}/{self.n_iterations}: "
                      f"Best = {best_distance:.2f} km, Avg = {avg_distance:.2f} km")

        if verbose:
            print(f"\n{'='*80}")
            print("ALGORITHM COMPLETED!")
            print(f"{'='*80}")
            print(f"Best tour distance: {best_distance:.2f} km")
            print(f"Tour: {' → '.join(best_tour[:5])} ... → {best_tour[0]}")
            print(f"{'='*80}\n")

        return best_tour, best_distance, history
