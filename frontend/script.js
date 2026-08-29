// Initialize map
const map = L.map('map').setView([12.9716, 77.5946], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

L.marker([12.9716, 77.5946]).addTo(map).bindPopup("Intersection A");
L.marker([12.9800, 77.6000]).addTo(map).bindPopup("Intersection B");

// Fetch REAL data from backend
async function loadTrafficData() {
  try {
    const response = await fetch('https://smart-traffic-system-g74d.onrender.com/predict');
    const data = await response.json();

    document.getElementById('congestion-a').innerText =
      `${data.intersection_a.status} (${data.intersection_a.congestion_percent}%)`;

    document.getElementById('congestion-b').innerText =
      `${data.intersection_b.status} (${data.intersection_b.congestion_percent}%)`;

    document.getElementById('signal-status').innerText =
      `Green: ${data.recommended_signal_timing.green_seconds}s`;

  } catch (error) {
    console.error("Error fetching traffic data:", error);
    document.getElementById('congestion-a').innerText = "Backend not connected ❌";
  }
}

// Load once immediately
loadTrafficData();

// Refresh every 5 seconds (live effect)
setInterval(loadTrafficData, 5000);