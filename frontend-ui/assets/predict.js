document.addEventListener('DOMContentLoaded', function() {
  // Hamburger menu (from main.js)
  // Prediction form logic
  const form = document.getElementById('predict-form');
  const resultBox = document.getElementById('prediction-result');
  const sampleBtn = document.getElementById('sample-btn');

  sampleBtn.addEventListener('click', function() {
    // Fill with 115 random floats for demo
    const arr = Array.from({length: 115}, () => (Math.random() * 2 - 1).toFixed(3));
    document.getElementById('features').value = arr.join(', ');
  });

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    resultBox.style.display = 'none';
    resultBox.textContent = '';
    const features = document.getElementById('features').value.split(',').map(x => parseFloat(x.trim()));
    if (features.length !== 115 || features.some(isNaN)) {
      resultBox.style.display = 'block';
      resultBox.className = 'status-box error';
      resultBox.textContent = 'Please enter exactly 115 valid numbers.';
      return;
    }
    fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({features})
    })
    .then(res => res.json())
    .then(data => {
      resultBox.style.display = 'block';
      if (data.prediction === 1) {
        resultBox.className = 'status-box high-risk';
        resultBox.innerHTML = `<strong>High Seizure Risk</strong><br>
          Confidence: ${data.confidence}<br>
          <span>${data.message}</span>`;
      } else if (data.prediction === 0) {
        resultBox.className = 'status-box low-risk';
        resultBox.innerHTML = `<strong>Low Seizure Risk</strong><br>
          Confidence: ${data.confidence}<br>
          <span>${data.message}</span>`;
      } else {
        resultBox.className = 'status-box';
        resultBox.textContent = data.message || 'Unknown response from server.';
      }
    })
    .catch(err => {
      resultBox.style.display = 'block';
      resultBox.className = 'status-box error';
      resultBox.textContent = 'Error contacting backend: ' + err;
    });
  });
});