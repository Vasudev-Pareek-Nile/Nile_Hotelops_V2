from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY)

def encrypt_id(id):
    """Encrypt the ID."""
    return fernet.encrypt(str(id).encode()).decode()

def decrypt_id(encrypted_id):
    """Decrypt the ID."""
    try:
        return int(fernet.decrypt(encrypted_id.encode()).decode())
    except Exception:
        return None  # Handle failed decryption
