#!/bin/bash
# Script để test tất cả examples

echo "=================================="
echo "Testing All Examples"
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

# Counter cho results
total=0
passed=0
failed=0

echo "Running all examples..."
echo ""

# Test 1: Simple Example
echo "▶ Test 1: Simple Example"
echo "-----------------------------------"
poetry run python examples/example_simple.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PASSED"
    ((passed++))
else
    echo "✗ FAILED"
    ((failed++))
fi
((total++))
echo ""

# Test 2: Complex Example
echo "▶ Test 2: Complex Example"
echo "-----------------------------------"
poetry run python examples/example_complex.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PASSED"
    ((passed++))
else
    echo "✗ FAILED"
    ((failed++))
fi
((total++))
echo ""

# Test 3: Import test
echo "▶ Test 3: Import Test"
echo "-----------------------------------"
poetry run python -c "from src.aco import AntColony; from src.visualization import plot_graph; print('Import successful')" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PASSED"
    ((passed++))
else
    echo "✗ FAILED"
    ((failed++))
fi
((total++))
echo ""

# Summary
echo "=================================="
echo "Test Results"
echo "=================================="
echo "Total:  $total"
echo "Passed: $passed"
echo "Failed: $failed"
echo ""

if [ $failed -eq 0 ]; then
    echo "✓ All tests passed!"
    exit 0
else
    echo "✗ Some tests failed!"
    exit 1
fi
