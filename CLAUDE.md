# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Ant Colony Optimization (ACO) implementation for solving two types of problems:
1. **Shortest Path Problem** - Finding optimal paths in weighted graphs
2. **Traveling Salesman Problem (TSP)** - Finding optimal tours visiting all cities

The project uses Python with Poetry for dependency management, NetworkX for graph operations, and provides both algorithmic implementations and rich visualizations.

## Development Commands

### Setup and Installation

```bash
# Install dependencies
./scripts/setup.sh
# or manually:
poetry install
```

### Running Examples

```bash
# Shortest Path examples
./scripts/run_simple.sh      # 7 nodes, basic example
./scripts/run_sparse.sh      # 15 nodes, 3 clusters
./scripts/run_complex.sh     # 100 nodes, grid layout

# TSP example
./scripts/run_tsp.sh         # 30 European cities

# Custom parameters
./scripts/run_custom.sh <n_ants> <n_iterations> <alpha> <beta>

# Test all examples
./scripts/test_all.sh
```

### Direct Python Execution

```bash
# Using poetry
poetry run python examples/example_simple.py
poetry run python examples/example_tsp_europe.py

# Or activate venv first
poetry shell
python examples/example_simple.py
```

## Code Architecture

### Two Distinct Algorithm Implementations

The codebase has **two separate ACO implementations** for different problem types:

#### 1. Shortest Path ACO (`src/aco.py`)
- **Purpose**: Find shortest path between two specific nodes
- **Key characteristic**: Partial graph traversal (start → end)
- **Core class**: `AntColony`
- **Methods**:
  - `_construct_solution(start, end)` - Ants build paths until reaching end node
  - Supports fallback to NetworkX shortest_path if ant gets stuck

#### 2. TSP ACO (`src/tsp_aco.py`)
- **Purpose**: Find shortest tour visiting all cities exactly once
- **Key characteristic**: Complete graph traversal (all nodes) + return to start
- **Core class**: `TSP_AntColony`
- **Advanced features**:
  - **Elitist strategy**: Only top 20% ants update pheromone
  - **Max-Min Ant System**: Bounded pheromone values to prevent stagnation
  - **2-opt local search**: Post-processing improvement
  - **Complete graph**: Uses Haversine distance for real GPS coordinates

### Key Algorithmic Differences

| Aspect | Shortest Path | TSP |
|--------|--------------|-----|
| Goal | Start → End | Visit all + cycle |
| Graph | Subset of edges | Complete graph |
| Termination | Reach end node | Visit all cities |
| Beta (heuristic weight) | 2.0 | 5.0 (more greedy) |
| Evaporation rate | 0.5 | 0.1 (slower) |
| Local search | No | Yes (2-opt) |
| Elite strategy | No | Yes |

### Core Algorithm Flow

Both implementations follow this pattern:

```
1. Initialize pheromone (τ) and heuristic (η=1/distance) matrices
2. For each iteration:
   a. Each ant constructs a solution:
      - Calculate probability: P(i,j) = [τ^α × η^β] / Σ[τ^α × η^β]
      - Select next node/city stochastically
   b. Update pheromone:
      - Evaporation: τ *= (1-ρ)
      - Reinforcement: τ += Q/distance for edges in solution
   c. Track best solution found
3. Return best solution + convergence history
```

### Utility Modules

- **`src/tsp_utils.py`**: TSP-specific utilities
  - `haversine_distance()` - Real-world distance calculation using GPS coordinates
  - `nearest_neighbor_tsp()` - Greedy benchmark algorithm
  - `two_opt_improve()` - Local search optimization
  - `calculate_distance_matrix()` - Precompute all pairwise distances

- **`src/visualization.py`**: Shortest path visualization (NetworkX graphs)
- **`src/tsp_visualization.py`**: TSP visualization (Matplotlib + Folium interactive maps)

## Data Structures

### Pheromone and Distance Storage

Both implementations use **dictionaries** rather than 2D arrays:

```python
# Pheromone: {(node_a, node_b): pheromone_value}
self.pheromone = {(0, 1): 1.0, (1, 2): 1.0, ...}

# Distance: {(city_a, city_b): distance_km}
self.distances = {('Paris', 'London'): 343.5, ...}
```

**Rationale**: Efficient for sparse graphs, symmetric edge support, and direct edge lookup.

### TSP Distance Matrix

For TSP, the complete distance matrix is **precomputed** once during initialization using Haversine formula for GPS coordinates. This trades memory for speed since TSP requires O(n²) distance lookups.

## Parameter Tuning Guidelines

### Shortest Path Problem

- **Small graphs (<20 nodes)**: `n_ants=20, n_iterations=100, beta=2.0`
- **Large graphs (>50 nodes)**: `n_ants=50, n_iterations=200, beta=4.0`

### TSP Problem

- **Standard configuration** (30 cities):
  - `n_ants=50, n_iterations=200`
  - `alpha=1.0, beta=5.0` (high beta = greedy, good for TSP)
  - `evaporation_rate=0.1` (low = pheromone persists)
  - `elitist=True, elitist_ratio=0.2`
  - `local_search=True, max_min=True`

### Parameter Effects

- **Higher β**: More greedy (favor short distances), faster convergence
- **Lower ρ (evaporation)**: Pheromone persists longer, more exploitation
- **More ants**: Better exploration, slower execution
- **Elitist strategy**: Only best ants reinforce pheromone, faster convergence

## Testing and Validation

Each example includes comparison with optimal solutions:
- Shortest Path: Compared against NetworkX Dijkstra
- TSP: Compared against Nearest Neighbor heuristic

Typical results:
- Simple graphs: ACO finds optimal path
- Complex graphs: ACO within 0-5% of optimal
- TSP (30 cities): 15-25% improvement over Nearest Neighbor

## File Organization

```
src/
├── aco.py                 # Shortest Path ACO implementation
├── tsp_aco.py            # TSP ACO implementation (separate algorithm)
├── tsp_utils.py          # TSP utilities (Haversine, 2-opt, etc.)
├── visualization.py       # Shortest Path plotting
└── tsp_visualization.py  # TSP plotting (includes Folium maps)

examples/
├── example_simple.py      # 7 nodes
├── example_sparse_graph.py # 15 nodes, clustered
├── example_complex.py     # 100 nodes, parameter comparison
└── example_tsp_europe.py  # 30 European cities with GPS coords

data/
└── european_cities.json   # Real GPS coordinates for 30 cities

scripts/
└── *.sh                   # Convenience scripts for running examples
```

## Important Implementation Details

### Probability Calculation Edge Cases

When an ant calculates next-node probabilities, if no valid neighbors exist (disconnected graph or all visited), the code has fallback mechanisms:
- **Shortest Path**: Falls back to NetworkX `shortest_path()` to complete the route
- **TSP**: Randomly selects from unvisited cities

### Symmetric Graph Handling

Both edge directions are stored and updated:
```python
self.pheromone[(u, v)] += delta
self.pheromone[(v, u)] += delta  # Symmetric
```

This ensures undirected graphs work correctly.

### 2-opt Local Search (TSP Only)

The 2-opt improvement swaps edge pairs to eliminate crossing edges:
```python
# If reversing segment [i:j] reduces distance, apply swap
best_tour[i:j+1] = reversed(best_tour[i:j+1])
```

Limited to `max_iterations=100` to avoid excessive runtime.

## Working with TSP Data

European cities data structure:
```json
{
  "cities": {
    "Paris": {
      "lat": 48.8566,
      "lon": 2.3522,
      "country": "France"
    }
  }
}
```

To add new cities or create custom datasets, maintain this JSON structure and ensure all cities have `lat`, `lon`, and `country` fields.

## Visualization Outputs

- **Shortest Path**: Matplotlib figures showing graph, path, and convergence
- **TSP**: 6 visualizations including:
  - Tour maps with cities and routes
  - Convergence plots
  - Statistical analysis (distance per segment, countries visited)
  - Interactive HTML map (`tsp_europe_tour.html`) using Folium

## Common Pitfalls

1. **Disconnected graphs**: Shortest Path ACO requires connected graphs. Check with `nx.is_connected(G)`.

2. **Parameter sensitivity**: ACO is stochastic - results vary between runs. For reproducible results, set `np.random.seed()`.

3. **TSP vs Shortest Path confusion**: These are **different algorithms** in different files. Don't mix their APIs.

4. **Distance matrix symmetry**: When adding edges, ensure both directions are added for undirected graphs.

5. **2-opt complexity**: For large TSP instances (>100 cities), 2-opt can become slow. Consider reducing `max_iterations`.

## Performance Characteristics

### Time Complexity
- **Shortest Path**: O(iterations × ants × nodes²)
- **TSP**: O(iterations × ants × cities²) + O(cities² × 2opt_iterations)

### Typical Execution Times (M1 MacBook)
- Simple example (7 nodes): ~1 second
- Complex example (100 nodes): ~20 seconds
- TSP Europe (30 cities): ~18 seconds

## Dependencies

Core dependencies (see `pyproject.toml`):
- `networkx` - Graph data structures and algorithms
- `numpy` - Numerical computations and random selection
- `matplotlib` - Static visualizations
- `folium` - Interactive map generation for TSP

Poetry manages all dependencies - no manual pip installs needed.
