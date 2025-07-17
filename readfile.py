import base64
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

# Étape 1 : Charger la clé privée de l'utilisateur
def load_private_key(path):
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

# Étape 2 : Lire le fichier à signer
with open("indication.txt", "rb") as f:
    document_data = f.read()

# Étape 3 : Calculer le hash SHA-256 du fichier
digest = hashes.Hash(hashes.SHA256())
digest.update(document_data)
hash_value = digest.finalize()

# Étape 4 : Signer le hash avec la clé privée RSA
private_key = load_private_key("user1_private.pem")  # chemin vers la clé privée

signature = private_key.sign(
    hash_value,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Étape 5 : Sauvegarder la signature brute
with open("document.sig", "wb") as f:
    f.write(signature)

# Étape 6 : Sauvegarder les métadonnées au format JSON
metadata = {
    "user": "user1",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "signature": base64.b64encode(signature).decode("utf-8")
}

with open("document_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)
