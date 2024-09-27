import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import getpass

# Connect to SQLite3 database
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Create users and transactions tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT NOT NULL,  -- Income or Expense
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()

# Function for user registration
def register():
    print("=== User Registration ===")
    username = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")

    cursor.execute('''
    INSERT INTO users (username, password)
    VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    print("Registration successful!")

# Function for user login
def login():
    print("=== User Login ===")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute('''
    SELECT id FROM users WHERE username=? AND password=?
    ''', (username, password))
    result = cursor.fetchone()

    if result:
        print("Login successful!")
        return result[0]  # Return user_id
    else:
        print("Invalid credentials. Please try again.")
        return None

# Function to add a transaction for a logged-in user
def add_transaction(user_id):
    print("=== Add Transaction ===")
    transaction_type = input("Enter transaction type (Income/Expense): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute('''
    INSERT INTO transactions (user_id, type, category, amount, date)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, transaction_type, category, amount, date))
    conn.commit()
    print("Transaction added successfully!")

# Function to view transactions of the logged-in user
def view_transactions(user_id):
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id=?', conn, params=(user_id,))
    print(df)
    return df

# Function to generate report for a logged-in user
def generate_report(user_id):
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id=? AND type="Expense"', conn, params=(user_id,))
    report = df.groupby('category')['amount'].sum().reset_index()
    print("Expense Report:")
    print(report)
    return report

# Function to visualize expenses using a pie chart for a logged-in user
def visualize_expenses(user_id):
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id=? AND type="Expense"', conn, params=(user_id,))
    expense_summary = df.groupby('category')['amount'].sum()

    plt.figure(figsize=(7, 7))
    expense_summary.plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title("Expenses Breakdown by Category")
    plt.ylabel('')
    plt.show()

# Function to set and track budget goals for a logged-in user
def set_budget_goal(user_id, budget, category):
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id=? AND type="Expense" AND category=?', conn, params=(user_id, category))
    total_spent = df['amount'].sum()

    print(f"Total spent on {category}: {total_spent}")
    print(f"Budget for {category}: {budget}")

    if total_spent > budget:
        print(f"Warning: You have exceeded your budget for {category}!")
    else:
        print(f"Good job! You are within the budget for {category}.")

# Function to export transactions to CSV for a logged-in user
def export_to_csv(user_id, filename='transactions.csv'):
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id=?', conn, params=(user_id,))
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

# Function to edit an existing transaction for a logged-in user
def edit_transaction(user_id):
    print("=== Edit Transaction ===")
    transaction_id = input("Enter the transaction ID to edit: ")

    cursor.execute('SELECT * FROM transactions WHERE user_id=? AND id=?', (user_id, transaction_id))
    transaction = cursor.fetchone()

    if transaction:
        print(f"Current Transaction: Type: {transaction[2]}, Category: {transaction[3]}, Amount: {transaction[4]}, Date: {transaction[5]}")
        new_type = input(f"Enter new type (current: {transaction[2]}): ") or transaction[2]
        new_category = input(f"Enter new category (current: {transaction[3]}): ") or transaction[3]
        new_amount = input(f"Enter new amount (current: {transaction[4]}): ") or transaction[4]
        new_date = input(f"Enter new date (YYYY-MM-DD) (current: {transaction[5]}): ") or transaction[5]

        cursor.execute('''
        UPDATE transactions
        SET type=?, category=?, amount=?, date=?
        WHERE user_id=? AND id=?
        ''', (new_type, new_category, new_amount, new_date, user_id, transaction_id))
        conn.commit()

        print("Transaction updated successfully!")
    else:
        print("Transaction not found.")

# Function to delete an existing transaction for a logged-in user
def delete_transaction(user_id):
    print("=== Delete Transaction ===")
    transaction_id = input("Enter the transaction ID to delete: ")

    cursor.execute('SELECT * FROM transactions WHERE user_id=? AND id=?', (user_id, transaction_id))
    transaction = cursor.fetchone()

    if transaction:
        cursor.execute('DELETE FROM transactions WHERE user_id=? AND id=?', (user_id, transaction_id))
        conn.commit()
        print("Transaction deleted successfully!")
    else:
        print("Transaction not found.")

# Main CLI program
def main():
    print("=== Personal Finance Tracker ===")
    
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()

        elif choice == '2':
            user_id = login()
            if user_id:
                while True:
                    print("\n1. Add Transaction\n2. View Transactions\n3. Generate Report\n4. Visualize Expenses\n5. Set Budget Goal\n6. Export Data\n7. Edit Transaction\n8. Delete Transaction\n9. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        add_transaction(user_id)
                    elif user_choice == '2':
                        view_transactions(user_id)
                    elif user_choice == '3':
                        generate_report(user_id)
                    elif user_choice == '4':
                        visualize_expenses(user_id)
                    elif user_choice == '5':
                        category = input("Enter category: ")
                        budget = float(input("Enter budget: "))
                        set_budget_goal(user_id, budget, category)
                    elif user_choice == '6':
                        filename = input("Enter filename (default: transactions.csv): ") or 'transactions.csv'
                        export_to_csv(user_id, filename)
                    elif user_choice == '7':
                        edit_transaction(user_id)
                    elif user_choice == '8':
                        delete_transaction(user_id)
                    elif user_choice == '9':
                        print("Logged out successfully!! See You Again...")
                        break
                    else:
                        print("Invalid choice! Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
