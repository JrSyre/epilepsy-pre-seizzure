"""
Stripe payments endpoints for appointment booking.
Provides endpoints to fetch publishable key and create PaymentIntents.
"""

import os
from flask import Blueprint, jsonify, request
import stripe

payments_bp = Blueprint('payments', __name__)

# Read Stripe keys from environment
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_CURRENCY = os.environ.get('STRIPE_CURRENCY', 'usd')
APPOINTMENT_PRICE_CENTS = int(os.environ.get('APPOINTMENT_PRICE_CENTS', '2000'))  # default $20.00

# Initialize Stripe client if key present
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

@payments_bp.route('/payments/config', methods=['GET'])
def payments_config():
    """Expose publishable key and pricing configuration to the frontend."""
    return jsonify({
        'publishableKey': STRIPE_PUBLISHABLE_KEY,
        'currency': STRIPE_CURRENCY,
        'amount_cents': APPOINTMENT_PRICE_CENTS
    })

@payments_bp.route('/payments/create-intent', methods=['POST'])
def create_payment_intent():
    """
    Create a Stripe PaymentIntent for an appointment booking.

    Request JSON (optional overrides):
    {
        "amount_cents": 2500,           # optional; defaults to APPOINTMENT_PRICE_CENTS
        "currency": "usd",             # optional; defaults to STRIPE_CURRENCY
        "metadata": { ... }             # optional metadata (patient, doctor, date, time)
    }
    """
    if not STRIPE_SECRET_KEY:
        return jsonify({
            'error': 'stripe_not_configured',
            'message': 'Stripe secret key is not configured on the server.'
        }), 500

    try:
        data = request.get_json(silent=True) or {}
        amount_cents = int(data.get('amount_cents', APPOINTMENT_PRICE_CENTS))
        currency = (data.get('currency') or STRIPE_CURRENCY).lower()
        metadata = data.get('metadata') or {}

        # Basic guardrails
        if amount_cents <= 0:
            return jsonify({'error': 'invalid_amount', 'message': 'Amount must be greater than zero.'}), 400

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            automatic_payment_methods={'enabled': True},
            metadata=metadata
        )

        return jsonify({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id,
            'amount_cents': amount_cents,
            'currency': currency
        })

    except stripe.error.StripeError as e:
        return jsonify({'error': 'stripe_error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'server_error', 'message': str(e)}), 500
