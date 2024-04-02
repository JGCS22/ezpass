import random
import os
import string
import encrypt_keys
import decrypt_keys
import encrypt_login_index
import os.path

def generate_password(uppercase_letters, lowercase_letters, numbers, special_characters):
    intialize_password = []
    for i in range(4):
        random.seed()
        intialize_password.append(random.choice(uppercase_letters))
        intialize_password.append(random.choice(lowercase_letters))
        intialize_password.append(random.choice(numbers))
    for i in range(2):
        random.seed()
        intialize_password.append(random.choice(special_characters))
    generated_password = random.sample(intialize_password, 14)
    
    while set(generated_password[0]).intersection(numbers + special_characters):
        random.seed()
        generated_password = random.sample(intialize_password, 14)

    list_to_string = ""
    for i in generated_password:
        list_to_string += str(i)
    generated_password = list_to_string

    return generated_password

def save_password_index(password_index):
    overwrite_passwords_file = open("password_tokens.txt", "w")
    overwrite_passwords_file.writelines(password_index)
    overwrite_passwords_file.close()


def read_password_index(generated_password, password_purpose):
    read_password_file = open("password_tokens.txt", "r")
    password_index = read_password_file.readlines()
    read_password_file.close()

    if password_index != []:
        if len(password_index[0]) > 30:
            decrypt_keys.main()
            read_password_file = open("password_tokens.txt", "r")
            password_index = read_password_file.readlines()
            read_password_file.close()

    new_password = " " + generated_password + " | " + password_purpose + " \n"

    return password_index, new_password

def main():
    print("")
    password_state = input("'/R'ead or '/G'enerate: /")
    print("")
    if password_state == 'R':
        decrypt_keys.main()
        os.system('password_tokens.txt')
        encrypt_keys.main()
        encrypt_login_index.main()
        exit()
    elif password_state == 'G':
        pass
    password_purpose = input("Description: ")
    print("")
    uppercase_letters = list(string.ascii_uppercase)
    lowercase_letters = list(string.ascii_lowercase)
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    special_characters = ["!", "@", "?", "$", "#", "_", ".", "-", "/", ":", ";"]

    generated_password = generate_password(uppercase_letters, lowercase_letters, numbers, special_characters)
    password_index, new_password = read_password_index(generated_password, password_purpose)

    if password_index == []:
        header = "    PASSWORDS   | FOR \n"
        password_index.append(header)


    password_index.append(new_password)

    save_password_index(password_index)

    os.system('password_tokens.txt')
    encrypt_keys.main()
    encrypt_login_index.main()

if '__main__' == __name__:
    main()

