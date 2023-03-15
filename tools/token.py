from cryptography.fernet import Fernet


def save_token(filename, token, password):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    encrypted_token = f.encrypt(token.encode())
    with open(filename, "wb") as file:
        file.write(key + b"\n")
        file.write(encrypted_password + b"\n")
        file.write(encrypted_token)


def load_token(filename, password) -> str:
    with open(filename, "rb") as file:
        key = file.readline().strip()
        f = Fernet(key)
        encrypted_password = file.readline().strip()
        if f.decrypt(encrypted_password).decode() != password:
            raise ValueError("Password does not match.")
        encrypted_token = file.readline().strip()
    token = f.decrypt(encrypted_token).decode()
    return token
