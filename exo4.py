import base64
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def load_public_key_from_register(username, register_path="register.json"):
    with open(register_path, "r") as f:
        register = json.load(f)
    pem = register.get(username)
    if not pem:
        raise ValueError(f"Aucune clé publique pour l'utilisateur {username}")
    return serialization.load_pem_public_key(pem.encode('utf-8'))

def verify_signature(username, file_path, metadata_path):
    # Étape 1 : Lire le fichier texte
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Étape 2 : Calculer le hash SHA-256
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file_data)
    hash_value = digest.finalize()

    # Étape 3 : Charger la signature et métadonnées
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    signature_b64 = metadata["signature"]
    signature = base64.b64decode(signature_b64)

    # Étape 4 : Charger la clé publique de l'utilisateur depuis le registre
    public_key = load_public_key_from_register(username)

    # Étape 5 : Vérification
    try:
        public_key.verify(
            signature,
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Signature VALIDE")
    except InvalidSignature:
        print("❌ Signature INVALIDE")


if __name__ == "__main__":
    verify_signature("user1", "indication.txt", "document_metadata.json")
