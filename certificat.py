import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature


# Générer une paire de clés RSA (pour la CA) - à faire UNE FOIS
def generate_ca_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


# Générer un certificat rudimentaire signé par la CA
def generate_certificate(username, user_public_key_pem, ca_private_key):
    # Préparer la donnée à signer : username + clé publique PEM
    data_to_sign = (username + user_public_key_pem).encode('utf-8')

    # Calculer le hash
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data_to_sign)
    hashed = digest.finalize()

    # Signer le hash avec la clé privée CA
    ca_signature = ca_private_key.sign(
        hashed,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Créer le certificat sous forme JSON
    certificate = {
        "username": username,
        "public_key": user_public_key_pem,
        "CA_signature": base64.b64encode(ca_signature).decode('utf-8')
    }
    return certificate


# Vérifier un certificat
def verify_certificate(certificate, ca_public_key):
    username = certificate["username"]
    user_public_key_pem = certificate["public_key"]
    ca_signature_b64 = certificate["CA_signature"]
    ca_signature = base64.b64decode(ca_signature_b64)

    # Refaire le hash sur username + clé publique
    data_to_verify = (username + user_public_key_pem).encode('utf-8')
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data_to_verify)
    hashed = digest.finalize()

    # Vérifier la signature CA
    try:
        ca_public_key.verify(
            ca_signature,
            hashed,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Certificat VALIDE")
        return True
    except InvalidSignature:
        print("❌ Certificat INVALIDE")
        return False


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    # 1. CA génère ses clés (à faire UNE FOIS)
    # ca_private_key, ca_public_key = generate_ca_keys()

    # # 2. Supposons qu'on a déjà une clé publique utilisateur (exemple)
    # user_public_key = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key()
    # user_public_key_pem = user_public_key.public_bytes(
    #     serialization.Encoding.PEM,
    #     serialization.PublicFormat.SubjectPublicKeyInfo
    # ).decode('utf-8')

    # # 3. Générer le certificat signé par la CA
    # cert = generate_certificate("user1", user_public_key_pem, ca_private_key)

    # # 4. Sauvegarder le certificat en JSON (optionnel)
    # with open("certificate_user1.json", "w") as f:
    #     json.dump(cert, f, indent=2)

    # # 5. Vérifier le certificat
    # verify_certificate(cert, ca_public_key)

        # Charge la clé publique CA à partir d’un fichier PEM (générée une fois et sauvegardée)
    with open("user1_public.pem", "rb") as f:
        ca_public_key = serialization.load_pem_public_key(f.read())

    with open("certificate_user1.json", "r") as f:
        cert = json.load(f)

    verify_certificate(cert, ca_public_key)