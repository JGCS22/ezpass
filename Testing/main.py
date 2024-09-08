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




def get_data():
    with open("data_storage.json", "r") as ds_file:
        list_of_dict = json.load(ds_file)
    return list_of_dict



def main():
    print("\n\tE\tZ\tP\tA\tS\tS\n")
    while True:
        if os.path.exists("data_storage.json") == True:
            username_attempt = input("USERNAME: ")
            master_password_attempt = getpass_asterisk("PASSWORD: ")
            
            list_of_dict = get_data()
            username_onfile = list_of_dict[0]["USERNAME"]
            salt_onfile = base64.b64decode(list_of_dict[1]["SALT"])
            unique_key = generate_key(salt_onfile, master_password_attempt)
            decrypted_password_dict = decrypt(unique_key, list_of_dict[2])

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
                    append_data(unique_key, list_of_dict)
                    print_data(list_of_dict)
                    sys.exit()
        else:
            print("CREATING A NEW PROFILE")
            generate_profile()
            sys.exit()




main()