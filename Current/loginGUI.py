import mysql.connector
import tkinter as tk
from tkinter import messagebox

def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

def check_creds(member_id, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT admin FROM member WHERE memberID = %s AND password = %s"
        cursor.execute(query, (member_id, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def login(entry_user, entry_password):
    member_id = entry_user.get()
    password = entry_password.get()
    result = check_creds(member_id, password)

    if result:
        messagebox.showinfo("Login Success", "Welcome!")
        return result[0] == 1  # Return True if the user is admin, otherwise False
    else:
        messagebox.showerror("Login Failed", "Invalid ID or Password")
        return None

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
