from cryptography.fernet import Fernet

# Generowanie klucza
key = Fernet.generate_key()

# Zapis klucza do pliku
with open("secret.key", "wb") as key_file:
    key_file.write(key)
