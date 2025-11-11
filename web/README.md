# Web Demo - GitHub Pages

Thư mục này chứa website và interactive demos cho GitHub Pages.

## Cấu trúc

```
web/
├── index.html              # Trang chủ
├── playground.html         # Interactive ACO Playground 🎮
├── aco-simulation.js       # JavaScript ACO implementation
├── demo/                   # Interactive demos
│   └── tsp_europe_tour.html
├── .nojekyll              # Cho phép Jekyll bypass
└── README.md              # File này
```

## GitHub Pages Setup

### 1. Enable GitHub Pages

Vào repository settings → Pages → chọn:
- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/web`

### 2. URL

Sau khi enable, website sẽ có tại:
```
https://yourusername.github.io/ant-colony-shortest-path/
```

Demo TSP:
```
https://yourusername.github.io/ant-colony-shortest-path/demo/tsp_europe_tour.html
```

## Local Development

Để test local trước khi push:

```bash
# Chạy simple HTTP server
cd web
python -m http.server 8000

# Mở browser
open http://localhost:8000
```

## Cập nhật Demo

Khi chạy TSP example, file HTML sẽ tự động được tạo/cập nhật:

```bash
# Từ root directory
poetry run python examples/example_tsp_europe.py

# File được lưu tại: web/demo/tsp_europe_tour.html
```

## Features

### Trang chủ (index.html)
- Overview về dự án ACO
- Links đến demos
- Statistics và kết quả
- Quick start guide
- Links đến documentation

### 🎮 Interactive Playground (playground.html) ⭐ NEW!
**Real-time ACO simulation với Leaflet maps**

- **Cấu hình tham số live:**
  - Số kiến (n_ants): 10-100
  - Số iterations: 10-200
  - Alpha (pheromone weight): 0.1-3.0
  - Beta (heuristic weight): 1.0-10.0
  - Evaporation rate: 0.05-0.5
  - Animation speed: 10-500ms

- **Chọn thành phố:**
  - Start city selection
  - Number of cities: 10/15/20/30

- **Real-time visualization:**
  - Interactive Leaflet map với OpenStreetMap tiles
  - City markers (green = start, blue = others)
  - Best tour visualization (red line)
  - Pheromone trails (blue fading lines)
  - Click markers để xem city info

- **Live statistics:**
  - Current iteration
  - Best distance found
  - Improvement percentage
  - Active ants count
  - Paths found
  - Average distance
  - Elapsed time

- **Controls:**
  - Start/Pause/Resume/Reset
  - Step-by-step execution
  - Progress bar
  - Convergence chart (Chart.js)
  - Console log real-time

- **Technologies:**
  - Pure JavaScript ACO implementation
  - Leaflet.js for interactive maps
  - Chart.js for convergence plot
  - Haversine distance calculation

### TSP Europe Tour Demo
- Interactive map với 30 thành phố châu Âu
- Folium + Leaflet.js
- Click markers để xem thông tin
- Tour visualization với màu sắc
- Total distance: 13,216.69 km

## Technologies

- **HTML/CSS/JavaScript**: Frontend
- **Folium**: Python library tạo interactive maps
- **Leaflet.js**: JavaScript mapping library
- **OpenStreetMap**: Map tiles

## Deploy

Mỗi lần push lên GitHub, GitHub Pages sẽ tự động deploy:

```bash
git add web/
git commit -m "Update web demo"
git push origin main

# Đợi 1-2 phút để GitHub Pages rebuild
```

## Troubleshooting

### Demo không hiển thị

1. Check `.nojekyll` file có tồn tại
2. Verify đường dẫn trong `index.html` đúng (relative paths)
3. Check browser console cho errors
4. Đảm bảo GitHub Pages đã enabled

### Map không load

1. Check file `tsp_europe_tour.html` có tồn tại
2. Verify CDN links trong HTML (Leaflet, jQuery, etc.)
3. Check browser network tab

## License

MIT License - Kinhluan, SGU
