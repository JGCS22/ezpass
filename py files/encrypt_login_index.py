from cryptography.fernet import Fernet
import os.path

def encrypt_contents(key):
    fernet = Fernet(key)
    with open("login_index.txt", 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open("login_index.txt", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def save_key(key):
    with open("filekey_u.key", 'wb') as filekey:
        filekey.write(key)


def validate_key(generated_key):
    with open("filekey_u.key", 'rb') as filekey:
        current_key = filekey.read()
        if current_key == b"":
            return generated_key
        else:
            return current_key

def main():
    generated_key = Fernet.generate_key()
    key = validate_key(generated_key)
    if key == generated_key:
        save_key(key)
    else:
        pass
    encrypt_contents(key)
if '__main__' == __name__:
    main()
