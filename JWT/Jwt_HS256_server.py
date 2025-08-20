# The goal of this code is to show what is hapenning server side to better understand the authentication mechanism
from flask import Flask, request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

app = Flask(__name__)

# Shared secret key
SECRET_KEY = "your-256-bit-secret"
ALGORITHM = "HS256"
EXPECTED_ISSUER = "https://auth.example.com"
EXPECTED_AUDIENCE = "my-api"

@app.route("/protected", methods=["GET"])
def protected():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=EXPECTED_ISSUER,
            audience=EXPECTED_AUDIENCE,
            leeway=10  # seconds
        )
        return jsonify({"message": "Access granted", "user": payload}), 200

    except ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)
