from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded list of users
USERS = {
    "rohit2110": {"user_id": "rohit2110", "name": "Rohit Vishwakarma", "role": "customer"},
    "rahul": {"user_id": "rahul", "name": "Rahul", "role": "customer"},
    "admin123": {"user_id": "admin123", "name": "Admin User", "role": "admin"}
}

@app.route('/api/auth/verify', methods=['POST'])
def verify_user():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        token = request.headers.get('Authorization')

        # Basic token validation (mock: assume token is just "Bearer <user_id>")
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Invalid or missing Authorization header'}), 401

        token_user_id = token.split(' ')[1]
        if token_user_id != user_id:
            return jsonify({'error': 'Token does not match user_id'}), 401

        # Check if user_id exists in USERS
        if user_id not in USERS:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'status': 'success',
            'user': USERS[user_id]
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=1507, debug=True)