#!/bin/bash
# Script để chạy complex example với parameter comparison

echo "=================================="
echo "Running Complex Example"
echo "=================================="
echo ""
echo "This will test ACO with different parameter settings"
echo "and compare the results."
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra xem Poetry đã cài đặt dependencies chưa
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

# Chạy example
echo "Starting ACO Complex Example..."
echo ""
poetry run python examples/example_complex.py

echo ""
echo "=================================="
echo "Complex Example Completed!"
echo "=================================="
