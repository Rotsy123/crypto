import json 
# python
with open("user1_public.pem") as f:
    fake_key = f.read()

with open("certificate_user1.json", "r") as f:
    register = json.load(f)

register["public_key"] = fake_key

with open("certificate_user1.json", "w") as f:
    json.dump(register, f, indent=4)

print("⚠️ Clé publique de user1 remplacée par celle de Mallory.")
