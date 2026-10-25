/*const $ = (id) => document.getElementById(id);
let currentLocation = null;

function setStatus(id, message, kind = '') {
  const element = $(id);
  if (!element) return;
  element.textContent = message;
  element.classList.remove('success', 'error');
  if (kind) element.classList.add(kind);
}

function toast(message) {
  const element = $('toast');
  element.textContent = message;
  element.hidden = false;
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => { element.hidden = true; }, 3500);
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  let data;
  try { data = await response.json(); } catch { data = {}; }
  if (!response.ok) throw new Error(data.detail || 'Request failed. Please try again.');
  return data;
}

$('locationButton').addEventListener('click', () => {
  if (!navigator.geolocation) {
    setStatus('locationStatus', 'Geolocation is not supported by this browser.', 'error');
    return;
  }
  setStatus('locationStatus', 'Requesting location permission…');
  navigator.geolocation.getCurrentPosition(
    (position) => {
      currentLocation = { latitude: position.coords.latitude, longitude: position.coords.longitude };
      setStatus('locationStatus', `Location ready: ${currentLocation.latitude.toFixed(5)}, ${currentLocation.longitude.toFixed(5)}`, 'success');
      toast('Location captured in this browser session.');
    },
    (error) => {
      currentLocation = null;
      const message = error.code === 1 ? 'Location permission was denied.' : 'Unable to get location. Try HTTPS or localhost and check browser permissions.';
      setStatus('locationStatus', message, 'error');
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 30000 }
  );
});

$('sosButton').addEventListener('click', async () => {
  const button = $('sosButton');
  button.disabled = true;
  setStatus('sosStatus', 'Recording demo SOS alert…');
  try {
    const result = await request('/api/sos', { method: 'POST', body: JSON.stringify(currentLocation || {}) });
    setStatus('sosStatus', result.message, 'success');
    toast('Demo SOS alert recorded.');
    await refreshHistory();
  } catch (error) {
    setStatus('sosStatus', error.message, 'error');
  } finally { button.disabled = false; }
});

$('checkinForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  setStatus('checkinStatus', 'Saving check-in…');
  try {
    const result = await request('/api/checkin', { method: 'POST', body: JSON.stringify({ name: $('checkinName').value.trim() }) });
    setStatus('checkinStatus', result.message, 'success');
    toast('Safety check-in recorded.');
    await refreshHistory();
  } catch (error) { setStatus('checkinStatus', error.message, 'error'); }
});

$('incidentForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitButton = $('incidentForm').querySelector('button[type="submit"]');
  submitButton.disabled = true;
  setStatus('reportStatus', 'Submitting report…');
  const payload = {
    category: $('category').value,
    description: $('description').value.trim(),
    location: $('incidentLocation').value.trim(),
  };
  try {
    const result = await request('/api/incidents', { method: 'POST', body: JSON.stringify(payload) });
    setStatus('reportStatus', result.message, 'success');
    $('incidentForm').reset();
    toast('Incident report recorded.');
    await refreshHistory();
  } catch (error) { setStatus('reportStatus', error.message, 'error'); }
  finally { submitButton.disabled = false; }
});

function formatTime(value) {
  try { return new Date(value).toLocaleString(); } catch { return value || ''; }
}

function escapeText(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
}

function renderHistory(items) {
  const container = $('alertHistory');
  if (!items || items.length === 0) {
    container.innerHTML = '<p class="empty-state">No activity recorded yet. Use a safety tool or submit an incident report.</p>';
    return;
  }
  container.innerHTML = items.map((item) => {
    const details = item.details || {};
    const extra = [];
    if (details.category) extra.push(`<strong>Category:</strong> ${escapeText(details.category)}`);
    if (details.location) extra.push(`<strong>Location:</strong> ${escapeText(details.location)}`);
    if (details.latitude != null && details.longitude != null) extra.push(`<strong>Coordinates:</strong> ${escapeText(details.latitude)}, ${escapeText(details.longitude)}`);
    if (details.description) extra.push(`<span>${escapeText(details.description)}</span>`);
    return `<article class="history-item"><div class="history-item-top"><span class="history-type">${escapeText(item.type)}</span><time class="history-time">${escapeText(formatTime(item.timestamp))}</time></div><p>${escapeText(item.message)}</p>${extra.length ? `<p class="history-detail">${extra.join('<br>')}</p>` : ''}</article>`;
  }).join('');
}

async function refreshHistory() {
  const container = $('alertHistory');
  try {
    const data = await request('/api/history');
    renderHistory(data.items || []);
  } catch (error) {
    container.innerHTML = `<p class="empty-state">Could not load history: ${escapeText(error.message)}. Check that the server is running.</p>`;
  }
}

$('refreshButton').addEventListener('click', refreshHistory);
refreshHistory();
*/







const $ = (id) => document.getElementById(id);
let currentLocation = null;

function setStatus(id, message, kind = '') {
  const element = $(id);
  if (!element) return;
  element.textContent = message;
  element.classList.remove('success', 'error');
  if (kind) element.classList.add(kind);
}

function toast(message) {
  const element = $('toast');
  element.textContent = message;
  element.hidden = false;
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => { element.hidden = true; }, 3500);
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  let data;
  try { data = await response.json(); } catch { data = {}; }
  if (!response.ok) throw new Error(data.detail || 'Request failed. Please try again.');
  return data;
}

$('locationButton').addEventListener('click', () => {
  if (!navigator.geolocation) {
    setStatus('locationStatus', 'Geolocation is not supported by this browser.', 'error');
    return;
  }
  setStatus('locationStatus', 'Requesting location permission…');
  navigator.geolocation.getCurrentPosition(
    (position) => {
      currentLocation = { latitude: position.coords.latitude, longitude: position.coords.longitude };
      setStatus('locationStatus', `Location ready: ${currentLocation.latitude.toFixed(5)}, ${currentLocation.longitude.toFixed(5)}`, 'success');
      toast('Location captured in this browser session.');
    },
    (error) => {
      currentLocation = null;
      const message = error.code === 1 ? 'Location permission was denied.' : 'Unable to get location. Try HTTPS or localhost and check browser permissions.';
      setStatus('locationStatus', message, 'error');
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 30000 }
  );
});

$('sosButton').addEventListener('click', async () => {
  const button = $('sosButton');
  button.disabled = true;
  setStatus('sosStatus', 'Recording demo SOS alert…');
  try {
    const result = await request('/api/sos', { method: 'POST', body: JSON.stringify(currentLocation || {}) });
    setStatus('sosStatus', result.message, 'success');
    toast('Demo SOS alert recorded.');
    await refreshHistory();
  } catch (error) {
    setStatus('sosStatus', error.message, 'error');
  } finally { button.disabled = false; }
});

$('checkinForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  setStatus('checkinStatus', 'Saving check-in…');
  try {
    const result = await request('/api/checkin', { method: 'POST', body: JSON.stringify({ name: $('checkinName').value.trim() }) });
    setStatus('checkinStatus', result.message, 'success');
    toast('Safety check-in recorded.');
    await refreshHistory();
  } catch (error) { setStatus('checkinStatus', error.message, 'error'); }
});

$('incidentForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitButton = $('incidentForm').querySelector('button[type="submit"]');
  submitButton.disabled = true;
  setStatus('reportStatus', 'Submitting report…');
  const payload = {
    category: $('category').value,
    description: $('description').value.trim(),
    location: $('incidentLocation').value.trim(),
  };
  try {
    const result = await request('/api/incidents', { method: 'POST', body: JSON.stringify(payload) });
    setStatus('reportStatus', result.message, 'success');
    $('incidentForm').reset();
    toast('Incident report recorded.');
    await refreshHistory();
  } catch (error) { setStatus('reportStatus', error.message, 'error'); }
  finally { submitButton.disabled = false; }
});

function formatTime(value) {
  try { return new Date(value).toLocaleString(); } catch { return value || ''; }
}

function escapeText(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
}

function renderHistory(items) {
  const container = $('alertHistory');
  if (!items || items.length === 0) {
    container.innerHTML = '<p class="empty-state">No activity recorded yet. Use a safety tool or submit an incident report.</p>';
    return;
  }
  container.innerHTML = items.map((item) => {
    const details = item.details || {};
    const extra = [];
    if (details.category) extra.push(`<strong>Category:</strong> ${escapeText(details.category)}`);
    if (details.location) extra.push(`<strong>Location:</strong> ${escapeText(details.location)}`);
    if (details.latitude != null && details.longitude != null) extra.push(`<strong>Coordinates:</strong> ${escapeText(details.latitude)}, ${escapeText(details.longitude)}`);
    if (details.description) extra.push(`<span>${escapeText(details.description)}</span>`);
    return `<article class="history-item"><div class="history-item-top"><span class="history-type">${escapeText(item.type)}</span><time class="history-time">${escapeText(formatTime(item.timestamp))}</time></div><p>${escapeText(item.message)}</p>${extra.length ? `<p class="history-detail">${extra.join('<br>')}</p>` : ''}</article>`;
  }).join('');
}

async function refreshHistory() {
  const container = $('alertHistory');
  try {
    const data = await request('/api/history');
    renderHistory(data.items || []);
  } catch (error) {
    container.innerHTML = `<p class="empty-state">Could not load history: ${escapeText(error.message)}. Check that the server is running.</p>`;
  }
}

$('refreshButton').addEventListener('click', refreshHistory);

// Load history when the page opens
refreshHistory();

// Automatically update alert history every 3 seconds
setInterval(() => {
  refreshHistory();
}, 3000);


