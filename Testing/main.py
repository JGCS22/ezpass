import json
import sys
import string
import secrets
from tabulate import tabulate
from getpass_asterisk.getpass_asterisk import getpass_asterisk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pandas as pd
import os
import base64

# import bcrypt

def decrypt(decryption_key, pd_encrypted):

    return pd_encrypted

def generate_sp():
    character_domain = string.ascii_letters + string.digits + string.punctuation
    generated_sp = ''.join(secrets.choice(character_domain) for _ in range(16))

    return generated_sp
                           

def rederive(salt, master_password):
    kdf = PBKDF2HMAC (
        algorithm=hashes.SHA256(),
        length=32,  # Length of the derived key in bytes (32 bytes = 256 bits)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    return kdf.derive(master_password)

def print_passwords(sp_dict):
    df = pd.DataFrame(list(sp_dict[2].items()), columns=["Comment", "Password"])
    formatted_df = tabulate(df, headers="keys", tablefmt="grid", stralign="center", numalign="center")
    print(formatted_df)

def append_data(entry):
    with open("data_storage.json", "w") as ds_file:
        json.dump(entry, ds_file, indent=4)
    print_passwords(entry)

def new_user():
    salt_encoded = base64.b64encode(os.urandom(16)).decode("utf-8")
    username = input("NEW USERNAME: ")
    master_password = getpass_asterisk("NEW PASSWORD: ").encode()
    sp_comment = input("Comment: ")
    new_sp = generate_sp()
    print(new_sp)

    data_template = [
        {"username": f"{username}"},
        {"salt": salt_encoded},
        {sp_comment: new_sp}
    ]
    
    with open("data_storage.json", "w") as ds_file:
        json.dump(data_template, ds_file, indent=4)
    
    return


def main():
    print("\n\tezpass")
    while True:
        if os.path.exists("data_storage.json") == True:
            username = input("USERNAME: ")
            master_password = getpass_asterisk("PASSWORD: ").encode()

            with open("data_storage.json", "r") as ds_file:
                ds_list = json.load(ds_file)
            
            username_of = ds_list[0]["username"]
            salt_decoded = base64.b64decode(ds_list[1]["salt"])
            encryption_key = rederive(salt_decoded, master_password)
            pd_encrypted = ds_list[2]
            pd_decrypted = decrypt(encryption_key, pd_encrypted)

            if username != ds_list[0]["username"] or pd_decrypted == False:
                print("Invalid Username or Password, Please try Again.")
            else:  
                print(f"\nHello, {username_of}!")
                if input("Read or Write(r/w): ") == 'r':
                    print_passwords(ds_list)
                    sys.exit()
                        

                else:
                    sp_comment = input("Comment: ")
                    new_sp = generate_sp()
                    ds_list[2][sp_comment] = new_sp
                    append_data(ds_list)
                    sys.exit()
                    #append to dict, rewrite dict and write to file

        else:
            print("\nCreating a new User...\n")
            new_user()
            
            


main()
