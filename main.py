import inquirer
import script
import password


#This is the main DB file with all the users registered in the script.
USER_DB ="USER_DB.txt"



def loading_file():
    """This method is used to check if the USER_DB exist and is NOT empty. The check_file_exist has his own
    documentation. The method check_file_empty is used because ast.literal_eval(f.read()) returns error when the file
    is empty, so is mandatory to create an account first."""
    #First, it checks if the USER_DB file exist.
    script.check_file_exist(USER_DB)
    #Then, for avoiding error with methods that need to read the file, it checks if the USER_DB file is empty.
    if script.check_file_empty(USER_DB):
        print("***WARNING***: File USER_DB exist, however it is empty! Login is disabled.\n")
        print("Creating an account....")
        # This method cannot be included in check_file_empty, due circular import. This error occurs when two
        # modules mutually dependent on each other try to import before fully loading. It causes a loop in which each
        # function tries to load the other and fails, creating unpredictable behavior and runtime errors.
        script.create_account()



def first_menu():
    print("Welcome into the pre-release of the Password Manager.\n")
    questions = [
        inquirer.List(
            "choice",
            message="Select an option:",
            choices=["Create an account", "Log In"],
        ),
    ]
    # Variable answers contains the choices selected from the inquirer, is a dictionary where the key is the name on
    # the list and the value is one of the possible choices.
    answers = inquirer.prompt(questions)
    if answers["choice"] == "Create an account":
        script.create_account()
    # No else; maybe it's better if check_login (LOGIN Method) is run in main rather than in the script method.



def user_menu(username):
    """This is the meny dedicated to each user, where services can be added, seen or modified."""
    while True:
        questions = [
            inquirer.List(
            "choice",
            message="What do you want to do?",
            choices=["Add a Service", "View a Service", "Modify a Service", "Exit"],
            ),
        ]
    # Variable answers contains the choices selected from the inquirer, is a dictionary where the key is the name on
    # the list and the value is one of the possible choices.
        answers = inquirer.prompt(questions)
        match answers["choice"]:
            case "Add a Service":
                print("Welcome to the Password Manager!\n")
                password.add_service(username)
            case "View a Service":
                password.view_service(username)
                print("Welcome to the Password Manager!\n")
            case "Modify a Service":
                password.modify_service(username)
                print("Welcome to the Password Manager!\n")
            case "Exit":
                break



def main():
    #First of all, it is necessary to check if all the files are in the directory of this script.
    loading_file()
    #Launching first menu.
    first_menu()
    # After clicking log in on the first menu, it returns here and continues with the next line (LOG-IN)
    log, username, psw = script.check_login()
    # If log returns True, so that the login procedure is successful, then proceed.
    if log:
        # After logging in, it checks if the user has his own DB files, where all the passwords are going to be stored.a
        if not script.check_file_exist(username+"_DB.txt"):
            print("Now the user DB personal is going to be saved.")
    user_menu(username)

# EXECUTE SCRIPT
main()