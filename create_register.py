import json

def add_user_to_register(username, public_key_pem, path="register.json"):
    try:
        with open(path, "r") as f:
            register = json.load(f)
    except FileNotFoundError:
        register = {}

    register[username] = public_key_pem

    with open(path, "w") as f:
        json.dump(register, f, indent=4)
    print(f"✅ Utilisateur {username} ajouté au registre avec succès.")

# Exemple d'utilisation
if __name__ == "__main__":
    username = "user1"
    # Charge la clé publique depuis un fichier PEM
    with open("user1_public.pem", "r") as f:
        public_key_pem = f.read()

    add_user_to_register(username, public_key_pem)