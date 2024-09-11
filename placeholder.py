from imports import *

def decrypt(unique_key, encrypted_password_string):
    try:
        f = Fernet(unique_key)
        decrypted_password_string = f.decrypt(encrypted_password_string)
        decrypted_password_dict = json.loads(decrypted_password_string)
        return decrypted_password_dict
    except (InvalidSignature, InvalidToken):
        return False


def encrypt(unique_key, decrypted_password_dict):
    f = Fernet(unique_key)
    decrypted_password_string = json.dumps(decrypted_password_dict)
    encrypted_password_dict = f.encrypt(decrypted_password_string.encode())
    return encrypted_password_dict

def clear_clipboard():
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    ctypes.windll.user32.CloseClipboard()


def generate_profile():
    salt = os.urandom(16)
    salt_encoded = base64.b64encode(salt).decode("utf-8")
    new_username = input("NEW USERNAME: ")
    new_master_password = getpass_asterisk("NEW PASSWORD: ").encode()
    comment = input("Comment: ")
    password = generate_password()
    pyperclip.copy(password)

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
        backend=default_backend(),
    )

    return urlsafe_b64encode(kdf.derive(master_password_attempt))


def append_data(unique_key, list_of_dict):
    password_dict = list_of_dict[2]
    encrypted_password_dict = encrypt(unique_key, password_dict)
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
    input("press enter to exit...")
    clear_clipboard()


def main():
    print("\n\tE\tZ\tP\tA\tS\tS")
    while True:
        if os.path.exists("data_storage.json") == True:
            username_attempt = input("\nUSERNAME: ")
            master_password_attempt = getpass_asterisk("PASSWORD: ").encode()
            
            list_of_dict = get_data()
            username_onfile = list_of_dict[0]["USERNAME"]
            salt_onfile = base64.b64decode(list_of_dict[1]["SALT"])
            unique_key = generate_key(salt_onfile, master_password_attempt)
            decrypted_password_dict = decrypt(unique_key, list_of_dict[2])
            list_of_dict[2] = decrypted_password_dict


            if username_attempt != username_onfile or decrypted_password_dict == False:
                print("Invalid Username or Password, Please Try Again.")
            else:
                print(f"\nWelcome back, {username_onfile}!")
                if input("Would you like to Read or Write? (r/w): ") == 'r':
                    last_dict = list_of_dict[-1]
                    last_key = list(last_dict.keys())[-1]
                    recent_password = last_dict[last_key]
                    pyperclip.copy(recent_password)
                    print_data(list_of_dict)
                    sys.exit()
                else:
                    comment_to_append = input("Comment: ")
                    password_to_append = generate_password()
                    pyperclip.copy(password_to_append)
                    list_of_dict[2][comment_to_append] = password_to_append
                    print_data(list_of_dict)
                    append_data(unique_key, list_of_dict)
                    sys.exit()
        else:
            print("\nCREATING A NEW PROFILE...\n")
            generate_profile()
            sys.exit()

if __name__ == "__main__":
    main()
