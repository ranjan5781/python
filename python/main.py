import os
import datetime
import random
import json
from main1 import *

SUPER_USER_FILE = 'super_user.txt'
ADMIN_STAFF_FILE = 'admin_staff.txt'
CUSTOMERS_FILE = 'customers.txt'

def name_validation():
    username = input("Confirm your name :")
    while True:
        if username.isalpha():
            break
        else:
            print("Invalid name Please input alphabet only")
            username = input("Enter a Valied Name :")
            
def get_mixed_format_password():
    while True:
        password = input("Enter Password: ")
        if len(password) == 8:
            return password
        else:
            print("Password must be 8 characters long and contain both letters and numbers.")
def email_validation(): 
    email = input("Confirm your  Email: ")
    while True:
        if email.endswith("@gmail.com") or email.endswith("@hotmail.com") or email.endswith("@yahoo.com"):
            break
        else:
            print("Invalid Email Please Enter valid email")
            email = input("Enter Superuser Email: ")    
            
def phno_num_validation():
    phone = input("Confirm Phone: ")
    while True:
        if phone.isdigit():
            if len(phone)==10:
                break
            else:
                print("phone number must be of 10 digit")
                phone = input("Plse Enter Valied Phone number :")
        else:
            print("phone number must be digit only")
            phone = input("Phone number you have enter is invalied Enter again :")

def get_mixed_format_password():
    while True:
        password = input("Enter Password: ")
        if len(password) == 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password):
            return password
        else:
            print("Password must be 8 characters long and contain both letters and numbers.")

def generate_account_number():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            customers = json.load(file)
    else:
        customers = {}
    while True:
        account_number = random.randint(1000000000, 9999999999)
        if str(account_number) not in customers:
            print(account_number)
            return account_number

def save_super_user(super_user):
    with open(SUPER_USER_FILE, 'w') as file:
        file.write(f"{super_user['username']},{super_user['password']},{super_user['email']},{super_user['phone']}\n")

def load_super_user():
    if os.path.exists(SUPER_USER_FILE):
        with open(SUPER_USER_FILE, 'r') as file:
            line = file.readline().strip().split(',')
            return {'username': line[0], 'password': line[1], 'email': line[2], 'phone': line[3]}
    return None

def save_admin_staff():
    with open(ADMIN_STAFF_FILE, 'w') as file:
        for username, details in admin_staff.items():
            file.write(f"{username},{details['password']},{details['email']},{details['phone']}\n")

def load_admin_staff():
    admin_staff = {}
    if os.path.exists(ADMIN_STAFF_FILE):
        with open(ADMIN_STAFF_FILE, 'r') as file:
            for line in file:
                line = line.strip().split(',')
                admin_staff[line[0]] = {'password': line[1], 'email': line[2], 'phone': line[3]}
    return admin_staff

def save_customers():
    with open(CUSTOMERS_FILE, 'w') as file:
        json.dump(customers, file)

def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def create_admin_staff(username, password, email, phone):
    admin_staff[username] = {
        'password': password,
        'email': email,
        'phone': phone
    }
    save_admin_staff()
    print(f"Admin staff {username} created successfully.")



def generate_statement(account_number, start_date, end_date):
    if str(account_number) in customers:
        statement = [txn for txn in transactions[account_number] if start_date <= txn['date'] <= end_date]
        total_deposits = sum(txn['amount'] for txn in statement if txn['type'] == 'deposit')
        total_withdrawals = sum(txn['amount'] for txn in statement if txn['type'] == 'withdrawal')
        
        print(f"Statement for account {account_number} from {start_date} to {end_date}:")
        for txn in statement:
            print(f"{txn['date']}: {txn['type']} of {txn['amount']}")
        print(f"Total deposits: {total_deposits}")
        print(f"Total withdrawals: {total_withdrawals}")
    else:
        print(f"Customer account {account_number} not found.")

def main():
    global admin_staff, customers, transactions
    
    print("WELCOME TO THE BANKING SYSTEM")
    admin_staff = load_admin_staff()

    while True:
        print("\nWELCOME TO THE SYSTEM, SELECT ONE OF THE CHOICES")
        print("\n1. Create Superuser Account")
        print("2. Login as Super User")
        print("3. Login as Admine_Staff")
        print("4. Login as Customer")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_superuser_account()
        elif choice == '2':
            login_super_user()
        elif choice == '3':
            login_Admine_staff()
        elif choice == '4':
            login_customer()
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def create_superuser_account():
    username =input("enter the Superusername: ")
    name_validation()
    password = input("Enter Superuser Password: ")
    get_mixed_format_password()
    email = input("Enter Superuser Email: ")
    email_validation()
    phone = input("Enter Superuser Phone: ")
    phno_num_validation()
    super_user = {'username': username, 'password': password, 'email': email, 'phone': phone}
    save_super_user(super_user)
    print("Superuser account created successfully.")

def login_super_user():
    super_user = load_super_user()
    
    if not super_user:
        print("Superuser account does not exist.")
        return

    while True:
        username = input("Enter Superuser Username: ")
        password = input("Enter Superuser Password: ")
        
        if username == super_user.get('username') and password == super_user.get('password'):
            print("Superuser logged in successfully.")
            while True:
                print("\n1. Create Admin Staff Account")
                print("2. Login Admin staff account")
                print("3. Logout")
                choice = input("Enter your choice: ")
                if choice == '1':
                    admin_username = input("Enter Admin Staff Username: ")
                    admin_password = input("Enter Admin Staff Password: ")
                    get_mixed_format_password()
                    admin_email = input("Enter Admin Staff Email: ")
                    email_validation()
                    admin_phone = input("Enter Admin Staff Phone: ")
                    phno_num_validation()
                    create_admin_staff(admin_username, admin_password, admin_email, admin_phone)
                elif choice == '2':
                    login_Admine_staff()
                    break
                elif choice == '3':
                    print("Logging out...")
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid credentials. Please try again.")

def login_Admine_staff():
    while True:
        username = input("Enter Staff Username: ")
        password = input("Enter Staff Password: ")
        if username in admin_staff and admin_staff[username]['password'] == password:
            print("Staff logged in successfully.")
            while True:
                print("1. Create Customer account")
                print("2. Login as Customer account")
                print("3. Logout")
                    
                c = int(input("Enter the choice: "))
                if c == 1:
                    register_customer()
                elif c == 2:
                    main1()
                elif c == 3:
                    print("Logging out...")
                    break
                else:
                    print("Please enter a valid number.")
            break
        else:
            print("Incorrect Username or Password. Please try again.") 

def register_customer():
    Account_num=generate_account_number()
    C_username = input("Enter Admin Staff Username: ")
    name_validation()
    C_password = input("Enter Admin Staff Password: ")
    get_mixed_format_password()
    C_email = input("Enter Admin Staff Email: ")
    email_validation()
    C_phone = input("Enter Admin Staff Phone: ")
    phno_num_validation()
    print("Account Create Successfully")
    save_customers()

def login_customer():
    main1()


main()