from cs50 import SQL
from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from tabulate import tabulate
import os
import random

# Clear the console screen (Windows-specific command).
os.system("cls")

# Create the database file if it doesn't exist.
open("passwords.db", "a+").close()

# Connect to the SQLite database.
db = SQL("sqlite:///passwords.db")

# Create a table 'passwords' if it doesn't already exist, with columns for the password name and the password itself.
db.execute("CREATE TABLE IF NOT EXISTS passwords(password_name TEXT, password TEXT)")

def main():
    """
    Main function to display the menu and handle user input for different operations.
    """
    while True:
        try:
            # Display the menu options.
            print("1. Generate Password")
            print("2. Add Password")
            print("3. Delete Password")
            print("4. Update Password")
            print("5. Show Passwords")
            print("6. Exit")

            # Get user input for the desired operation.
            operation = int(input())

            # Call the corresponding function based on user input.
            if operation == 1:
                generated_pass = generate_password()
                print(f"Generated Password: {generated_pass}", end='\n\n')
                save_generated(generated_pass)
            elif operation == 2:
                add_password()
            elif operation == 3:
                delete_password()
            elif operation == 4:
                update_password()
            elif operation == 5:
                show_passwords()
            elif operation == 6:
                exit("Good Bye ^_^")  # Exit the program.
            else:
                raise ValueError
        except ValueError:
            # Handle invalid input for menu selection.
            print("Please enter a valid number of operation", end="\n\n")
            return main()
        except KeyboardInterrupt:
            print()
            exit("Force Exiting .....")

def generate_password():
    """
    Function to generate a random password based on user-specified criteria.
    """
    try:
        # Get the desired length of the password from the user.
        length = int(input("Password Length: "))
        if length < 4:
            raise ValueError  # Password length must be at least 4.
    except ValueError:
        # Handle invalid input for password length.
        print("Please enter a number for password length that is equal or greater than 4", end="\n\n")
        return generate_password()
        
    try:
        # Get user preferences for including different character types in the password.
        password = []
        nums = input("- Include numbers? [yes, no]: ").lower().strip()
        if nums not in ["yes", "y", "no", "n"]:
            raise ValueError
        lows = input("- Include small letters? [yes, no]: ").lower().strip()
        if lows not in ["yes", "y", "no", "n"]:
            raise ValueError
        caps = input("- Include capital letters? [yes, no]: ").lower().strip()
        if caps not in ["yes", "y", "no", "n"]:
            raise ValueError
        puncs = input("- Include special characters? [yes, no]: ").lower().strip()
        if puncs not in ["yes", "y", "no", "n"]:
            raise ValueError

        pass_contain = []

        # Add the corresponding character sets to the password pool based on user choices.
        if nums in ["y", "yes"]:
            pass_contain += digits
        if lows in ["y", "yes"]:
            pass_contain += ascii_lowercase
        if caps in ["y", "yes"]:
            pass_contain += ascii_uppercase
        if puncs in ["y", "yes"]:
            pass_contain += punctuation
        
        # Ensure that at least one character type is selected.
        if not pass_contain:
            print("You must select at least one character type for your password!")
            return generate_password()
        
        # Generate the password using the selected character types.
        for _ in range(length):
            password.append(random.choice(pass_contain))
        
        return ''.join(password)  # Return the generated password as a string.
    except ValueError:
        # Handle invalid input for character type inclusion.
        print("Please enter yes or no", end="\n\n")
        return generate_password()

def add_password():
    """
    Function to save a password in the database.
    """
    try:
        # Get the name associated with the password from the user.
        pass_name = input("Password for: ")
        if not pass_name.isalpha():
            raise ValueError  # The name should be alphabetic only.
        
        # Get the password to be saved from the user.
        password = input("Password: ")
        
        # Insert the password into the database.
        db.execute("INSERT INTO passwords VALUES(?, ?)", pass_name, password)
        print("Password Saved", end="\n\n")
    except ValueError:
        # Handle invalid input for password name.
        print("Please enter what the password is for. ex: facebook, instagram")
        return add_password()

def show_passwords():
    """
    Function to display saved passwords based on user preference.
    """
    data = db.execute("SELECT * FROM passwords")
    if len(data) == 0:
        print("There are no data to display it", end="\n\n")
        return
    
    try:
        # Get user choice for showing specific, all, or no passwords.
        show = int(input("1. Show Specific Password\n2. Show All Passwords\n3. Back to main\n"))
        if show == 1:
            # Show a specific password based on its name.
            pass_name = input("Password name: ")
            data = db.execute("SELECT * FROM passwords WHERE password_name LIKE (?)", pass_name)
            if len(data) == 0:
                print("No data for password name to display it", end="\n\n")
            else:
                print(tabulate(data, headers="keys", tablefmt="grid"), end="\n\n")
        elif show == 2:
            # Show all saved passwords.
            print(tabulate(data, headers="keys", tablefmt="grid"), end="\n\n")
        elif show == 3:
            # Go back to the main menu.
            return
        else:
            raise ValueError
    except ValueError:
        # Handle invalid input for show option.
        print("Please enter 1 or 2 or 3")
        return show_passwords()
    
def delete_password():
    """
    Function to delete passwords from the database.
    """
    search_for_data = db.execute("SELECT * FROM passwords")
    if len(search_for_data) == 0:
        print("There are no data to delete it", end="\n\n")
        return 
    
    try:
        # Get user choice for deleting specific, all, or no passwords.
        delete = int(input("1. Delete Specific Password\n2. Delete All Passwords\n3. Back to main\n"))
        if delete == 1:
            # Delete a specific password based on its name.
            while True:
                pass_name = input("Password name: ")
                if pass_name:
                    break

            search_for_pass = db.execute("SELECT * FROM passwords WHERE password_name LIKE (?)", pass_name)
            if len(search_for_pass) == 0:
                print("No data for password name to delete it", end="\n\n")
            else:
                db.execute("DELETE FROM passwords WHERE password_name LIKE (?)", pass_name)
                print(f"{pass_name.title()} Deleted Successfully",end="\n\n")
        elif delete == 2:
            # Delete all saved passwords.    
            db.execute("DELETE FROM passwords")
            print("All Data Deleted Successfully", end="\n\n")
        elif delete == 3:
            # Go back to the main menu.
            return
        else:
            raise ValueError
    except ValueError:
        # Handle invalid input for delete option.
        print("Please enter 1 or 2 or 3")
        return delete_password()
    
def update_password():
    """
    Function to update an existing password in the database.
    """
    search_for_pass = db.execute("SELECT * FROM passwords")
    if len(search_for_pass) == 0:
        print("No data to update it", end="\n\n")
        return
    # Get the name associated with the password to be updated.
    pass_name = input("Password name: ")
    if not pass_name:
        print("You didn't enter a password name")
        return update_password()
    
    search_for_pass = db.execute("SELECT * FROM passwords WHERE password_name LIKE (?)", pass_name)
    if len(search_for_pass) == 0:
        print("No data for password name to update it", end="\n\n")
    else:
        # Get the new password from the user.
        while True:
            new_pass = input(f"Enter New Password For {pass_name}: ")
            if new_pass:
                break

        db.execute("UPDATE passwords SET password = (?) WHERE password_name LIKE (?)", new_pass, pass_name)
        print(f"{pass_name.title()} Updated Successfully", end="\n\n")

def save_generated(generated_pass):
    try:
        save = input("Do you want to save it? [yes, no]: ").lower().strip()
        if save in ["y", "yes"]:
            while True:
                pass_name = input("Password for: ").strip()
                if not pass_name.isalpha():
                    print("Please enter what the password is for. ex: facebook, instagram")
                else:
                    break
            db.execute("INSERT INTO passwords VALUES(?, ?)", pass_name, generated_pass)
            print("Password Saved", end="\n\n")
        elif save in ["n", "no"]:
            return
        else:
            raise ValueError
    except ValueError:
        print("Please enter yes or no", end="\n\n")
        return save_generated(generated_pass)
    

if __name__ == "__main__":
    # Run the main function when the script is executed.
    main()
