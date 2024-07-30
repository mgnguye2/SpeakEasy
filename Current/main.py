import tkinter as tk
from tkinter import messagebox
import mysql.connector
import createAccountGUI

def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

def login_and_open_board(entry_user, entry_password, root):
    username = entry_user.get()
    password = entry_password.get()
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member WHERE memberID = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user:
            if user[3]:  # Check if user is admin
                import boardGUI
                boardGUI.create_discussion_board_gui(root, is_admin=True)
            else:
                import boardGUI
                boardGUI.create_discussion_board_gui(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def create_login_gui(root):
    tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    return entry_user, entry_password

def main():
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x180")  # Set a smaller default size
    root.minsize(250, 150)    # Set minimum size

    # Configure grid layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    entry_user, entry_password = create_login_gui(root)

    frame_buttons = tk.Frame(root)
    frame_buttons.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

    button_create_account = tk.Button(frame_buttons, text="Create Account", command=lambda: createAccountGUI.create_account_gui(root), width=12, height=2)
    button_create_account.pack(side=tk.LEFT, padx=10)

    button_login = tk.Button(frame_buttons, text="Login", command=lambda: login_and_open_board(entry_user, entry_password, root), width=12, height=2)
    button_login.pack(side=tk.LEFT, padx=10)

    # Configure the button frame to expand properly
    frame_buttons.grid_rowconfigure(0, weight=1)
    frame_buttons.grid_columnconfigure(0, weight=1)
    frame_buttons.grid_columnconfigure(1, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
