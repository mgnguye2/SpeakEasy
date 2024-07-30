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
def create_user(member_id, password, apply_for_admin=False):
    if len(password) < 5:
        messagebox.showerror("Error", "Password must be at least 5 characters long.")
        return
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO member (memberID, active, password, admin, votes, admin_request) VALUES (%s, 1, %s, 0, 0, %s)"
        cursor.execute(query, (member_id, password, apply_for_admin))
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

    label_apply_admin = tk.Label(create_account_window, text="Apply for Admin (Optional)")
    label_apply_admin.grid(row=3, column=0, padx=10, pady=10)

    apply_admin_var = tk.IntVar()
    apply_admin_check = tk.Checkbutton(create_account_window, variable=apply_admin_var)
    apply_admin_check.grid(row=3, column=1, padx=10, pady=10)

    def create_account():
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        apply_for_admin = apply_admin_var.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        create_user(username, password, apply_for_admin)
        create_account_window.destroy()

    button_create_account = tk.Button(create_account_window, text="Create Account", command=create_account)
    button_create_account.grid(row=4, column=0, columnspan=2, pady=10)

    create_board_button = tk.Button(root, text="Create Board", command=open_board_gui)
    create_board_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    create_account_gui(root)
    root.mainloop()
