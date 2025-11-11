#!/bin/bash
# Script để clean/reset project

echo "=================================="
echo "Cleaning Project"
echo "=================================="
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

echo "This will remove:"
echo "  - Virtual environment (.venv)"
echo "  - Python cache (__pycache__)"
echo "  - Poetry lock file (poetry.lock)"
echo ""
read -p "Are you sure? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Cleaning..."

# Remove virtual environment
if [ -d ".venv" ]; then
    echo "  - Removing .venv/"
    rm -rf .venv
fi

# Remove __pycache__
echo "  - Removing __pycache__ directories"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove .pyc files
echo "  - Removing .pyc files"
find . -type f -name "*.pyc" -delete 2>/dev/null

# Remove poetry.lock (optional)
if [ -f "poetry.lock" ]; then
    read -p "  - Remove poetry.lock? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm poetry.lock
        echo "    ✓ Removed poetry.lock"
    fi
fi

echo ""
echo "=================================="
echo "Cleaning completed!"
echo "=================================="
echo ""
echo "Run './scripts/setup.sh' to reinstall dependencies."
