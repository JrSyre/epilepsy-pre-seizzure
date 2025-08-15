document.addEventListener('DOMContentLoaded', function() {
  // Hamburger menu (from main.js)
  const form = document.getElementById('medication-form');
  const statusBox = document.getElementById('medication-status');
  const listBox = document.getElementById('medication-list');

  function fetchMedication() {
    fetch('/api/medication')
      .then(res => res.json())
      .then(data => {
        const items = Array.isArray(data) ? data : (data.medications || []);
        if (items.length > 0) {
          listBox.innerHTML = items.map(med => `
            <div class="medication-card">
              <div><strong>Patient:</strong> ${med.patient}</div>
              <div><strong>Drug:</strong> ${med.drug_name}</div>
              <div><strong>Dosage:</strong> ${med.dosage}</div>
              <div><strong>Instructions:</strong> ${med.instructions || '-'}</div>
              <div><strong>Times:</strong> ${Array.isArray(med.times) ? med.times.join(', ') : med.times}</div>
            </div>
          `).join('');
        } else {
          listBox.innerHTML = '<em>No medication schedules found.</em>';
        }
      })
      .catch(() => {
        listBox.innerHTML = '<em>Could not load medication schedules.</em>';
      });
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    statusBox.style.display = 'none';
    statusBox.textContent = '';
    const data = {
      patient: form.patient.value,
      drug_name: form.drug_name.value,
      dosage: form.dosage.value,
      instructions: form.instructions.value,
      times: form.times.value.split(',').map(t => t.trim())
    };
    fetch('/api/medication', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
      statusBox.style.display = 'block';
      if (resp.error) {
        statusBox.className = 'status-box error';
        statusBox.textContent = resp.message || 'Failed to schedule medication.';
      } else {
        statusBox.className = 'status-box success';
        statusBox.textContent = 'Medication scheduled!';
        form.reset();
        fetchMedication();
      }
    })
    .catch(() => {
      statusBox.style.display = 'block';
      statusBox.className = 'status-box error';
      statusBox.textContent = 'Error contacting backend.';
    });
  });

  fetchMedication();
});