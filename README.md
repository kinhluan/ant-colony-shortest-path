# Ant Colony Optimization for Shortest Path Finding & TSP

Triển khai thuật toán **Ant Colony Optimization (ACO)** cho:
1. **Shortest Path Problem** - Tìm đường đi ngắn nhất trong đồ thị
2. **Traveling Salesman Problem (TSP)** - Tìm tour ngắn nhất qua tất cả các điểm

Sử dụng Python, NetworkX, và Folium.

📚 **Documentation**: [Implementation Details](docs/IMPLEMENTATION.md) | [Scripts Guide](scripts/README.md)

## Mô tả

Thuật toán ACO mô phỏng hành vi tìm đường của đàn kiến trong tự nhiên. Kiến giao tiếp với nhau thông qua pheromone (chất dấu vết hóa học), tạo ra một hệ thống tập thể thông minh để tìm đường đi tối ưu.

### Nguyên lý hoạt động

1. **Khởi tạo**: Đặt pheromone ban đầu trên tất cả các cạnh
2. **Xây dựng giải pháp**: Mỗi kiến di chuyển từ nguồn đến đích, chọn nút tiếp theo dựa trên:
   - **Pheromone** (τ): Dấu vết từ các kiến trước
   - **Heuristic** (η): Thông tin heuristic = 1/khoảng cách
   - Xác suất: `P(i,j) = [τ(i,j)^α * η(i,j)^β] / Σ[τ(i,k)^α * η(i,k)^β]`
3. **Cập nhật pheromone**:
   - Bay hơi: `τ(i,j) = (1 - ρ) * τ(i,j)`
   - Tăng cường: `τ(i,j) += Q / L` (với L là độ dài đường đi)
4. **Lặp lại**: Chạy 50-200 vòng lặp để hội tụ

## Cài đặt

### Yêu cầu

- Python 3.8+
- Poetry (để quản lý dependencies)

### Cài đặt dependencies

```bash
# Cài đặt Poetry (nếu chưa có)
curl -sSL https://install.python-poetry.org | python3 -

# Clone repository
git clone https://github.com/yourusername/ant-colony-shortest-path.git
cd ant-colony-shortest-path

# Cài đặt dependencies
poetry install
```

## Sử dụng

### Quick Start với Scripts

Cách đơn giản nhất để chạy examples:

```bash
# Setup và cài đặt dependencies
./scripts/setup.sh

# === SHORTEST PATH EXAMPLES ===
# Chạy simple example (7 nodes)
./scripts/run_simple.sh

# Chạy sparse graph example (15 nodes, 3 clusters)
./scripts/run_sparse.sh

# Chạy complex example (100 nodes, grid layout)
./scripts/run_complex.sh

# Chạy với custom parameters
./scripts/run_custom.sh 30 150 1.5 3.0

# === TSP EXAMPLE ===
# Chạy TSP Europe (30 cities) - NEW! ⭐
./scripts/run_tsp.sh

# Test tất cả examples
./scripts/test_all.sh
```

📖 Xem thêm: [Scripts Documentation](scripts/README.md)

---

### Example 1: Đồ thị đơn giản

```bash
# Sử dụng script
./scripts/run_simple.sh

# Hoặc chạy trực tiếp
poetry run python examples/example_simple.py
```

Chạy ACO trên đồ thị 7 nodes, hiển thị:
- Visualization của đồ thị
- Đường đi tốt nhất tìm được
- Biểu đồ hội tụ
- So sánh với Dijkstra

### Example 2: Đồ thị phân bố rời rạc (Sparse Graph)

```bash
# Sử dụng script
./scripts/run_sparse.sh

# Hoặc chạy trực tiếp
poetry run python examples/example_sparse_graph.py
```

Chạy ACO trên đồ thị 15 nodes phân bố thành 3 clusters rõ ràng:
- Visualization dễ nhìn với màu sắc phân biệt clusters
- Cross-cluster pathfinding
- Fixed positions để dễ theo dõi
- 2 test cases khác nhau

### Example 3: Đồ thị phức tạp (100 nodes)

```bash
# Sử dụng script
./scripts/run_complex.sh

# Hoặc chạy trực tiếp
poetry run python examples/example_complex.py
```

Chạy ACO trên đồ thị lớn 100 nodes phân bố đều theo grid:
- Grid layout với 100 nodes phân bố đồng đều
- 5 tests với bộ tham số khác nhau
- So sánh performance và accuracy
- Benchmark thời gian thực thi
- Phân tích convergence chi tiết

### Example 4: TSP - European Cities Tour ⭐ NEW

```bash
# Sử dụng script
./scripts/run_tsp.sh

# Hoặc chạy trực tiếp
poetry run python examples/example_tsp_europe.py
```

**Traveling Salesman Problem** - Tìm tour ngắn nhất qua 30 thành phố châu Âu:

**Features:**
- 🌍 **30 major European cities** với GPS coordinates thực
- 🧮 **Haversine distance** - Khoảng cách thực tế (km)
- 🎯 **Complete graph** - Mọi city kết nối với nhau
- 🏆 **Elitist strategy** - Top 20% ants update pheromone
- 📈 **Max-Min Ant System** - Bounded pheromone
- 🔍 **2-opt local search** - Post-processing optimization
- 🗺️ **Interactive Folium map** - Export HTML, mở bằng browser
- 📊 **6 visualizations** khác nhau
- ⚖️ **Benchmark** với Nearest Neighbor và Random tours

**Output:**
- Shortest tour visiting all 30 cities
- Distance comparison (ACO vs NN vs Random)
- Interactive HTML map (tsp_europe_tour.html)
- Detailed statistics và analysis
- Multiple starting cities comparison

**Typical Results:**
- Nearest Neighbor: ~12,000-15,000 km
- ACO Optimized: ~10,000-12,000 km
- Improvement: 15-25%

### Sử dụng trong code

#### Shortest Path Example

```python
import networkx as nx
from src.aco import AntColony
from src.visualization import plot_graph, plot_convergence

# Tạo đồ thị
G = nx.Graph()
G.add_edge(0, 1, weight=2.0)
G.add_edge(1, 2, weight=3.0)
G.add_edge(0, 2, weight=7.0)

# Khởi tạo ACO
aco = AntColony(
    graph=G,
    n_ants=20,
    n_iterations=100,
    alpha=1.0,
    beta=2.0,
    evaporation_rate=0.5,
    Q=100
)

# Chạy thuật toán
best_path, best_distance, history = aco.run(start=0, end=2)

print(f"Best path: {best_path}")
print(f"Distance: {best_distance}")

# Visualize
plot_graph(G, path=best_path)
plot_convergence(history)
```

#### TSP Example

```python
from src.tsp_aco import TSP_AntColony
from src.tsp_utils import load_cities
from src.tsp_visualization import plot_tsp_tour, plot_interactive_tour

# Load cities
cities = load_cities('data/european_cities.json')

# Initialize TSP ACO
tsp_aco = TSP_AntColony(
    cities=cities,
    n_ants=50,
    n_iterations=200,
    alpha=1.0,
    beta=5.0,
    evaporation_rate=0.1,
    Q=1000,
    elitist=True,
    local_search=True,
    max_min=True
)

# Solve TSP
best_tour, best_distance, history = tsp_aco.run(start_city='Paris')

print(f"Best tour distance: {best_distance:.2f} km")
print(f"Tour: {' → '.join(best_tour)}")

# Visualize
plot_tsp_tour(cities, best_tour)
plot_interactive_tour(cities, best_tour, best_distance)
```

## Tham số ACO

### Shortest Path Parameters

| Tham số | Mô tả | Giá trị mặc định | Khuyến nghị |
|---------|-------|------------------|-------------|
| `n_ants` | Số kiến mỗi vòng lặp | 20 | 10-50 |
| `n_iterations` | Số vòng lặp | 100 | 50-200 |
| `alpha` | Trọng số pheromone | 1.0 | 0.5-2.0 |
| `beta` | Trọng số heuristic | 2.0 | 1.0-5.0 |
| `evaporation_rate` | Tỷ lệ bay hơi (ρ) | 0.5 | 0.1-0.9 |
| `Q` | Hằng số cập nhật pheromone | 100 | 1-1000 |

### TSP Parameters

| Tham số | Mô tả | Giá trị mặc định | Khuyến nghị cho TSP |
|---------|-------|------------------|---------------------|
| `n_ants` | Số kiến mỗi vòng lặp | 50 | 30-100 |
| `n_iterations` | Số vòng lặp | 200 | 100-300 |
| `alpha` | Trọng số pheromone | 1.0 | 0.8-1.5 |
| `beta` | Trọng số heuristic | 5.0 | 3.0-7.0 (cao hơn) |
| `evaporation_rate` | Tỷ lệ bay hơi (ρ) | 0.1 | 0.05-0.3 (thấp hơn) |
| `Q` | Hằng số cập nhật pheromone | 1000 | 500-2000 |
| `elitist` | Chỉ top ants update | True | True |
| `elitist_ratio` | Tỷ lệ elite ants | 0.2 | 0.1-0.3 |
| `local_search` | 2-opt improvement | True | True |
| `max_min` | Max-Min bounds | True | True |

### Hướng dẫn điều chỉnh tham số

- **Tăng `n_ants`**: Cải thiện khả năng khám phá, nhưng tốn thời gian hơn
- **Tăng `beta`**: Ưu tiên đường đi ngắn hơn (greedy), hội tụ nhanh hơn
- **Giảm `evaporation_rate`**: Pheromone tồn tại lâu hơn, tăng exploitation
- **Tăng `alpha`**: Tin tưởng pheromone nhiều hơn, có thể hội tụ sớm

## Cấu trúc dự án

```
ant-colony-shortest-path/
├── pyproject.toml              # Poetry configuration
├── README.md                   # Tài liệu này
├── data/                       # Data files
│   └── european_cities.json   # 30 European cities với GPS coords
├── src/
│   ├── __init__.py            # Package initialization
│   ├── aco.py                 # ACO cho Shortest Path
│   ├── visualization.py       # Plotting functions
│   ├── tsp_aco.py             # ACO cho TSP ⭐
│   ├── tsp_utils.py           # TSP utilities (Haversine, 2-opt, etc.) ⭐
│   └── tsp_visualization.py   # TSP plotting (Matplotlib + Folium) ⭐
├── examples/
│   ├── example_simple.py      # Shortest Path: 7 nodes
│   ├── example_sparse_graph.py # Shortest Path: 15 nodes, 3 clusters
│   ├── example_complex.py     # Shortest Path: 100 nodes, grid
│   └── example_tsp_europe.py  # TSP: 30 European cities ⭐
├── scripts/                    # Bash scripts tiện ích
│   ├── README.md              # Scripts documentation
│   ├── setup.sh               # Setup dependencies
│   ├── run_simple.sh          # Chạy simple example
│   ├── run_sparse.sh          # Chạy sparse graph example
│   ├── run_complex.sh         # Chạy complex example
│   ├── run_custom.sh          # Chạy với custom parameters
│   ├── run_tsp.sh             # Chạy TSP example ⭐
│   ├── test_all.sh            # Test tất cả examples
│   └── clean.sh               # Clean project
└── docs/                       # Documentation
    └── IMPLEMENTATION.md      # Chi tiết implementation
```

## API Reference

### Class `AntColony`

#### `__init__(graph, n_ants, n_iterations, alpha, beta, evaporation_rate, Q)`

Khởi tạo thuật toán ACO.

#### `run(start, end)`

Chạy thuật toán để tìm đường đi ngắn nhất.

**Returns:**
- `best_path` (List[int]): Đường đi tốt nhất
- `best_distance` (float): Độ dài đường đi
- `history` (List[float]): Lịch sử best distance qua các iterations

### Visualization Functions

#### `plot_graph(G, path=None, title="Graph")`

Vẽ đồ thị với tùy chọn highlight đường đi.

#### `plot_convergence(history, title="ACO Convergence")`

Vẽ biểu đồ hội tụ của thuật toán.

#### `plot_comparison(histories, title="Comparison")`

So sánh nhiều lần chạy với các tham số khác nhau.

## Thuật toán

### Pseudocode

```
1. Khởi tạo pheromone τ(i,j) = 1 cho tất cả cạnh
2. Khởi tạo heuristic η(i,j) = 1/distance(i,j)

3. For iteration = 1 to n_iterations:
   a. For each ant:
      - Xây dựng đường đi từ start đến end
      - Chọn nút tiếp theo theo xác suất P(i,j)

   b. Cập nhật pheromone:
      - Bay hơi: τ(i,j) *= (1 - ρ)
      - Tăng cường: τ(i,j) += Q/L cho cạnh trong đường đi

   c. Lưu best solution

4. Return best_path, best_distance
```

### Độ phức tạp

- **Time**: O(n_iterations × n_ants × n_nodes²)
- **Space**: O(n_edges)

## Ví dụ kết quả

### Simple Graph (7 nodes)
```
Best path: 0 -> 1 -> 4 -> 6
Best distance: 8.00
Optimal distance: 8.00
✓ ACO found the optimal path!
```

### Sparse Graph (15 nodes, 3 clusters)
```
Test 1 (Cluster A → Cluster C):
  ACO path: 0 -> 10 -> 11 -> 13 -> 14
  Distance: 17.50
  ✓ Found optimal path!

Test 2 (Cluster B → Cluster A):
  ACO path: 9 -> 8 -> 7 -> 2 -> 0
  Distance: 19.00
  ✓ Found optimal path!
```

### Complex Graph (20 nodes)
```
Test 1 (Default)        Distance: 24.53    Time: 2.15s    Error: 2.34%
Test 2 (More Ants)      Distance: 23.97    Time: 4.82s    Error: 0.00%
Test 3 (High Beta)      Distance: 24.12    Time: 2.08s    Error: 0.63%
Test 4 (Low Evap)       Distance: 24.31    Time: 2.19s    Error: 1.42%
```

## Tài liệu tham khảo

- [Ant Colony Optimization on Medium](https://medium.com/@abdallahashraf90/ant-colony-optimization-algorithm-for-shortest-path-problem-in-graph-3b5e9a4f8d2a)
- [ACO GitHub Repository](https://github.com/vasilibotnaru/ant-colony-optimization)
- NetworkX Documentation: https://networkx.org/

## Tác giả

Luân B

## License

MIT License
