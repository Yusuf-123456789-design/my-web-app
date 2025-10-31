# api.py
from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)

# 🧑‍💻 Username & Password
USERNAME = "buddy"
PASSWORD = "12345"


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
            return make_response(
                "🚫 Unauthorized! Please enter valid credentials.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

# ✅ Simple GET API
@app.route('/')
@require_auth
def home():
    return "✅ Welcome to Buddy's Simple API!"

# 💼 Example GET endpoint with JSON data
@app.route('/wallet', methods=['GET'])
@require_auth
def get_wallet():
    wallet_data = {
        "id": 1,
        "brand": "Generic",
        "type": "Full Grain Leather Wallet",
        "color": "Black",
        "price": 2499,
        "currency": "INR"
    }
    return jsonify(wallet_data)

# ➕ Example POST endpoint
@app.route('/addWallet', methods=['POST'])
@require_auth
def add_wallet():
    wallet = request.get_json()
    print("📦 New Wallet Added:", wallet)
    return jsonify({
        "message": "Wallet added successfully!",
        "data": wallet
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=3000)

