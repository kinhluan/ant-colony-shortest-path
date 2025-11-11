"""
Visualization functions for TSP (Traveling Salesman Problem)
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    print("Warning: folium not installed. Interactive maps will not be available.")


def plot_tsp_tour(
    cities: Dict,
    tour: List[str],
    title: str = "TSP Tour - European Cities",
    figsize: tuple = (16, 12),
    save_path: Optional[str] = None
):
    """
    Vẽ TSP tour trên bản đồ với matplotlib.

    Parameters:
    -----------
    cities : Dict
        Cities data với coordinates
    tour : List[str]
        Tour (danh sách cities)
    title : str
        Title của plot
    figsize : tuple
        Figure size
    save_path : str, optional
        Path để save figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Extract coordinates
    lats = [cities[city]['lat'] for city in cities.keys()]
    lons = [cities[city]['lon'] for city in cities.keys()]

    # Plot all cities
    ax.scatter(lons, lats, c='lightblue', s=300, zorder=5,
               edgecolors='black', linewidths=2, alpha=0.7, label='Cities')

    # Plot tour path
    if tour:
        tour_lons = [cities[city]['lon'] for city in tour]
        tour_lats = [cities[city]['lat'] for city in tour]

        ax.plot(tour_lons, tour_lats, 'r-', linewidth=2.5, alpha=0.7, zorder=3, label='Tour')

        # Arrows để chỉ hướng
        for i in range(len(tour) - 1):
            city_a = tour[i]
            city_b = tour[i + 1]

            lon_a, lat_a = cities[city_a]['lon'], cities[city_a]['lat']
            lon_b, lat_b = cities[city_b]['lon'], cities[city_b]['lat']

            # Small arrow in the middle
            mid_lon = (lon_a + lon_b) / 2
            mid_lat = (lat_a + lat_b) / 2
            dx = lon_b - lon_a
            dy = lat_b - lat_a

            ax.annotate('', xy=(mid_lon + dx*0.1, mid_lat + dy*0.1),
                       xytext=(mid_lon - dx*0.1, mid_lat - dy*0.1),
                       arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                       zorder=4)

        # Highlight start city
        start_city = tour[0]
        ax.scatter([cities[start_city]['lon']], [cities[start_city]['lat']],
                  c='green', s=500, marker='*', zorder=6,
                  edgecolors='darkgreen', linewidths=3, label='Start/End')

    # City labels
    for city, data in cities.items():
        ax.text(data['lon'], data['lat'], f"  {city}",
               fontsize=9, ha='left', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

    ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=12)

    # Set aspect ratio to show Europe properly
    ax.set_aspect('equal', adjustable='box')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Tour visualization saved to {save_path}")

    plt.show()


def plot_tsp_comparison(
    cities: Dict,
    tours: Dict[str, List[str]],
    distances: Dict[str, float],
    title: str = "TSP Tour Comparison",
    figsize: tuple = (20, 10)
):
    """
    So sánh nhiều tours trên cùng một figure.

    Parameters:
    -----------
    cities : Dict
        Cities data
    tours : Dict[str, List[str]]
        Dictionary {method_name: tour}
    distances : Dict[str, float]
        Dictionary {method_name: distance}
    title : str
        Title
    figsize : tuple
        Figure size
    """
    n_tours = len(tours)
    fig, axes = plt.subplots(1, n_tours, figsize=figsize)

    if n_tours == 1:
        axes = [axes]

    colors = ['red', 'blue', 'green', 'orange', 'purple']

    for idx, (method, tour) in enumerate(tours.items()):
        ax = axes[idx]

        # Extract coordinates
        lons = [cities[city]['lon'] for city in cities.keys()]
        lats = [cities[city]['lat'] for city in cities.keys()]

        # Plot cities
        ax.scatter(lons, lats, c='lightblue', s=200, zorder=5,
                  edgecolors='black', linewidths=1.5, alpha=0.7)

        # Plot tour
        tour_lons = [cities[city]['lon'] for city in tour]
        tour_lats = [cities[city]['lat'] for city in tour]

        color = colors[idx % len(colors)]
        ax.plot(tour_lons, tour_lats, color=color, linewidth=2, alpha=0.7, zorder=3)

        # Start city
        start_city = tour[0]
        ax.scatter([cities[start_city]['lon']], [cities[start_city]['lat']],
                  c='green', s=400, marker='*', zorder=6,
                  edgecolors='darkgreen', linewidths=2)

        # Title với distance
        distance = distances[method]
        ax.set_title(f"{method}\nDistance: {distance:.2f} km",
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal', adjustable='box')

    fig.suptitle(title, fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def plot_interactive_tour(
    cities: Dict,
    tour: List[str],
    distance: float,
    save_path: str = "tsp_tour_map.html"
) -> Optional[object]:
    """
    Tạo interactive map với Folium.

    Parameters:
    -----------
    cities : Dict
        Cities data
    tour : List[str]
        Tour
    distance : float
        Total distance
    save_path : str
        HTML file path to save

    Returns:
    --------
    folium.Map hoặc None nếu folium không available
    """
    if not FOLIUM_AVAILABLE:
        print("Folium not available. Please install: poetry add folium")
        return None

    # Calculate center of Europe
    avg_lat = np.mean([data['lat'] for data in cities.values()])
    avg_lon = np.mean([data['lon'] for data in cities.values()])

    # Create map
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4,
                   tiles='OpenStreetMap')

    # Add markers for all cities
    for city, data in cities.items():
        # Check if in tour
        if city in tour:
            tour_index = tour.index(city)
            color = 'green' if tour_index == 0 else 'red'
            icon = 'star' if tour_index == 0 else 'info-sign'
            popup_text = f"<b>{city}</b><br>Stop #{tour_index + 1}"
        else:
            color = 'gray'
            icon = 'info-sign'
            popup_text = f"<b>{city}</b><br>Not in tour"

        folium.Marker(
            location=[data['lat'], data['lon']],
            popup=folium.Popup(popup_text, max_width=200),
            tooltip=city,
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)

    # Add tour path
    if tour:
        tour_coords = [[cities[city]['lat'], cities[city]['lon']] for city in tour]

        folium.PolyLine(
            tour_coords,
            color='red',
            weight=3,
            opacity=0.7,
            popup=f"Total Distance: {distance:.2f} km"
        ).add_to(m)

        # Add arrows
        for i in range(len(tour) - 1):
            city_a = tour[i]
            city_b = tour[i + 1]

            lat_a, lon_a = cities[city_a]['lat'], cities[city_a]['lon']
            lat_b, lon_b = cities[city_b]['lat'], cities[city_b]['lon']

            # Arrow in the middle
            mid_lat = (lat_a + lat_b) / 2
            mid_lon = (lon_a + lon_b) / 2

            folium.CircleMarker(
                location=[mid_lat, mid_lon],
                radius=3,
                color='darkred',
                fill=True,
                fillColor='darkred',
                fillOpacity=0.8
            ).add_to(m)

    # Add legend
    legend_html = f"""
    <div style="position: fixed;
                top: 10px; right: 10px; width: 250px; height: 140px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
    <p><b>TSP Tour - European Cities</b></p>
    <p>🟢 Start/End City</p>
    <p>🔴 Visited Cities</p>
    <p>⚪ Not in Tour</p>
    <p><b>Total Distance: {distance:.2f} km</b></p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save map
    m.save(save_path)
    print(f"\n✓ Interactive map saved to: {save_path}")
    print(f"  Open this file in your web browser to view the interactive map!")

    return m


def plot_tour_statistics(
    cities: Dict,
    tour: List[str],
    distance: float,
    figsize: tuple = (14, 8)
):
    """
    Vẽ statistics và analysis của tour.

    Parameters:
    -----------
    cities : Dict
        Cities data
    tour : List[str]
        Tour
    distance : float
        Total distance
    figsize : tuple
        Figure size
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # 1. Distance per segment
    ax1 = axes[0, 0]
    from .tsp_utils import haversine_distance

    segments = []
    segment_distances = []
    for i in range(len(tour) - 1):
        city_a = tour[i]
        city_b = tour[i + 1]
        dist = haversine_distance(
            cities[city_a]['lat'], cities[city_a]['lon'],
            cities[city_b]['lat'], cities[city_b]['lon']
        )
        segments.append(f"{city_a[:3]}-{city_b[:3]}")
        segment_distances.append(dist)

    ax1.bar(range(len(segments)), segment_distances, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Segment', fontweight='bold')
    ax1.set_ylabel('Distance (km)', fontweight='bold')
    ax1.set_title('Distance per Segment', fontweight='bold')
    ax1.tick_params(axis='x', rotation=90, labelsize=8)
    ax1.grid(True, alpha=0.3, axis='y')

    # 2. Country distribution
    ax2 = axes[0, 1]
    countries = {}
    for city in tour[:-1]:  # Exclude last (same as first)
        country = cities[city].get('country', 'Unknown')
        countries[country] = countries.get(country, 0) + 1

    ax2.pie(countries.values(), labels=countries.keys(), autopct='%1.1f%%',
           startangle=90, colors=plt.cm.Pastel1.colors)
    ax2.set_title('Countries Visited', fontweight='bold')

    # 3. Cumulative distance
    ax3 = axes[1, 0]
    cumulative = [0]
    for dist in segment_distances:
        cumulative.append(cumulative[-1] + dist)

    ax3.plot(range(len(cumulative)), cumulative, 'b-o', linewidth=2, markersize=4)
    ax3.set_xlabel('Stop Number', fontweight='bold')
    ax3.set_ylabel('Cumulative Distance (km)', fontweight='bold')
    ax3.set_title('Cumulative Distance Progress', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=distance, color='r', linestyle='--', label=f'Total: {distance:.2f} km')
    ax3.legend()

    # 4. Summary statistics
    ax4 = axes[1, 1]
    ax4.axis('off')

    stats_text = f"""
    TSP TOUR STATISTICS
    {'='*35}

    Total Cities:        {len(tour) - 1}
    Total Distance:      {distance:.2f} km

    Average Segment:     {np.mean(segment_distances):.2f} km
    Max Segment:         {np.max(segment_distances):.2f} km
    Min Segment:         {np.min(segment_distances):.2f} km

    Countries Visited:   {len(countries)}

    Start/End City:      {tour[0]}
    """

    ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.show()
