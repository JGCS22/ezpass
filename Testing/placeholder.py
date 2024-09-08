import json
import sys
import string
import secrets
from tabulate import tabulate
from getpass_asterisk.getpass_asterisk import getpass_asterisk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
import pandas as pd
import os
import base64

def decrypt(unique_key, encrypted_password_string):
    f = Fernet(unique_key)
    decrypted_password_string = f.decrypt(encrypted_password_string)
    decrypted_password_dict = json.loads(decrypted_password_string)
    return decrypted_password_dict

def encrypt(unique_key, decrypted_password_dict):
    f = Fernet(unique_key)
    decrypted_password_string = json.dumps(decrypted_password_dict)
    encrypted_password_dict = f.encrypt(decrypted_password_string.encode())
    return encrypted_password_dict

def generate_profile():
    salt = os.urandom(16)
    salt_encoded = base64.b64encode(salt).decode("utf-8")
    new_username = input("NEW USERNAME: ")
    new_master_password = getpass_asterisk("NEW PASSWORD: ").encode()
    comment = input("COMMENT: ")
    password = generate_password()

    data_storage_template = [
        {"USERNAME": f"{new_username}"},
        {"SALT": salt_encoded},
        {comment: password}
    ]
    unique_key = generate_key(salt, new_master_password)
    print_data(data_storage_template)
    append_data(unique_key, data_storage_template)
    return

def generate_password():
    character_domain = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(character_domain) for _ in range(16))
    return password

def generate_key(salt_onfile, master_password_attempt):
    kdf = PBKDF2HMAC (
        algorithm=hashes.SHA256(),
        length=32,  # Length of the derived key in bytes (32 bytes = 256 bits)
        salt=salt_onfile,
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(master_password_attempt))


def append_data(unique_key, list_of_dict):
    password_dict = list_of_dict[2]
    encrypted_password_dict = encrypt(unique_key, password_dict)
    print(encrypted_password_dict)
    list_of_dict[2] = encrypted_password_dict.decode()
    with open("data_storage.json", "w") as ds_file:
        json.dump(list_of_dict, ds_file, indent=4)
    return

def get_data():
    with open("data_storage.json", "r") as ds_file:
        list_of_dict = json.load(ds_file)
    return list_of_dict


def print_data(list_of_dict):
    df = pd.DataFrame(list(list_of_dict[2].items()), columns=["Comment", "Password"])
    formatted_df = tabulate(df, headers="keys", tablefmt="grid", stralign="center", numalign="center", showindex=False)
    print(formatted_df)

def main():
    print("\n\tE\tZ\tP\tA\tS\tS\n")
    while True:
        if os.path.exists("data_storage.json") == True:
            username_attempt = input("USERNAME: ")
            master_password_attempt = getpass_asterisk("PASSWORD: ").encode()
            
            list_of_dict = get_data()
            username_onfile = list_of_dict[0]["USERNAME"]
            salt_onfile = base64.b64decode(list_of_dict[1]["SALT"])
            unique_key = generate_key(salt_onfile, master_password_attempt)
            decrypted_password_dict = decrypt(unique_key, list_of_dict[2])
            list_of_dict[2] = decrypted_password_dict


            if username_attempt != username_onfile or decrypted_password_dict == False:
                print("INVALID USERNAME OR PASSWORD")
            else:
                print(f"Welcome back, {username_onfile}!")
                if input("Read or Write(r/w): ") == 'r':
                    print_data(list_of_dict)
                    sys.exit()
                else:
                    comment_to_append = input("COMMENT: ")
                    password_to_append = generate_password()
                    list_of_dict[2][comment_to_append] = password_to_append
                    print_data(list_of_dict)
                    append_data(unique_key, list_of_dict)
                    sys.exit()
        else:
            print("CREATING A NEW PROFILE")
            generate_profile()
            sys.exit()

main()