import sys
import password_generator
import decrypt_login_index
import encrypt_login_index
import os.path

def create_user(login_index):
    authorize_access = input("Enter Authorization Code: /")
    if authorize_access == "edoc":
        pass
    else:
        sys.exit()
    print("")
    new_username = input("New Username: ")
    new_user_password = input("New Password: ")
    print("")
    print("-" * 41)
    new_user = new_username + " " + new_user_password + " \n"
    
    counter = 0
    for i in range(len(login_index)):
        if login_index[i] == new_user:
            print("User exists; try again.")
            return None
        elif login_index[i] != new_user:
            counter += 1
    if counter == len(login_index):
        return new_user
 
def save_login_index(login_index):
    overwrite_login_file = open("login_index.txt", "w")
    overwrite_login_file.writelines(login_index)
    overwrite_login_file.close()

def intialize_login_index():
    read_login_file = open("login_index.txt", "r")
    login_index = read_login_file.readlines()
    read_login_file.close()
    if login_index == []:
        return login_index
    elif len(login_index[0]) > 30:
        decrypt_login_index.main()
        read_login_file = open("login_index.txt", "r")
        login_index = read_login_file.readlines()
        read_login_file.close()
    
    
    login_index.sort()
    return login_index

def check_credentials(login_request, login_index):
    for i in range(len(login_index)):
        if login_index[i] == login_request:
            return True

def main():
    if os.path.exists("login_index.txt") == False:
        create_file = open("login_index.txt", "x")
        create_file.close()
    if os.path.exists("password_tokens.txt") == False:
        create_file = open("password_tokens.txt", "x")
        create_file.close()
    if os.path.exists("filekey_u.key") == False:
        create_file = open("filekey_u.key", "x")
        create_file.close()
    if os.path.exists("filekey.key") == False:
        create_file = open("filekey.key", "x")
        create_file.close()
    print("")
    print("WARNING: USE AT YOUR OWN RISK!")
    print("")
    print("")
    print("     Password Generator by Joseph Gallant")
    print("")
    print("System Login ~")
    print("")
    print("-" * 41)
    print("")
    get_username = input("Username: ")
    get_user_password = input("Password: ")
    print("")
    print("-" * 41)

    login_request = get_username + " " + get_user_password + " \n"

    login_index = intialize_login_index()
    login_state = check_credentials(login_request, login_index)
    
    if login_state == True:
        password_generator.main()
    elif login_state == None:
        print("")
        print("User or Password is invalid;")
        print("/C to create new User, /R to go back: ")
        print("")
        create_or_reset = input("/")
        if create_or_reset == "C":
            print("")
            print("-" * 41)
            print("")
            new_user = create_user(login_index)
            while new_user == None:
                new_user = create_user(login_index)
            login_index.append(new_user)
            save_login_index(login_index)
            encrypt_login_index.main()
            main()
        elif create_or_reset == "R":
            
            main()
main()