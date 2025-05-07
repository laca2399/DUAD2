from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt
import datetime

class JWT_Manager:
    def __init__(self, private_path="private.pem", public_path="public.pem", passphrase="!abc123abc!"):
        with open(private_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=passphrase.encode(),
                backend=default_backend()
            )
        with open(public_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
        print(f"Public key loaded: {self.public_key}")

    def encode(self, user_id, role="user"):
        payload = {
            "sub": str(user_id),
            "role": role,  
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, self.private_key, algorithm="RS256")
        print(f"Encoded token: {token}") 
        return token

    def decode(self, token):
        try:
            print(f"Attempting to decode token: {token}")  
            decoded_token = jwt.decode(token, self.public_key, algorithms=["RS256"])
            print(f"Decoded token: {decoded_token}")  
            return decoded_token
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None





