import re
import pwinput

def validate_email(email):
    if "@" in email and "." in email.split("@")[-1]:
        return True
    return False

def validate_password(password):
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/"
    if len(password) < 10:
        return False, "The password must consist of at least 10 characters."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char in special_characters for char in password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."

def main():
    user_email = input("Enter your email: ")
    user_password = pwinput.pwinput("Enter your password: ", mask="*")
    
    if validate_email(user_email):
        print("\nValid email.")
    else:
        print("Invalid email. Email must contain '@' and at least one '.' after '@' character.")
    
    is_valid, message = validate_password(user_password)
    print(message)
    
if __name__ == "__main__":
    main()



# This program can only be run from the Windows terminal environment, using the command:
# python3 .\User_Email-Password_Validity.py
