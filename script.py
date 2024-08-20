import ast
import hashlib
import json
import os
import sys
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


#This is the main DB file with all the users registered in the script.
USER_DB = "USER_DB.txt"



def check_file_empty(filepath):
    """Check if the file is empty. In the latter case, return True."""
    file = os.stat(filepath).st_size == 0
    return file

def check_file_exist(filepath):
    """Check if the used files exist. In the latter case, return True."""
    file = os.path.isfile(filepath)
    if not file:
        print(f"***WARNING***: The database file named <{filepath}> does not exist! It will be created right now...")
        with (open(filepath, "w")):
            print(f"File {filepath} has been created!")
    else:
        print(f"File {filepath} loaded. ")


def check_credentials(username,password):
    """This function is used to log in. It loads the file where credentials are saved and matches them with user input"""
    with open(USER_DB, "r") as f:
        # Evaluate an expression node or a string containing only a Python literal or container display. The string
        # or node provided may only consist of the following Python literal structures: strings, bytes, numbers,
        # tuples, lists, dicts, sets, booleans, None and Ellipsis.
        data = ast.literal_eval(f.read())
    for credentials in data:
        if credentials["username"] == username and credentials["password"] == password:
            print("Login Successful")
            return True
    print("Login Failed!")
    return False

def check_username(username):
    with open(USER_DB, "r") as f:
        if not check_file_empty(USER_DB):
            data = ast.literal_eval(f.read())
        else:
            data = []

    for credentials in data:
        if credentials["username"] == username:
            print("User already exist!")
            return False
    print("Name available!")
    return True

def check_login():
    check = False
    username, password =" " " "
    while not check:
        username = input("Enter the username: \n")
        password = hash_pass(input("Enter the password: \n"))
        check = check_credentials(username, password)
    return check, username, password

def hash_pass(psw):
    psw_bytes = psw.encode("utf-8")
    hash_obj = hashlib.sha256(psw_bytes)
    return hash_obj.hexdigest()

def check_service(username, service):
    """This function is used to log in. It loads the file where credentials are saved and matches them with user input"""
    with open(username+"_DB.txt", "r") as f:
        data = ast.literal_eval(f.read())
    for service_dict in data:
        if service_dict["service"] == service:
            print(f"{service_dict["service"]}"+ " exist!")
            return service_dict
        else :
            print("Service does not exist!")



def create_account():
    username = ""
    flag = False
    while not flag:
        username = input("Enter the username for your new account: \n")
        flag = check_username(username)
    psw = hash_pass(input("Enter the password for the new account: \n"))
    salt = os.urandom(16)
    with open(USER_DB, "r+") as f:
        if not check_file_empty(USER_DB):
            data = ast.literal_eval(f.read())
            index = str(len(data) + 1)
        else:
            data = []
            index = "1"
        # Data is a list, so the new user is appended.
        user_dict = {"username": username, "password": psw, "salt": salt.hex(), "index": index}
        data.append(user_dict)
        # The method seek() to move the cursor back to the beginning of the file then start writing.
        f.seek(0)
        json.dump(data, f)
        print("User added!")
        generate_key(username, psw, salt)

def generate_key(username, psw, salt):

    kdf = Scrypt(salt=salt,length=32,n=2 ** 14,r=8,p=1)
    input_string = bytes(username+psw, "utf-8")
    key = kdf.derive(input_string).hex()
    print("WARNING: If this message appear, the fresh account has no KEY for encryption and decryption operations.\n"
          "Follow the next steps:\n"
          "\t1) Open a terminal\n "
          "\t2) Write the command <sudo nano(or vim) /etc/environment>\n"
          f"\t3) Add the line <$KEY_PM_N = {key}\n"
          f"\t   N is the generic N-th user that want to create a personal account\n"
          f"\t   So, for example, if this is the first running of the script, you will be the first account (so change N with 1)\n"
          f"\t4) Restart the system to set the KEY as an environmental variable.\n"
          "Quitting the script.")
    sys.exit(1)
