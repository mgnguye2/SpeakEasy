import mysql.connector
import tkinter as tk
from tkinter import messagebox

# this function connects to db and checks the credentials against the member table
def check_creds(member_id, password):
    try:
        connection = mysql.connector.connect(
            host="107.180.1.16",
            user="summer2024team4",
            password="summer2024team4",
            database="summer2024team4"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM member WHERE memberID = %s AND password = %s"
        cursor.execute(query, (member_id, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# login function and pop ups for success or fail
def login():
    member_id = entry_user.get()
    password = entry_password.get()

    if check_creds(member_id, password):
        messagebox.showinfo("Login Success", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid ID or Password")

# create main window
root = tk.Tk()
root.title("Login")

# create and place widgets
label_user = tk.Label(root, text="ID")
label_user.grid(row=0, column=0, padx=10, pady=10)

entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(root, text="Password")
label_password.grid(row=1, column=0, padx=10, pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

button_login = tk.Button(root, text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

# run main loop
root.mainloop()



