#!/bin/bash
# Script để setup project và install dependencies

echo "=================================="
echo "ACO Project Setup"
echo "=================================="
echo ""

# Chuyển đến thư mục root của project
cd "$(dirname "$0")/.."

# Kiểm tra Poetry đã được cài đặt chưa
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed!"
    echo ""
    echo "Please install Poetry first:"
    echo "  curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    echo "Or visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "Poetry found: $(poetry --version)"
echo ""

# Kiểm tra Python version
python_version=$(python3 --version)
echo "Python version: $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
poetry install

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Setup completed successfully!"
    echo "=================================="
    echo ""
    echo "You can now run:"
    echo "  ./scripts/run_simple.sh     - Run simple example"
    echo "  ./scripts/run_complex.sh    - Run complex example"
    echo "  ./scripts/test_all.sh       - Run all examples"
    echo ""
else
    echo ""
    echo "Setup failed! Please check the error messages above."
    exit 1
fi
