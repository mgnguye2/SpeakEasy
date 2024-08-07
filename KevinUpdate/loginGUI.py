import mysql.connector  # For database operations
import tkinter as tk  # For GUI
from tkinter import messagebox  # For dialog boxes


# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to validate user credentials
def check_creds(member_id, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT admin FROM member WHERE memberID = %s AND password = %s"
        cursor.execute(query, (member_id, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return result[0], member_id  # Return admin status and member ID
        return None, None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None, None

# Function to handle login logic
def login(entry_user, entry_password):
    global current_member_id
    member_id = entry_user.get()
    password = entry_password.get()
    is_admin, member_id = check_creds(member_id, password)

    if is_admin is not None:
        current_member_id = member_id  # Store the member ID globally
        messagebox.showinfo("Login Success", f"Welcome! User ID: {current_member_id}")
        return is_admin  # Return admin status
    else:
        messagebox.showerror("Login Failed", "Invalid ID or Password")
        return None

# Function to set up the login GUI
def create_login_gui(root):
    label_user = tk.Label(root, text="ID")
    label_user.grid(row=0, column=0, padx=10, pady=10)

    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(root, text="Password")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    return entry_user, entry_password
