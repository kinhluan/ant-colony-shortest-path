#!/bin/bash
# Script để chạy simple example

echo "=================================="
echo "Running Simple Example"
echo "=================================="
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra xem Poetry đã cài đặt dependencies chưa
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

# Chạy example
echo "Starting ACO Simple Example..."
echo ""
poetry run python examples/example_simple.py

echo ""
echo "=================================="
echo "Simple Example Completed!"
echo "=================================="
