document.addEventListener('DOMContentLoaded', async function () {
  const statusBox = document.getElementById('appointment-status');
  const cardErrors = document.getElementById('card-errors');
  const payButton = document.getElementById('pay-book');
  const cardElementContainer = document.getElementById('card-element');

  if (!window.Stripe || !payButton || !cardElementContainer) {
    return;
  }

  function showError(message) {
    if (cardErrors) {
      cardErrors.style.display = 'block';
      cardErrors.className = 'status-box error';
      cardErrors.textContent = message;
    }
  }

  function showStatus(message, ok = true) {
    if (statusBox) {
      statusBox.style.display = 'block';
      statusBox.className = 'status-box ' + (ok ? 'success' : 'error');
      statusBox.textContent = message;
    }
  }

  try {
    // 1) Fetch publishable key and pricing
    const cfgResp = await fetch('/api/payments/config');
    const cfg = await cfgResp.json();
    if (!cfg.publishableKey) {
      showError('Payment configuration is missing.');
      return;
    }

    const stripe = Stripe(cfg.publishableKey);
    const elements = stripe.elements({
      appearance: {
        theme: 'night',
        variables: {
          colorPrimary: '#A259FF',
          colorBackground: 'transparent',
          colorText: '#ffffff',
        }
      }
    });

    const cardElement = elements.create('card', {
      style: {
        base: {
          color: '#fff',
          fontFamily: 'Poppins, Inter, Arial, sans-serif',
          fontSmoothing: 'antialiased',
          '::placeholder': { color: '#cfcfcf' }
        },
        invalid: { color: '#ff6b6b' }
      }
    });
    cardElement.mount('#card-element');

    payButton.addEventListener('click', async function () {
      cardErrors.style.display = 'none';
      statusBox.style.display = 'none';

      // Validate appointment fields
      const patient = document.getElementById('patient').value.trim();
      const doctor = document.getElementById('doctor').value.trim();
      const date = document.getElementById('date').value;
      const time = document.getElementById('time').value;

      if (!patient || !doctor || !date || !time) {
        showError('Please complete all appointment details first.');
        return;
      }

      try {
        // 2) Create PaymentIntent on server
        const meta = { patient, doctor, date, time };
        const piResp = await fetch('/api/payments/create-intent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ metadata: meta })
        });
        const pi = await piResp.json();
        if (!pi.client_secret) {
          showError(pi.message || 'Could not create payment.');
          return;
        }

        // 3) Confirm payment on client
        const { error, paymentIntent } = await stripe.confirmCardPayment(pi.client_secret, {
          payment_method: {
            card: cardElement,
          }
        });

        if (error) {
          showError(error.message || 'Payment failed.');
          return;
        }

        if (paymentIntent && paymentIntent.status === 'succeeded') {
          // 4) Book the appointment upon successful payment
          const bookResp = await fetch('/api/appointments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patient, doctor, date, time })
          });
          const book = await bookResp.json();
          if (bookResp.ok) {
            showStatus('Payment successful and appointment booked!');
          } else {
            showError(book.message || 'Payment succeeded but booking failed.');
          }
        } else {
          showError('Payment was not successful.');
        }
      } catch (e) {
        showError(e.message || 'An error occurred while processing payment.');
      }
    });
  } catch (e) {
    showError('Could not initialize payment.');
  }
});
