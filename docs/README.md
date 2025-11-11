# Tài liệu Dự án - Documentation

Thư mục này chứa tài liệu chi tiết về dự án Ant Colony Optimization.

## Danh sách Tài liệu

### 📘 [IMPLEMENTATION.md](IMPLEMENTATION.md)
**Chi tiết Triển khai Thuật toán ACO**

Tài liệu kỹ thuật về cách triển khai thuật toán Ant Colony Optimization cho bài toán Shortest Path.

**Nội dung:**
- Cấu trúc class `AntColony` và các methods
- Chi tiết implementation của từng bước thuật toán
- Công thức toán học và pseudocode
- Độ phức tạp thời gian và không gian
- Hướng dẫn testing và validation
- Performance tips cho các loại đồ thị
- Tối ưu hóa đã áp dụng và giới hạn hiện tại

**Đối tượng:** Developer muốn hiểu cách code hoạt động hoặc đóng góp vào dự án.

---

### 📗 [TSP_DOCUMENTATION.md](TSP_DOCUMENTATION.md)
**Tài liệu Thuật toán Traveling Salesman Problem (TSP)**

Tài liệu toàn diện về giải pháp TSP sử dụng ACO cho 30 thành phố châu Âu, với phân tích kết quả chi tiết và visualizations.

**Nội dung:**
- Giới thiệu về TSP và độ phức tạp NP-hard
- Giải pháp ACO với các tối ưu hóa nâng cao:
  - Elitist Strategy
  - Max-Min Ant System
  - 2-opt Local Search
- Phân tích 6 hình ảnh kết quả (Figure_1 đến Figure_6)
- So sánh ACO vs Nearest Neighbor vs Random tours
- Biểu đồ hội tụ và thống kê tour
- Hướng dẫn sử dụng và code examples
- Parameter tuning cho TSP
- Benchmark và performance analysis

**Đối tượng:**
- Sinh viên học thuật toán tối ưu
- Người muốn hiểu kết quả và cách áp dụng ACO cho TSP
- Researcher quan tâm đến metaheuristic algorithms

---

## Tài liệu Khác

### 📄 [CLAUDE.md](../CLAUDE.md) (Root directory)
**Hướng dẫn cho Claude Code AI**

Tài liệu này nằm ở thư mục gốc và cung cấp hướng dẫn cho AI Claude Code khi làm việc với repository này.

**Nội dung:**
- Overview kiến trúc dự án
- Commands để development
- Sự khác biệt giữa 2 implementations (Shortest Path vs TSP)
- Data structures và design decisions
- Common pitfalls và best practices

---

### 📄 [README.md](../README.md) (Root directory)
**Tài liệu chính của dự án**

README chính nằm ở thư mục gốc, cung cấp quick start guide và overview toàn bộ dự án.

**Nội dung:**
- Giới thiệu dự án và thuật toán ACO
- Hướng dẫn cài đặt
- Quick start với scripts
- Examples và cách chạy
- Cấu trúc dự án
- API reference cơ bản

---

## Cách Sử Dụng Tài liệu

### Nếu bạn mới bắt đầu:
1. Đọc [README.md](../README.md) ở thư mục gốc để hiểu overview
2. Chạy examples để xem thuật toán hoạt động
3. Đọc [TSP_DOCUMENTATION.md](TSP_DOCUMENTATION.md) để hiểu kết quả

### Nếu bạn muốn hiểu sâu về code:
1. Đọc [IMPLEMENTATION.md](IMPLEMENTATION.md) để hiểu chi tiết triển khai
2. Xem source code trong `src/`
3. Tham khảo [CLAUDE.md](../CLAUDE.md) cho architecture overview

### Nếu bạn muốn nghiên cứu TSP:
1. Đọc [TSP_DOCUMENTATION.md](TSP_DOCUMENTATION.md) - tài liệu đầy đủ nhất
2. Xem các hình ảnh trong `data/images/`
3. Chạy `./scripts/run_tsp.sh` để tạo kết quả riêng
4. Đọc paper references trong tài liệu TSP

---

## Cấu trúc Dự án

```
ant-colony-shortest-path/
├── README.md                    # Quick start guide
├── CLAUDE.md                    # AI assistant guidance
├── docs/                        # ← BẠN ĐANG Ở ĐÂY
│   ├── README.md               # (Tài liệu này)
│   ├── IMPLEMENTATION.md       # Chi tiết triển khai Shortest Path ACO
│   └── TSP_DOCUMENTATION.md    # Tài liệu đầy đủ về TSP
├── src/                         # Source code
│   ├── aco.py                  # Shortest Path ACO
│   ├── tsp_aco.py              # TSP ACO (khác biệt hoàn toàn)
│   ├── tsp_utils.py            # TSP utilities
│   ├── visualization.py        # Plotting cho Shortest Path
│   └── tsp_visualization.py    # Plotting cho TSP
├── examples/                    # Example scripts
│   ├── example_simple.py       # 7 nodes
│   ├── example_sparse_graph.py # 15 nodes
│   ├── example_complex.py      # 100 nodes
│   └── example_tsp_europe.py   # 30 cities TSP
├── data/
│   ├── european_cities.json    # GPS data
│   └── images/                 # Hình ảnh kết quả
│       ├── Figure_1.png        # TSP tour 1
│       ├── Figure_2.png        # TSP tour 2
│       ├── Figure_3.png        # TSP tour 3
│       ├── Figure_4.png        # ACO vs NN comparison
│       ├── Figure_5.png        # Convergence plot
│       └── Figure_6.png        # Tour statistics
└── scripts/                     # Convenience scripts
    ├── run_simple.sh
    ├── run_tsp.sh
    └── ...
```

---

## Đóng Góp Tài liệu

Nếu bạn muốn cải thiện hoặc thêm tài liệu:

1. **IMPLEMENTATION.md**: Thêm chi tiết về implementation, test cases, hoặc optimizations
2. **TSP_DOCUMENTATION.md**: Thêm phân tích, so sánh với thuật toán khác, hoặc case studies
3. Tạo tài liệu mới cho features mới (ví dụ: GENETIC_ALGORITHM.md nếu thêm GA)

### Nguyên tắc viết tài liệu:

- Sử dụng tiếng Việt cho technical docs (trừ CLAUDE.md phải tiếng Anh)
- Bao gồm code examples và visualizations
- Giải thích "tại sao" chứ không chỉ "cái gì"
- Cung cấp references cho papers và resources
- Update README này khi thêm tài liệu mới

---

## Liên Hệ

**Tác giả:** Kinhluan - SGU

**Repository:** ant-colony-shortest-path

**License:** MIT

---

**Cập nhật lần cuối:** 2025-01-11
