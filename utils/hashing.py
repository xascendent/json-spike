import hashlib

def generate_hash(value: str) -> bytes:
    return hashlib.sha256(value.encode('utf-8')).digest()
