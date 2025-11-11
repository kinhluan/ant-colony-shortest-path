#!/bin/bash
# Script để chạy ACO với custom parameters

echo "=================================="
echo "Run ACO with Custom Parameters"
echo "=================================="
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra setup
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
    echo ""
fi

# Create temporary Python script
cat > /tmp/aco_custom.py << 'EOF'
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import networkx as nx
from src.aco import AntColony
from src.visualization import plot_graph, plot_convergence

def main():
    # Tạo đồ thị mẫu
    G = nx.Graph()
    edges = [
        (0, 1, 2.0), (0, 3, 4.0),
        (1, 2, 3.0), (1, 4, 1.0),
        (2, 5, 2.0), (3, 4, 2.0),
        (4, 5, 3.0), (4, 6, 5.0),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    print("Graph created with {} nodes and {} edges".format(
        G.number_of_nodes(), G.number_of_edges()
    ))

    # Parameters từ command line hoặc default
    n_ants = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    n_iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    alpha = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    beta = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0

    print("\nParameters:")
    print("  n_ants: {}".format(n_ants))
    print("  n_iterations: {}".format(n_iterations))
    print("  alpha: {}".format(alpha))
    print("  beta: {}".format(beta))
    print()

    # Run ACO
    aco = AntColony(
        graph=G,
        n_ants=n_ants,
        n_iterations=n_iterations,
        alpha=alpha,
        beta=beta
    )

    best_path, best_distance, history = aco.run(start=0, end=6)

    # Visualize
    plot_graph(G, path=best_path,
               title="Custom ACO (Distance: {:.2f})".format(best_distance))
    plot_convergence(history, title="Custom ACO Convergence")

if __name__ == "__main__":
    main()
EOF

# Hướng dẫn sử dụng
echo "Usage: ./scripts/run_custom.sh [n_ants] [n_iterations] [alpha] [beta]"
echo ""
echo "Examples:"
echo "  ./scripts/run_custom.sh                    # Use defaults"
echo "  ./scripts/run_custom.sh 50 200            # 50 ants, 200 iterations"
echo "  ./scripts/run_custom.sh 30 150 1.5 3.0   # Custom all parameters"
echo ""

# Chạy với parameters từ command line
poetry run python /tmp/aco_custom.py "$@"

# Cleanup
rm /tmp/aco_custom.py

echo ""
echo "=================================="
echo "Custom Run Completed!"
echo "=================================="
