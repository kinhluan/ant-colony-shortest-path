# Project Overview

This project implements the Ant Colony Optimization (ACO) algorithm in Python to find the shortest path in a graph. It uses the `networkx` library to represent and manipulate graphs, `numpy` for numerical calculations, and `matplotlib` for visualizing the graph and the algorithm's convergence.

The core of the project is the `AntColony` class in `src/aco.py`, which encapsulates the ACO logic. The `src/visualization.py` module provides utility functions to plot the graph, highlight the shortest path found, and visualize the convergence of the algorithm over iterations.

The project is structured as a Python package and uses Poetry for dependency management. It includes several examples in the `examples/` directory that demonstrate how to use the ACO algorithm on different types of graphs (simple, sparse, and complex).

# Building and Running

The project uses Poetry to manage dependencies and run the code.

## Setup

To set up the project and install the required dependencies, run the following command:

```bash
poetry install
```

This will create a virtual environment and install the packages listed in `pyproject.toml`.

## Running the Examples

The `scripts/` directory contains several shell scripts to easily run the examples.

*   **Run the simple example:**
    ```bash
    ./scripts/run_simple.sh
    ```
    or
    ```bash
    poetry run python examples/example_simple.py
    ```

*   **Run the sparse graph example:**
    ```bash
    ./scripts/run_sparse.sh
    ```
    or
    ```bash
    poetry run python examples/example_sparse_graph.py
    ```

*   **Run the complex example:**
    ```bash
    ./scripts/run_complex.sh
    ```
    or
    ```bash
    poetry run python examples/example_complex.py
    ```

## Running with Custom Parameters

You can run the ACO algorithm with custom parameters using the `run_custom.sh` script:

```bash
./scripts/run_custom.sh [n_nodes] [n_ants] [alpha] [beta]
```

For example:

```bash
./scripts/run_custom.sh 30 150 1.5 3.0
```

# Development Conventions

*   **Code Style:** The code follows the standard Python conventions (PEP 8).
*   **Typing:** The code uses type hints for better readability and maintainability.
*   **Modularity:** The project is organized into modules with clear responsibilities (e.g., `aco.py` for the algorithm, `visualization.py` for plotting).
*   **Documentation:** The code includes docstrings that explain the purpose of classes, methods, and functions. The `README.md` file provides a comprehensive overview of the project.
