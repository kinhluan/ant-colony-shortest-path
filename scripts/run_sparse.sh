#!/bin/bash
# Script để chạy sparse graph example với nhiều nodes phân bố rời rạc

echo "=================================="
echo "Running Sparse Graph Example"
echo "=================================="
echo ""
echo "This example demonstrates ACO on a graph with:"
echo "  - 15 nodes organized in 3 clusters"
echo "  - Clear visual separation for easy understanding"
echo "  - Cross-cluster pathfinding"
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra xem Poetry đã cài đặt dependencies chưa
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

# Chạy example
echo "Starting ACO Sparse Graph Example..."
echo ""
poetry run python examples/example_sparse_graph.py

echo ""
echo "=================================="
echo "Sparse Graph Example Completed!"
echo "=================================="
