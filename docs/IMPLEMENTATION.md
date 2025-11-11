# Chi tiết triển khai ACO Algorithm

## Tổng quan

Dự án đã được triển khai hoàn chỉnh với các thành phần chính:

### 1. Core Algorithm (`src/aco.py`)

#### Class `AntColony`

**Các thuộc tính chính:**

- `pheromone`: Dict lưu mức pheromone trên mỗi cạnh `{(u,v): value}`
- `heuristic`: Dict lưu giá trị heuristic `{(u,v): 1/distance}`

**Các methods đã implement:**

1. **`__init__()`** - Khởi tạo
   - Tạo ma trận pheromone với giá trị ban đầu = 1.0
   - Tính ma trận heuristic = 1/weight cho mỗi cạnh
   - Lưu các tham số (alpha, beta, evaporation_rate, Q)

2. **`_calculate_probabilities(current, unvisited)`** - Tính xác suất
   - Với mỗi nút có thể đến: `attractiveness = τ^α * η^β`
   - Chuẩn hóa thành xác suất: `P = attractiveness / sum(attractiveness)`
   - Return: Dict {node: probability}

3. **`_select_next_node(probabilities)`** - Chọn nút
   - Sử dụng `numpy.random.choice()` với probabilities
   - Chọn ngẫu nhiên theo phân phối xác suất

4. **`_construct_solution(start, end)`** - Xây dựng đường đi
   - Khởi tạo path = [start]
   - Loop cho đến khi current == end:
     - Tính probabilities cho các nút kề
     - Select next node
     - Add vào path và update distance
   - Fallback: Nếu bị stuck, dùng NetworkX shortest_path
   - Return: (path, distance)

5. **`_update_pheromone(all_paths)`** - Cập nhật pheromone
   - **Bay hơi**: `τ *= (1 - ρ)` cho tất cả cạnh
   - **Tăng cường**:
     - Với mỗi path: `delta = Q / distance`
     - Với mỗi cạnh trong path: `τ += delta`

6. **`run(start, end)`** - Main algorithm
   - Loop n_iterations lần:
     - Mỗi ant xây dựng solution
     - Update best_path và best_distance
     - Update pheromone
     - Lưu history
   - Return: (best_path, best_distance, history)

### 2. Visualization (`src/visualization.py`)

**3 functions chính:**

1. **`plot_graph(G, path, title)`**
   - Vẽ đồ thị NetworkX
   - Highlight path bằng màu đỏ
   - Start node = xanh lá, End node = đỏ
   - Hiển thị trọng số trên edges

2. **`plot_convergence(history, title)`**
   - Vẽ line chart: iterations vs best_distance
   - Annotation cho giá trị cuối cùng
   - Grid và legend

3. **`plot_comparison(histories, title)`**
   - So sánh nhiều lần chạy
   - Multiple lines trên cùng 1 chart
   - Dùng để so sánh tham số

### 3. Examples

#### Example Simple (`examples/example_simple.py`)

**Đồ thị 7 nodes:**

```
    0 --- 1 --- 2
    |     |     |
    3 --- 4 --- 5
          |
          6
```

**Workflow:**

1. Tạo graph với NetworkX
2. Visualize graph
3. Run ACO (10 ants, 50 iterations)
4. Visualize solution
5. Visualize convergence
6. So sánh với Dijkstra

**Kết quả:**

- Best path: 0 → 1 → 4 → 6
- Distance: 8.00
- ✓ Tìm được optimal path

#### Example Complex (`examples/example_complex.py`)

**Đồ thị 20 nodes (random geometric graph)**

**Workflow:**

1. Tạo random graph với NetworkX
2. Chạy 4 tests với tham số khác nhau:
   - Test 1: Default parameters
   - Test 2: More ants (50 ants)
   - Test 3: Higher beta (5.0)
   - Test 4: Lower evaporation (0.3)
3. So sánh kết quả:
   - Distance
   - Execution time
   - Error % so với optimal
4. Visualize:
   - Best ACO path
   - Optimal path (Dijkstra)
   - Convergence comparison

### 4. Công thức toán học

#### Xác suất chọn nút tiếp theo

```
P_ij = [τ_ij^α * η_ij^β] / Σ[τ_ik^α * η_ik^β]
```

Trong đó:

- `τ_ij`: Pheromone trên cạnh (i,j)
- `η_ij`: Heuristic = 1/distance(i,j)
- `α`: Trọng số pheromone (default: 1.0)
- `β`: Trọng số heuristic (default: 2.0)

#### Cập nhật pheromone

```
τ_ij = (1 - ρ) * τ_ij + Δτ_ij
```

Trong đó:

- `ρ`: Evaporation rate (default: 0.5)
- `Δτ_ij = Q / L_k` nếu kiến k đi qua cạnh (i,j)
- `L_k`: Độ dài đường đi của kiến k
- `Q`: Hằng số (default: 100)

## Testing

### Test 1: Simple Example

```bash
poetry run python examples/example_simple.py
```

**Kết quả:**

- ✓ Algorithm chạy thành công
- ✓ Tìm được optimal path
- ✓ Visualization hoạt động
- ✓ Convergence tốt (hội tụ sau ~10 iterations)

### Test 2: Complex Example

```bash
poetry run python examples/example_complex.py
```

**Kết quả dự kiến:**

- Test với nhiều bộ tham số
- So sánh performance
- Phân tích trade-offs

## Độ phức tạp

### Time Complexity

```
O(n_iterations × n_ants × V^2)
```

Trong đó V = số nodes

**Phân tích:**

- Mỗi iteration: n_ants con kiến
- Mỗi con kiến: Tối đa V steps
- Mỗi step: Tính probability cho ~V neighbors
- Total: O(I × A × V^2)

### Space Complexity

```
O(E)
```

Trong đó E = số edges

**Phân tích:**

- Pheromone matrix: O(E)
- Heuristic matrix: O(E)
- Path storage: O(V)
- Total: O(E)

## Optimizations Applied

1. **Dictionary thay vì Matrix**: Tiết kiệm memory cho sparse graphs
2. **Fallback mechanism**: Tránh infinite loop khi stuck
3. **Early convergence check**: Có thể dừng sớm nếu hội tụ
4. **Vectorized operations**: Dùng numpy cho probability calculations

## Known Limitations

1. **Undirected graph only**: Code hiện tại chỉ support undirected graphs
2. **Must be connected**: Đồ thị phải liên thông
3. **Stochastic**: Kết quả có thể khác nhau mỗi lần chạy
4. **Parameter sensitive**: Performance phụ thuộc nhiều vào tham số

## Future Improvements

1. **Support directed graphs**: Thêm option cho directed edges
2. **Multiple objectives**: Optimize nhiều objectives cùng lúc
3. **Adaptive parameters**: Tự động điều chỉnh alpha, beta theo progress
4. **Parallel processing**: Chạy ants song song để tăng tốc
5. **Early stopping**: Dừng khi convergence rate < threshold

## Performance Tips

### Cho đồ thị nhỏ (< 10 nodes)

- n_ants = 10
- n_iterations = 50
- beta = 2.0 (heuristic-focused)

### Cho đồ thị trung bình (10-50 nodes)

- n_ants = 20-30
- n_iterations = 100-150
- beta = 3.0

### Cho đồ thị lớn (> 50 nodes)

- n_ants = 50+
- n_iterations = 200+
- beta = 5.0 (very greedy)
- evaporation_rate = 0.3 (low)
