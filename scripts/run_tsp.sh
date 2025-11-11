#!/bin/bash
# Script để chạy TSP Europe example

echo "=========================================="
echo "TSP: European Cities Tour with ACO"
echo "=========================================="
echo ""
echo "This example demonstrates Ant Colony Optimization"
echo "for the Traveling Salesman Problem:"
echo "  - 30 major European cities"
echo "  - Elitist strategy + Max-Min AS"
echo "  - 2-opt local search"
echo "  - Interactive Folium map"
echo "  - Benchmark với Nearest Neighbor"
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra xem Poetry đã cài đặt dependencies chưa
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

# Kiểm tra folium
echo "Checking dependencies..."
poetry run python -c "import folium" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing folium..."
    poetry add folium
fi

# Chạy example
echo ""
echo "Starting TSP ACO Example..."
echo "This may take 2-3 minutes to complete."
echo ""
poetry run python examples/example_tsp_europe.py

echo ""
echo "=========================================="
echo "TSP Example Completed!"
echo "=========================================="
echo ""
echo "Check for 'tsp_europe_tour.html' in the project root"
echo "Open it in your browser to see the interactive map!"
