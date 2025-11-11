# Scripts

Thư mục này chứa các bash scripts tiện ích để chạy và quản lý dự án ACO.

## Danh sách Scripts

### 1. `setup.sh` - Cài đặt dependencies

Cài đặt tất cả dependencies cần thiết sử dụng Poetry.

```bash
./scripts/setup.sh
```

**Chức năng:**
- Kiểm tra Poetry đã được cài đặt
- Kiểm tra Python version
- Cài đặt dependencies từ pyproject.toml
- Tạo virtual environment

---

### 2. `run_simple.sh` - Chạy simple example

Chạy ví dụ đơn giản với đồ thị 7 nodes.

```bash
./scripts/run_simple.sh
```

**Output:**
- Đồ thị gốc
- Đường đi tốt nhất
- Biểu đồ hội tụ
- So sánh với Dijkstra

---

### 3. `run_sparse.sh` - Chạy sparse graph example

Chạy ví dụ với đồ thị 15 nodes phân bố rời rạc thành 3 clusters.

```bash
./scripts/run_sparse.sh
```

**Output:**
- Đồ thị với 3 clusters dễ nhìn (màu khác nhau)
- 2 test cases: cross-cluster pathfinding
- Visualization rõ ràng với positions cố định
- Convergence comparison

---

### 4. `run_complex.sh` - Chạy complex example

Chạy ví dụ phức tạp với đồ thị 20 nodes và so sánh nhiều bộ tham số.

```bash
./scripts/run_complex.sh
```

**Output:**
- Test với 4 bộ tham số khác nhau
- Comparison table
- Visualization cho best path
- Convergence comparison

---

### 5. `run_custom.sh` - Chạy với custom parameters

Chạy ACO với tham số tùy chỉnh.

```bash
./scripts/run_custom.sh [n_ants] [n_iterations] [alpha] [beta]
```

**Examples:**
```bash
# Sử dụng default parameters
./scripts/run_custom.sh

# 50 ants, 200 iterations
./scripts/run_custom.sh 50 200

# Custom tất cả parameters
./scripts/run_custom.sh 30 150 1.5 3.0
```

**Parameters:**
- `n_ants`: Số kiến mỗi vòng lặp (default: 20)
- `n_iterations`: Số vòng lặp (default: 100)
- `alpha`: Trọng số pheromone (default: 1.0)
- `beta`: Trọng số heuristic (default: 2.0)

---

### 6. `test_all.sh` - Test tất cả examples

Chạy tất cả examples và kiểm tra xem có lỗi không.

```bash
./scripts/test_all.sh
```

**Tests:**
- Simple example
- Complex example
- Import test (kiểm tra modules)

**Output:**
```
Test Results
==================================
Total:  3
Passed: 3
Failed: 0

✓ All tests passed!
```

---

### 7. `clean.sh` - Dọn dẹp project

Xóa virtual environment, cache files, và optional poetry.lock.

```bash
./scripts/clean.sh
```

**Removes:**
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache directories
- `*.pyc` - Compiled Python files
- `poetry.lock` (optional) - Poetry lock file

---

## Workflow Thông Thường

### Lần đầu setup:
```bash
# 1. Clone/download project
cd ant-colony-shortest-path

# 2. Cài đặt dependencies
./scripts/setup.sh

# 3. Test xem mọi thứ hoạt động
./scripts/test_all.sh
```

### Chạy examples:
```bash
# Simple example
./scripts/run_simple.sh

# Complex example
./scripts/run_complex.sh

# Custom parameters
./scripts/run_custom.sh 40 150 2.0 3.0
```

### Clean và rebuild:
```bash
# Clean project
./scripts/clean.sh

# Setup lại
./scripts/setup.sh
```

---

## Troubleshooting

### Script không chạy được (Permission denied)

Thêm quyền executable:
```bash
chmod +x scripts/*.sh
```

### Poetry không tìm thấy

Cài đặt Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Python version không đúng

Dự án yêu cầu Python 3.8+. Kiểm tra version:
```bash
python3 --version
```

### Dependencies cài đặt thất bại

Thử xóa và cài lại:
```bash
./scripts/clean.sh
./scripts/setup.sh
```

---

## Tạo script riêng

Bạn có thể tạo script riêng của mình trong thư mục này. Template:

```bash
#!/bin/bash
# Mô tả script

echo "Script name"
cd "$(dirname "$0")/.."  # Chuyển về root directory

# Kiểm tra setup
if [ ! -d ".venv" ]; then
    ./scripts/setup.sh
fi

# Code của bạn ở đây
poetry run python your_script.py

echo "Done!"
```

Nhớ chmod +x cho script mới:
```bash
chmod +x scripts/your_script.sh
```
