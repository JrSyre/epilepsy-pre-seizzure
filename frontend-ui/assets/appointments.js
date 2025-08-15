document.addEventListener('DOMContentLoaded', function() {
  // Hamburger menu (from main.js)
  const form = document.getElementById('appointment-form');
  const statusBox = document.getElementById('appointment-status');
  const listBox = document.getElementById('appointments-list');

  function fetchAppointments() {
    fetch('/api/appointments')
      .then(res => res.json())
      .then(data => {
        const items = Array.isArray(data) ? data : (data.appointments || []);
        if (items.length > 0) {
          listBox.innerHTML = items.map(appt => `
            <div class="appointment-card">
              <div><strong>Patient:</strong> ${appt.patient}</div>
              <div><strong>Doctor:</strong> ${appt.doctor}</div>
              <div><strong>Date:</strong> ${appt.date}</div>
              <div><strong>Time:</strong> ${appt.time}</div>
            </div>
          `).join('');
        } else {
          listBox.innerHTML = '<em>No appointments found.</em>';
        }
      })
      .catch(() => {
        listBox.innerHTML = '<em>Could not load appointments.</em>';
      });
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    statusBox.style.display = 'none';
    statusBox.textContent = '';
    const data = {
      patient: form.patient.value,
      doctor: form.doctor.value,
      date: form.date.value,
      time: form.time.value
    };
    fetch('/api/appointments', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
      statusBox.style.display = 'block';
      if (resp.error) {
        statusBox.className = 'status-box error';
        statusBox.textContent = resp.message || 'Failed to book appointment.';
      } else {
        statusBox.className = 'status-box success';
        statusBox.textContent = 'Appointment booked!';
        form.reset();
        fetchAppointments();
      }
    })
    .catch(() => {
      statusBox.style.display = 'block';
      statusBox.className = 'status-box error';
      statusBox.textContent = 'Error contacting backend.';
    });
  });

  fetchAppointments();
});