import mysql.connector  # For database operations
import tkinter as tk  # For GUI
import create_account
from tkinter import messagebox  # For dialog boxes
from PIL import Image, ImageTk  # For image resizing

# Function to connect to the MySQL database
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
        query = "SELECT admin, active FROM member WHERE memberID = %s AND password = %s"
        cursor.execute(query, (member_id, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            admin_status, active = result
            if active == 1:
                return admin_status, member_id, ""  # Include a third return value
            else:
                return None, None, "Account is inactive"  # Account is inactive
        return None, None, "Invalid ID or Password"  # Credentials are incorrect
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None, None, "Error in database query"


# Function to handle login logic
def login(entry_user, entry_password):
    global current_member_id
    member_id = entry_user.get()
    password = entry_password.get()
    is_admin, member_id, message = check_creds(member_id, password)

    if is_admin is not None:
        current_member_id = member_id  # Store the member ID globally
        messagebox.showinfo("Login Success", f"Welcome! User ID: {current_member_id}")
        return is_admin, member_id  # Return admin status and member ID
    else:
        messagebox.showerror("Login Failed", message) #Specifies why in message
        return None, None

# Function to set up the login GUI
def create_login_gui(root):
    # Load and resize the logo image
    image = Image.open("SpeakEasy3.png")  # Replace with your logo image path
    image = image.resize((300, 300), Image.LANCZOS)  # Resize the image
    logo = ImageTk.PhotoImage(image)

    # Create a label for the logo and place it at the top
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    # ID label and entry
    label_user = tk.Label(root, text="ID")
    label_user.grid(row=1, column=0, padx=10, pady=10)
    entry_user = tk.Entry(root)
    entry_user.grid(row=1, column=1, padx=10, pady=10)

    # Password label and entry
    label_password = tk.Label(root, text="Password")
    label_password.grid(row=2, column=0, padx=10, pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=10)

    # Button frame for Create Account and Login buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    button_create_account = tk.Button(button_frame, text="Create Account", command=lambda: create_account.create_account_gui(root))
    button_create_account.pack(side=tk.LEFT, padx=10)

    button_login = tk.Button(button_frame, text="Login", command=lambda: login(entry_user, entry_password))
    button_login.pack(side=tk.RIGHT, padx=10)

    button_exit = tk.Button(button_frame, text="Exit", command=root.destroy)
    button_exit.pack(side=tk.RIGHT, padx=10)

    return entry_user, entry_password
