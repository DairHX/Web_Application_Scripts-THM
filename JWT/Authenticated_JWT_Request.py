import jwt
import datetime
import requests

SECRET_KEY = "MyscretPassword123" #EasyOne an ASCII string
ALGORITHM = "HS256"

# Current time
now = datetime.datetime.utcnow()

# JWT payload (claims)
payload = {
    "sub": "user123",                                # User ID (subject)
    "name": "Dair",                                # Optional claim
    "iss": "https://auth.example.com",               # Issuer For better Precision
    "aud": "my-api",                                 # Audience (who this token is for)
    "iat": now,                                      # Issued at
    "exp": now + datetime.timedelta(hours=1)         # Expiration in 1 hour
}

# Optional JWT header
custom_headers = {
    "alg": "HS256",
    "typ": "JWT"
}

# Encode JWT (returns string in PyJWT v2+)
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM, headers=custom_headers)

print("🔐 JWT Token:")
print(token)
print()

# Set headers for HTTP request
http_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send request to Flask server
response = requests.get("http://localhost:5000/protected", headers=http_headers)

# Print response
print(" Server Response:")
print("Status Code:", response.status_code)
print("JSON:", response.json())
