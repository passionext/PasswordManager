import ast
import json
from datetime import datetime
import script
import encryption



def add_service(username):
    service = input("Add service name: \n")
    psw = input("Add the password: \n")
    date = datetime.now().strftime("%m/%d/%Y, %H:%M")
    serv_dict = {"service": service, "password": psw, "date": "Last modified: " + date}
    with open(username+"_DB.txt", "r+") as f:
        # Evaluate an expression node or a string containing only a Python literal or container display. The string
        # or node provided may only consist of the following Python literal structures: strings, bytes, numbers,
        # tuples, lists, dicts, sets, booleans, None and Ellipsis.
        if not script.check_file_empty(username+"_DB.txt"):
            encryption.decrypt_file(username + "_DB.txt", username)
            data = ast.literal_eval(f.read())
        else:
            data = []
        # Data is a list, so the new user is appended.
        data.append(serv_dict)
        # The method seek() to move the cursor back to the beginning of the file then start writing.
        f.seek(0)
        # Default is a function applied to objects that aren't serializable. In this case it's str, so it just
        # converts everything it doesn't know to strings.
        json.dump(data, f, default = str)
    encryption.encrypt_file(username + "_DB.txt", username)

def view_service(username):
    with open(username + "_DB.txt", "r+") as f:
        encryption.decrypt_file(username + "_DB.txt", username)
        service = input("Enter service's name: \n"
                    "Enter ALL to visualize all the items\n").lower()
        if service == "all":
            data = ast.literal_eval(f.read())
            print (data)
        else:
            service_dict = script.check_service(username, service)
            if service_dict is not None:
                print(f"This is the service extracted:\n {service_dict}")
    encryption.encrypt_file(username + "_DB.txt", username)




def modify_service(username):
    encryption.decrypt_file(username + "_DB.txt", username)
    flag = True
    service = input("Enter service's name: \n").lower()
    with open(username + "_DB.txt", "r+") as f:
        data = ast.literal_eval(f.read())
        for dict_service in data:
            if dict_service["service"] == service:
                while flag:
                    new_password = input("Enter the new password: ")
                    new_password_check = input ("Re-enter the new password: ")
                    if new_password == new_password_check:
                        dict_service ["password"] = new_password
                        print (dict_service)
                        f.seek(0)
                        json.dump(data, f, default=str)
                        flag = False
    encryption.encrypt_file(username + "_DB.txt", username)
