const map = L.map('map').setView([47.6, 14.1], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; OpenStreetMap contributors'}).addTo(map);

const legend = document.getElementById('legend');
const info = document.getElementById('info');
const forecastBox = document.getElementById('forecast');
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleSidebar');

toggleBtn.addEventListener('click', () => {
  const isHidden = sidebar.classList.toggle('hidden');
  toggleBtn.textContent = isHidden ? 'Show sidebar' : 'Hide sidebar';
  toggleBtn.setAttribute('aria-expanded', String(!isHidden));
});

function colorForClass(cls) {
  const palette = ['#f7fbff','#c6dbef','#6baed6','#3182bd','#08519c','#08306b'];
  const idx = Math.max(0, Math.min(palette.length - 1, (cls ?? 0)));
  return palette[idx];
}

function renderLegend() {
  legend.innerHTML = '';
  for (let i = 0; i < 6; i++) {
    const step = document.createElement('div');
    step.className = 'legend-step';
    step.style.background = colorForClass(i);
    legend.appendChild(step);
  }
}
renderLegend();

let layer;
fetch('/api/neighborhoods')
  .then(r => r.json())
  .then(geojson => {
    layer = L.geoJSON(geojson, {
      style: f => ({ color: '#333', weight: 1, fillColor: colorForClass(f.properties.lst_class), fillOpacity: 0.65 }),
      onEachFeature: (feature, lyr) => { lyr.on('click', () => onFeatureClick(feature, lyr)); }
    }).addTo(map);
    map.fitBounds(layer.getBounds(), { padding: [20, 20] });
  });

function formatMetric(v, suffix = '') { return (v == null ? '—' : v.toFixed(2) + suffix); }

function onFeatureClick(feature, lyr) {
  const { name, lst_mean, lst_min, lst_max, id } = feature.properties;
  const center = lyr.getBounds().getCenter();

  // Make sure sidebar is visible
  sidebar.classList.remove('hidden');
  toggleBtn.textContent = 'Hide sidebar';
  toggleBtn.setAttribute('aria-expanded', 'true');

  // Loading states
  info.innerHTML = `<em>Loading current weather…</em>`;
  forecastBox.innerHTML = `<h3>5-Day Forecast</h3><div><em>Loading forecast…</em></div>`;

  // Current weather
  fetch(`/api/weather?lat=${center.lat}&lon=${center.lng}`)
    .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then(wx => {
      const html = `
        <table class="popup-table">
          <tr><td><strong>${name} (${id})</strong></td><td></td></tr>
          <tr><td>LST mean</td><td>${formatMetric(lst_mean, ' °C')}</td></tr>
          <tr><td>LST min</td><td>${formatMetric(lst_min, ' °C')}</td></tr>
          <tr><td>LST max</td><td>${formatMetric(lst_max, ' °C')}</td></tr>
          <tr><td>Air temperature</td><td>${wx.temperature ?? '—'} ${wx.units?.temperature_2m ?? ''}</td></tr>
          <tr><td>Apparent</td><td>${wx.apparent_temperature ?? '—'} ${wx.units?.apparent_temperature ?? ''}</td></tr>
          <tr><td>Humidity</td><td>${wx.humidity ?? '—'} ${wx.units?.relative_humidity_2m ?? ''}</td></tr>
          <tr><td>Wind</td><td>${wx.wind_speed ?? '—'} ${wx.units?.wind_speed_10m ?? ''}</td></tr>
        </table>`;
      lyr.bindPopup(html, { maxWidth: 360 }).openPopup();
      info.innerHTML = html;
    })
    .catch(err => {
      console.error("Current weather failed:", err);
      info.innerHTML = `<strong>${name} (${id})</strong><br/>Current weather unavailable.`;
      lyr.bindPopup(`<b>${name}</b><br/>Current weather unavailable.`).openPopup();
    });

  // 5-day forecast
  fetch(`/api/forecast?lat=${center.lat}&lon=${center.lng}&days=5`)
    .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then(fc => {
      const d = fc.daily || {};
      const dates = d.time || [];
      const tmax = d.temperature_2m_max || [];
      const tmin = d.temperature_2m_min || [];
      const prcp = d.precipitation_sum || [];
      if (!dates.length) {
        console.warn("No forecast dates returned:", fc);
        forecastBox.innerHTML = '<h3>5-Day Forecast</h3><div>No data available.</div>';
        return;
      }
      let rows = '';
      for (let i = 0; i < dates.length; i++) {
        rows += `<tr><td>${dates[i]}</td><td>${tmin[i] ?? '—'} / ${tmax[i] ?? '—'} °C</td><td>${prcp[i] ?? '—'} mm</td></tr>`;
      }
      forecastBox.innerHTML = `<h3>5-Day Forecast</h3>
        <table><thead><tr><th>Date</th><th>Min/Max</th><th>Precipitation</th></tr></thead>
        <tbody>${rows}</tbody></table>`;
    })
    .catch(err => {
      console.error("Forecast fetch failed:", err);
      forecastBox.innerHTML = '<h3>5-Day Forecast</h3><div>Forecast unavailable.</div>';
    });
}
