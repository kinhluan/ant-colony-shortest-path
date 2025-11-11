// European Cities Data (simplified for demo)
const CITIES_DATA = {
    'Paris': { lat: 48.8566, lon: 2.3522, country: 'France' },
    'London': { lat: 51.5074, lon: -0.1278, country: 'United Kingdom' },
    'Berlin': { lat: 52.52, lon: 13.405, country: 'Germany' },
    'Madrid': { lat: 40.4168, lon: -3.7038, country: 'Spain' },
    'Rome': { lat: 41.9028, lon: 12.4964, country: 'Italy' },
    'Vienna': { lat: 48.2082, lon: 16.3738, country: 'Austria' },
    'Amsterdam': { lat: 52.3676, lon: 4.9041, country: 'Netherlands' },
    'Brussels': { lat: 50.8503, lon: 4.3517, country: 'Belgium' },
    'Prague': { lat: 50.0755, lon: 14.4378, country: 'Czech Republic' },
    'Barcelona': { lat: 41.3851, lon: 2.1734, country: 'Spain' },
    'Budapest': { lat: 47.4979, lon: 19.0402, country: 'Hungary' },
    'Munich': { lat: 48.1351, lon: 11.582, country: 'Germany' },
    'Milan': { lat: 45.4642, lon: 9.19, country: 'Italy' },
    'Copenhagen': { lat: 55.6761, lon: 12.5683, country: 'Denmark' },
    'Stockholm': { lat: 59.3293, lon: 18.0686, country: 'Sweden' },
    'Warsaw': { lat: 52.2297, lon: 21.0122, country: 'Poland' },
    'Lisbon': { lat: 38.7223, lon: -9.1393, country: 'Portugal' },
    'Dublin': { lat: 53.3498, lon: -6.2603, country: 'Ireland' },
    'Athens': { lat: 37.9838, lon: 23.7275, country: 'Greece' },
    'Oslo': { lat: 59.9139, lon: 10.7522, country: 'Norway' },
    'Helsinki': { lat: 60.1699, lon: 24.9384, country: 'Finland' },
    'Zurich': { lat: 47.3769, lon: 8.5417, country: 'Switzerland' },
    'Hamburg': { lat: 53.5511, lon: 9.9937, country: 'Germany' },
    'Lyon': { lat: 45.764, lon: 4.8357, country: 'France' },
    'Krakow': { lat: 50.0647, lon: 19.945, country: 'Poland' },
    'Seville': { lat: 37.3891, lon: -5.9845, country: 'Spain' },
    'Frankfurt': { lat: 50.1109, lon: 8.6821, country: 'Germany' },
    'Cologne': { lat: 50.9375, lon: 6.9603, country: 'Germany' },
    'Edinburgh': { lat: 55.9533, lon: -3.1883, country: 'United Kingdom' },
    'Venice': { lat: 45.4408, lon: 12.3155, country: 'Italy' }
};

// Global state
let state = {
    running: false,
    paused: false,
    iteration: 0,
    maxIterations: 50,
    nAnts: 30,
    alpha: 1.0,
    beta: 5.0,
    evaporationRate: 0.1,
    Q: 1000,
    animationSpeed: 100,
    startCity: 'Paris',
    numCities: 30,

    // ACO data
    cities: [],
    distances: {},
    pheromones: {},
    bestTour: null,
    bestDistance: Infinity,
    initialDistance: Infinity,
    history: [],
    currentAnts: [],

    // Leaflet Map
    map: null,
    markers: {},
    tourLine: null,
    pheromoneLines: [],

    // Chart
    chart: null,
    startTime: null
};

// Haversine distance
function haversineDistance(city1, city2) {
    const R = 6371; // Earth radius in km
    const lat1 = city1.lat * Math.PI / 180;
    const lat2 = city2.lat * Math.PI / 180;
    const dLat = (city2.lat - city1.lat) * Math.PI / 180;
    const dLon = (city2.lon - city1.lon) * Math.PI / 180;

    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1) * Math.cos(lat2) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c;
}

// Initialize cities and distances
function initializeData() {
    const allCities = Object.keys(CITIES_DATA);
    const numCities = parseInt(document.getElementById('num-cities').value);

    // Select cities (always include start city)
    const startCity = document.getElementById('start-city').value;
    let selectedCities = [startCity];

    const otherCities = allCities.filter(c => c !== startCity);
    while (selectedCities.length < numCities && otherCities.length > 0) {
        const randomIndex = Math.floor(Math.random() * otherCities.length);
        selectedCities.push(otherCities.splice(randomIndex, 1)[0]);
    }

    state.cities = selectedCities;
    state.startCity = startCity;

    // Calculate distances
    state.distances = {};
    for (let i = 0; i < state.cities.length; i++) {
        for (let j = i + 1; j < state.cities.length; j++) {
            const city1 = state.cities[i];
            const city2 = state.cities[j];
            const dist = haversineDistance(CITIES_DATA[city1], CITIES_DATA[city2]);
            state.distances[`${city1}-${city2}`] = dist;
            state.distances[`${city2}-${city1}`] = dist;
        }
    }

    // Initialize pheromones
    state.pheromones = {};
    for (let i = 0; i < state.cities.length; i++) {
        for (let j = 0; j < state.cities.length; j++) {
            if (i !== j) {
                const key = `${state.cities[i]}-${state.cities[j]}`;
                state.pheromones[key] = 1.0;
            }
        }
    }

    logMessage(`✅ Initialized ${state.cities.length} cities`);
    logMessage(`📍 Starting city: ${state.startCity}`);
}

// Calculate tour distance
function calculateTourDistance(tour) {
    let total = 0;
    for (let i = 0; i < tour.length - 1; i++) {
        const key = `${tour[i]}-${tour[i+1]}`;
        total += state.distances[key] || 0;
    }
    // Return to start
    const lastKey = `${tour[tour.length-1]}-${tour[0]}`;
    total += state.distances[lastKey] || 0;
    return total;
}

// Construct tour for one ant
function constructTour() {
    const tour = [state.startCity];
    const unvisited = new Set(state.cities.filter(c => c !== state.startCity));
    let current = state.startCity;

    while (unvisited.size > 0) {
        const probabilities = {};
        let sum = 0;

        // Calculate probabilities
        for (const nextCity of unvisited) {
            const key = `${current}-${nextCity}`;
            const pheromone = state.pheromones[key] || 1.0;
            const distance = state.distances[key];
            const heuristic = distance > 0 ? 1.0 / distance : 1.0;

            const attractiveness = Math.pow(pheromone, state.alpha) * Math.pow(heuristic, state.beta);
            probabilities[nextCity] = attractiveness;
            sum += attractiveness;
        }

        // Normalize and select
        if (sum === 0) {
            // Random selection if all probabilities are 0
            const arr = Array.from(unvisited);
            current = arr[Math.floor(Math.random() * arr.length)];
        } else {
            let random = Math.random() * sum;
            for (const [city, prob] of Object.entries(probabilities)) {
                random -= prob;
                if (random <= 0) {
                    current = city;
                    break;
                }
            }
        }

        tour.push(current);
        unvisited.delete(current);
    }

    return tour;
}

// Update pheromones
function updatePheromones(tours) {
    // Evaporation
    for (const key in state.pheromones) {
        state.pheromones[key] *= (1 - state.evaporationRate);
    }

    // Deposit
    for (const { tour, distance } of tours) {
        if (distance === Infinity) continue;

        const delta = state.Q / distance;
        for (let i = 0; i < tour.length; i++) {
            const nextI = (i + 1) % tour.length;
            const key = `${tour[i]}-${tour[nextI]}`;
            const reverseKey = `${tour[nextI]}-${tour[i]}`;

            if (state.pheromones[key] !== undefined) {
                state.pheromones[key] += delta;
            }
            if (state.pheromones[reverseKey] !== undefined) {
                state.pheromones[reverseKey] += delta;
            }
        }
    }
}

// Run one iteration
async function runIteration() {
    state.iteration++;

    const tours = [];
    let totalDistance = 0;
    let validTours = 0;

    // Each ant constructs a tour
    for (let i = 0; i < state.nAnts; i++) {
        const tour = constructTour();
        const distance = calculateTourDistance(tour);
        tours.push({ tour, distance });

        if (distance < Infinity) {
            totalDistance += distance;
            validTours++;
        }

        // Update best
        if (distance < state.bestDistance) {
            state.bestDistance = distance;
            state.bestTour = [...tour];

            if (state.initialDistance === Infinity) {
                state.initialDistance = distance;
            }

            logMessage(`🎯 New best: ${distance.toFixed(2)} km at iteration ${state.iteration}`);
        }

        // Animate ant (show briefly)
        await animateAnt(tour);
    }

    // Update pheromones
    updatePheromones(tours);

    // Update statistics
    const avgDistance = validTours > 0 ? totalDistance / validTours : Infinity;
    state.history.push(state.bestDistance);

    updateUI(avgDistance, validTours);
    drawVisualization();
    updateChart();

    // Check if done
    if (state.iteration >= state.maxIterations) {
        stopSimulation();
        logMessage(`✅ Hoàn thành ${state.maxIterations} iterations!`);
        logMessage(`🏆 Best distance: ${state.bestDistance.toFixed(2)} km`);
    }
}

// Animate ant movement
async function animateAnt(tour) {
    // Just a visual effect - show path briefly
    return new Promise(resolve => {
        setTimeout(resolve, state.animationSpeed / state.nAnts);
    });
}

// Initialize Leaflet map
function initializeMap() {
    // Clear existing map if any
    if (state.map) {
        state.map.remove();
    }

    // Create map centered on Europe
    state.map = L.map('map').setView([50, 10], 4);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(state.map);

    // Calculate bounds for cities
    const lats = state.cities.map(c => CITIES_DATA[c].lat);
    const lons = state.cities.map(c => CITIES_DATA[c].lon);
    const bounds = [
        [Math.min(...lats), Math.min(...lons)],
        [Math.max(...lats), Math.max(...lons)]
    ];

    // Fit map to show all cities
    state.map.fitBounds(bounds, { padding: [50, 50] });

    // Add city markers
    state.markers = {};
    for (const city of state.cities) {
        const data = CITIES_DATA[city];
        const isStart = city === state.startCity;

        const marker = L.circleMarker([data.lat, data.lon], {
            radius: isStart ? 10 : 7,
            fillColor: isStart ? '#28a745' : '#667eea',
            color: 'white',
            weight: 2,
            fillOpacity: 0.9
        }).addTo(state.map);

        marker.bindPopup(`
            <div class="city-popup">
                <h4>${city}</h4>
                <p>${data.country}</p>
                <p>📍 ${data.lat.toFixed(2)}, ${data.lon.toFixed(2)}</p>
            </div>
        `);

        state.markers[city] = marker;
    }

    drawVisualization();
}

// Draw visualization on map
function drawVisualization() {
    if (!state.map) return;

    // Remove old tour line if exists
    if (state.tourLine) {
        state.map.removeLayer(state.tourLine);
        state.tourLine = null;
    }

    // Remove old pheromone lines
    state.pheromoneLines.forEach(line => state.map.removeLayer(line));
    state.pheromoneLines = [];

    // Draw pheromone trails (top 10 strongest connections)
    const pheromoneArray = Object.entries(state.pheromones)
        .map(([key, value]) => ({ key, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 20); // Show top 20 connections

    for (const { key, value } of pheromoneArray) {
        const [city1, city2] = key.split('-');
        if (!CITIES_DATA[city1] || !CITIES_DATA[city2]) continue;

        const coords = [
            [CITIES_DATA[city1].lat, CITIES_DATA[city1].lon],
            [CITIES_DATA[city2].lat, CITIES_DATA[city2].lon]
        ];

        const opacity = Math.min(value / 10, 0.5); // Scale opacity
        const line = L.polyline(coords, {
            color: '#667eea',
            weight: 1,
            opacity: opacity
        }).addTo(state.map);

        state.pheromoneLines.push(line);
    }

    // Draw best tour if exists
    if (state.bestTour && state.bestTour.length > 0) {
        const coords = state.bestTour.map(city => {
            const data = CITIES_DATA[city];
            return [data.lat, data.lon];
        });

        // Close the tour
        coords.push(coords[0]);

        state.tourLine = L.polyline(coords, {
            color: '#ff6b6b',
            weight: 3,
            opacity: 0.8,
            smoothFactor: 1
        }).addTo(state.map);

        // Bring tour line to front
        state.tourLine.bringToFront();
    }

    // Bring markers to front
    for (const marker of Object.values(state.markers)) {
        marker.bringToFront();
    }
}

// Update UI
function updateUI(avgDistance, pathsFound) {
    document.getElementById('stat-iteration').textContent = state.iteration;
    document.getElementById('stat-distance').textContent =
        state.bestDistance === Infinity ? '∞' : state.bestDistance.toFixed(2);

    const improvement = state.initialDistance === Infinity ? 0 :
        ((state.initialDistance - state.bestDistance) / state.initialDistance * 100);
    document.getElementById('stat-improvement').textContent = improvement.toFixed(1) + '%';

    document.getElementById('stat-ants-active').textContent = state.nAnts;
    document.getElementById('stat-paths').textContent = pathsFound;
    document.getElementById('stat-avg').textContent =
        avgDistance === Infinity ? '∞' : avgDistance.toFixed(2);

    const elapsed = state.startTime ? ((Date.now() - state.startTime) / 1000).toFixed(1) : 0;
    document.getElementById('stat-time').textContent = elapsed + 's';

    const progress = (state.iteration / state.maxIterations * 100).toFixed(0);
    document.getElementById('progress').style.width = progress + '%';
    document.getElementById('progress').textContent = progress + '%';
}

// Initialize chart
function initializeChart() {
    const ctx = document.getElementById('convergence-chart').getContext('2d');

    if (state.chart) {
        state.chart.destroy();
    }

    state.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Best Distance (km)',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Convergence Plot'
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Update chart
function updateChart() {
    if (!state.chart) return;

    state.chart.data.labels = state.history.map((_, i) => i + 1);
    state.chart.data.datasets[0].data = state.history;
    state.chart.update('none'); // No animation for performance
}

// Log message
function logMessage(msg) {
    const logContainer = document.getElementById('log-container');
    const line = document.createElement('div');
    line.className = 'log-line';
    line.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logContainer.insertBefore(line, logContainer.firstChild);

    // Keep only last 20 messages
    while (logContainer.children.length > 20) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// Event listeners for parameters
function setupParameterListeners() {
    const params = [
        { id: 'ants', value: 'value-ants', state: 'nAnts', parse: parseInt },
        { id: 'iterations', value: 'value-iterations', state: 'maxIterations', parse: parseInt },
        { id: 'alpha', value: 'value-alpha', state: 'alpha', parse: parseFloat },
        { id: 'beta', value: 'value-beta', state: 'beta', parse: parseFloat },
        { id: 'evap', value: 'value-evap', state: 'evaporationRate', parse: parseFloat },
        { id: 'speed', value: 'value-speed', state: 'animationSpeed', parse: parseInt }
    ];

    params.forEach(({ id, value, state: stateKey, parse }) => {
        const input = document.getElementById(`param-${id}`);
        const display = document.getElementById(value);

        input.addEventListener('input', (e) => {
            const val = parse(e.target.value);
            display.textContent = val;
            state[stateKey] = val;
        });
    });
}

// Control buttons
async function startSimulation() {
    if (state.running) return;

    state.running = true;
    state.paused = false;
    state.startTime = Date.now();

    document.getElementById('btn-start').disabled = true;
    document.getElementById('btn-pause').disabled = false;
    document.getElementById('btn-reset').disabled = true;

    logMessage('🚀 Starting ACO simulation...');

    while (state.running && state.iteration < state.maxIterations) {
        if (!state.paused) {
            await runIteration();
            await new Promise(resolve => setTimeout(resolve, state.animationSpeed));
        } else {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
}

function pauseSimulation() {
    state.paused = !state.paused;
    document.getElementById('btn-pause').textContent = state.paused ? '▶️ Resume' : '⏸️ Pause';
    logMessage(state.paused ? '⏸️ Paused' : '▶️ Resumed');
}

function stopSimulation() {
    state.running = false;
    state.paused = false;

    document.getElementById('btn-start').disabled = false;
    document.getElementById('btn-pause').disabled = true;
    document.getElementById('btn-reset').disabled = false;
    document.getElementById('btn-pause').textContent = '⏸️ Pause';
}

function resetSimulation() {
    state.running = false;
    state.paused = false;
    state.iteration = 0;
    state.bestTour = null;
    state.bestDistance = Infinity;
    state.initialDistance = Infinity;
    state.history = [];
    state.startTime = null;

    initializeData();
    initializeMap();
    initializeChart();
    updateUI(Infinity, 0);

    document.getElementById('btn-start').disabled = false;
    document.getElementById('btn-pause').disabled = true;
    document.getElementById('btn-reset').disabled = false;
    document.getElementById('progress').style.width = '0%';
    document.getElementById('progress').textContent = '0%';

    logMessage('🔄 Reset complete');
}

// Initialize on load
window.addEventListener('load', () => {
    setupParameterListeners();

    document.getElementById('btn-start').addEventListener('click', startSimulation);
    document.getElementById('btn-pause').addEventListener('click', pauseSimulation);
    document.getElementById('btn-reset').addEventListener('click', resetSimulation);

    // Initialize with default settings
    resetSimulation();

    logMessage('💡 Ready! Configure parameters and click "Bắt đầu"');
});

// Handle window resize
window.addEventListener('resize', () => {
    if (state.map) {
        state.map.invalidateSize();
    }
});
