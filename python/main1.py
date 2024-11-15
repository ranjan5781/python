import os
import datetime

MIN_SAVINGS_BALANCE = 100
MIN_CURRENT_BALANCE = 500

def display_menu():
    print("Welcome to banking service")
    print("1. Login")
    print("2. Exit")
    choice = input("Enter your choice: ")
    return choice

def customer_login_service():
    account_number = input("Enter your account number: ")
    password = input("Enter the password: ")

    if os.path.exists("customers.txt"):
        with open("customers.txt", "r") as file:
            for line in file:
                data = line.split(",")
                if data[0] == account_number and data[2] == password:
                    print("Login successful!")
                    return account_number
                print("Invalid account number or password. Try again.")
            return None
    else:
        print("No customer account found. Please register first.")
        return None

def deposit_transaction(account_number):
    amount = float(input("Enter the amount to deposit: "))

    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return

    updated = False
    if os.path.exists("customers.txt"):
        with open("customers.txt", "r") as file:
            lines = file.readlines()

        with open("customers.txt", "w") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == account_number:
                    current_balance = float(data[3])
                    new_balance = current_balance + amount
                    file.write(f"{data[0]},{data[1]},{data[2]},{new_balance}\n")
                    print(f"Deposit successful! Current balance: {new_balance}")
                    updated = True
                else:
                    file.write(line)
        if not updated:
            print("Account not found.")
    else:
        print("No customer accounts found.")

def withdrawal_transaction(account_number, account_type):
    amount = float(input("Enter the amount to withdraw: "))

    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return

    updated = False
    if os.path.exists("customers.txt"):
        with open("customers.txt", "r") as file:
            lines = file.readlines()

        with open("customers.txt", "w") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == account_number:
                    current_balance = float(data[3])
                    if account_type == "Savings" and current_balance - amount < MIN_SAVINGS_BALANCE:
                        print("Withdrawal amount exceeds minimum balance for Savings account.")
                        file.write(line)
                        return
                    elif account_type == "Current" and current_balance - amount < MIN_CURRENT_BALANCE:
                        print("Withdrawal amount exceeds minimum balance for Current account.")
                        file.write(line)
                        return
                    else:
                        new_balance = current_balance - amount
                        file.write(f"{data[0]},{data[1]},{data[2]},{new_balance}\n")
                        print(f"Withdrawal successful! Current balance: {new_balance}")
                        updated = True
                else:
                    file.write(line)
        if not updated:
            print("Account not found.")
    else:
        print("No customer accounts found.")

def generate_statement(account_number):
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    if start_date > end_date:
        print("Start date cannot be after end date.")
        return

    if os.path.exists("customer_transactions.txt"):
        transactions = []
        with open("customer_transactions.txt", "r") as file:
            for line in file:
                transaction_data = line.strip().split(",")
                if transaction_data[0] == account_number:
                    trans_date = datetime.datetime.strptime(transaction_data[1], "%Y-%m-%d")
                    if start_date <= trans_date <= end_date:
                        transactions.append(transaction_data)

        if transactions:
            print(f"Statement of Account for Account Number: {account_number}")
            print("Transaction Date\tType\tAmount")
            total_deposit = 0
            total_withdrawal = 0
            for transaction in transactions:
                print(f"{transaction[1]}\t{transaction[2]}\t{transaction[3]}")
                if transaction[2] == "Deposit":
                    total_deposit += float(transaction[3])
                elif transaction[2] == "Withdrawal":
                    total_withdrawal += float(transaction[3])
            print(f"Total deposits: {total_deposit}")
            print(f"Total withdrawals: {total_withdrawal}")
        else:
            print("No transactions found in the given date range.")
    else:
        print("No transactions found.")

def update_password(account_number):
    new_password = input("Enter your new password: ")

    updated = False
    if os.path.exists("customers.txt"):
        with open("customers.txt", "r") as file:
            lines = file.readlines()

        with open("customers.txt", "w") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[0] == account_number:
                    file.write(f"{data[0]},{data[1]},{new_password},{data[3]}\n")
                    print("Password updated successfully!")
                    updated = True
                else:
                    file.write(line)
        if not updated:
            print("Account not found.")
    else:
        print("No customer accounts found.")

def main1():
    while True:
        choice = display_menu()
        if choice == '1':
            account_number = customer_login_service()
            if account_number:
                while True:
                    print("\nCustomer Menu:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Generate Statement")
                    print("4. Update Password")
                    print("5. Logout")
                    customer_choice = input("Enter your choice: ")
                    if customer_choice == '1':
                        deposit_transaction(account_number)
                    elif customer_choice == '2':
                        account_type = input("Enter account type (Savings/Current): ")
                        withdrawal_transaction(account_number, account_type)
                    elif customer_choice == '3':
                        generate_statement(account_number)
                    elif customer_choice == '4':
                        update_password(account_number)
                    elif customer_choice == '5':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '2':
            print("Thank you for using our system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
#main1()