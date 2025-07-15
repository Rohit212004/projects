from flask import Flask, request, jsonify, send_file
import requests
from dataclasses import dataclass
from typing import Optional

app = Flask(__name__)

AUTH_SERVICE_URL = 'http://localhost:1507/api/auth/verify'

@dataclass
class Address:
    street: str
    city: str
    state: str
    postal_code: str

@dataclass
class DeliveryRequest:
    customer_name: str
    customer_address: Address
    delivery_name: str
    delivery_address: Address
    parcel_size: str
    parcel_weight_grams: float

def parse_address(address_str: str) -> Address:
    parts = [part.strip() for part in address_str.split(',')]
    if len(parts) != 4:
        raise ValueError("Address must be in format: Street, City, State, PostalCode")
    return Address(street=parts[0], city=parts[1], state=parts[2], postal_code=parts[3])

def calculate_delivery_cost(weight_grams: float) -> float:
    return weight_grams * 10.0

def estimate_delivery_time(customer_state: str, delivery_state: str) -> int:
    return 3 if customer_state.lower() == delivery_state.lower() else 10

def verify_user(user_id: str, token: str) -> tuple[bool, str]:
    try:
        response = requests.post(
            AUTH_SERVICE_URL,
            json={'user_id': user_id},
            headers={'Authorization': token}
        )
        if response.status_code == 200:
            return True, "User authorized"
        else:
            return False, f"Auth service returned {response.status_code}: {response.json().get('error', 'Unknown error')}"
    except requests.RequestException as e:
        return False, f"Auth service error: {str(e)}"

@app.route('/api/delivery', methods=['POST'])
def create_delivery():
    try:
        user_id = request.headers.get('X-User-ID')
        auth_token = request.headers.get('Authorization')
        if not user_id or not auth_token:
            return jsonify({'error': 'Missing X-User-ID or Authorization header'}), 401

        is_authorized, auth_message = verify_user(user_id, auth_token)
        if not is_authorized:
            return jsonify({'error': f'Unauthorized: {auth_message}'}), 401

        data = request.get_json()
        required_fields = ['customer_name', 'customer_address', 'delivery_name',
                          'delivery_address', 'parcel_size', 'parcel_weight_grams']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400

        try:
            customer_address = parse_address(data['customer_address'])
            delivery_address = parse_address(data['delivery_address'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        delivery = DeliveryRequest(
            customer_name=data['customer_name'],
            customer_address=customer_address,
            delivery_name=data['delivery_name'],
            delivery_address=delivery_address,
            parcel_size=data['parcel_size'],
            parcel_weight_grams=float(data['parcel_weight_grams'])
        )

        cost = calculate_delivery_cost(delivery.parcel_weight_grams)
        delivery_days = estimate_delivery_time(
            delivery.customer_address.state,
            delivery.delivery_address.state
        )

        return jsonify({
            'status': 'success',
            'delivery': {
                'customer_name': delivery.customer_name,
                'customer_address': f"{delivery.customer_address.street}, {delivery.customer_address.city}, "
                                  f"{delivery.customer_address.state}, {delivery.customer_address.postal_code}",
                'delivery_name': delivery.delivery_name,
                'delivery_address': f"{delivery.delivery_address.street}, {delivery.delivery_address.city}, "
                                  f"{delivery.delivery_address.state}, {delivery.delivery_address.postal_code}",
                'parcel_size': delivery.parcel_size,
                'parcel_weight_grams': delivery.parcel_weight_grams,
                'cost_rupees': round(cost, 2),
                'estimated_delivery_days': delivery_days
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def serve_form():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=1407, debug=True)