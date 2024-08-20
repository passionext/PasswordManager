import ast
import base64
import hashlib
import os
from cryptography.fernet import Fernet
import script


def gen_fernet_key(passcode: bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def encrypt_file(filename, username):
    print (f"{filename} is going to be encrypted with the key in the system. WAIT....")
    user_index = get_index(username)
    passcode = os.environ["KEY_PM_" + user_index]
    passcode = bytes(passcode, "utf-8")[:32]
    key = base64.urlsafe_b64encode(passcode)
    fernet = Fernet(key)
    with open(filename, "rb+") as f:
        data = f.read()
        encrypted_data = fernet.encrypt(data)
        f.seek(0)
        f.write(encrypted_data)


def decrypt_file(filename,username):
    user_index = get_index(username)
    passcode = os.environ["KEY_PM_" + user_index]
    passcode = bytes(passcode, "utf-8")[:32]

    key = base64.urlsafe_b64encode(passcode)
    fernet = Fernet(key)
    if not script.check_file_empty(filename):
        with open(filename, "rb+") as f:
            encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            f.seek(0)
            f.write(decrypted_data)
            f.truncate()




def get_index(username):
    with open("USER_DB.txt", "r") as f:
        data = ast.literal_eval(f.read())
        for user_dict in data:
            if user_dict["username"] == username:
                index = user_dict["index"]
                type(index)
                return index
