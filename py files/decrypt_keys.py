import os
import sys
from cryptography.fernet import Fernet
import os.path

def decrypt_contents(key):
    fernet = Fernet(key)
    with open("password_tokens.txt", 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)
    with open("password_tokens.txt", 'wb') as dec_file:
        dec_file.write(decrypted)


def save_key(key):
    with open("filekey.key", 'wb') as filekey:
        filekey.write(key)


def validate_key(generated_key):
    with open("filekey.key", 'rb') as filekey:
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
    decrypt_contents(key)
if '__main__' == __name__:
    main()