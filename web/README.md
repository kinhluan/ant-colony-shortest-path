# Web Demo - GitHub Pages

Thư mục này chứa website và interactive demos cho GitHub Pages.

## Cấu trúc

```
web/
├── index.html           # Trang chủ
├── demo/               # Interactive demos
│   └── tsp_europe_tour.html
├── .nojekyll           # Cho phép Jekyll bypass
└── README.md           # File này
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
