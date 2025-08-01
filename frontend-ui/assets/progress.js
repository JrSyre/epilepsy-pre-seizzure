document.addEventListener('DOMContentLoaded', function() {
  // Hamburger menu (from main.js)
  const form = document.getElementById('progress-form');
  const statusBox = document.getElementById('progress-status');
  const listBox = document.getElementById('progress-list');

  function fetchProgress() {
    fetch('/progress')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          listBox.innerHTML = data.map(log => `
            <div class="progress-card${log.occurred ? ' occurred' : ''}">
              <div><strong>Date:</strong> ${log.date}</div>
              <div><strong>Patient:</strong> ${log.patient}</div>
              <div><strong>Occurred:</strong> ${log.occurred ? '<span class="badge occurred">Yes</span>' : '<span class="badge">No</span>'}</div>
              <div><strong>Notes:</strong> ${log.notes || '-'}</div>
            </div>
          `).join('');
        } else {
          listBox.innerHTML = '<em>No progress logs found.</em>';
        }
      })
      .catch(() => {
        listBox.innerHTML = '<em>Could not load progress logs.</em>';
      });
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    statusBox.style.display = 'none';
    statusBox.textContent = '';
    const data = {
      date: form.date.value,
      patient: form.patient.value,
      occurred: parseInt(form.occurred.value, 10),
      notes: form.notes.value
    };
    fetch('/progress', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
      statusBox.style.display = 'block';
      if (resp.error) {
        statusBox.className = 'status-box error';
        statusBox.textContent = resp.message || 'Failed to log progress.';
      } else {
        statusBox.className = 'status-box success';
        statusBox.textContent = 'Progress logged!';
        form.reset();
        fetchProgress();
      }
    })
    .catch(() => {
      statusBox.style.display = 'block';
      statusBox.className = 'status-box error';
      statusBox.textContent = 'Error contacting backend.';
    });
  });

  fetchProgress();
});