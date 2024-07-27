import mysql.connector
import tkinter as tk
from tkinter import messagebox
import random

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to check if the username is unique
def is_unique_username(username):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT memberID FROM member WHERE memberID = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

# Function to generate a random and unique username
def generate_unique_username():
    while True:
        username = ''.join(str(random.randint(1, 9)) for _ in range(10))
        if is_unique_username(username):
            return username

# Function to create a new user in the database
def create_user(member_id, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO member (memberID, active, password, admin, votes) VALUES (%s, 1, %s, 0, 0)"
        cursor.execute(query, (member_id, password))  # Adjust the column names as needed
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Account Created", "Your account has been successfully created!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to create the account creation GUI
def create_account_gui(root):
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")

    username = generate_unique_username()

    label_username = tk.Label(create_account_window, text=f"Your username: {username}")
    label_username.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    label_password = tk.Label(create_account_window, text="Password")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    entry_password = tk.Entry(create_account_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    label_confirm_password = tk.Label(create_account_window, text="Confirm Password")
    label_confirm_password.grid(row=2, column=0, padx=10, pady=10)

    entry_confirm_password = tk.Entry(create_account_window, show="*")
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=10)

    def create_account():
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        create_user(username, password)
        create_account_window.destroy()

    button_create_account = tk.Button(create_account_window, text="Create Account", command=create_account)
    button_create_account.grid(row=3, column=0, columnspan=2, pady=10)