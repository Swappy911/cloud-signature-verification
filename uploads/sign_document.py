from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Load private key
with open("private_key.pem", "rb") as f:
    private_key = load_pem_private_key(f.read(), password=None)

# Document to sign
data = b"This is a test document"

# Create signature
signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

with open("signature.sig", "wb") as f:
    f.write(signature)

print("Signature created!")