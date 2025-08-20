# In Your CMDline: (Generate Keys)

# $ openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048
# $ openssl rsa -pubout -in private.pem -out public.pem

import jwt
import datetime
import requests

# Load private key
with open("private.pem", "r") as f:
    PRIVATE_KEY = f.read()

ALGORITHM = "RS256"

# Current UTC time
now = datetime.datetime.utcnow()

# JWT payload (claims)
payload = {
    "sub": "user123",                                # Subject (user ID)
    "name": "Sophia",                                # Custom claim
    "iss": "https://auth.example.com",               # Issuer
    "aud": "my-api",                                 # Audience
    "iat": now,                                      # Issued at
    "exp": now + datetime.timedelta(hours=1)         # Expiry (1 hour)
}

# Create signed token with RS256 (private key)
token = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

print("RS256 JWT Token:")
print(token)
print()

# HTTP headers with token
http_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send to server
response = requests.get("http://localhost:5000/protected", headers=http_headers)

# Show server response
print("Server Response:")
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
