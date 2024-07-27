import tkinter as tk
from loginGUI import create_login_gui
from createAccountGUI import create_account_gui

# Create main window
root = tk.Tk()
root.title("Login")

# Create and place widgets for login
entry_user, entry_password = create_login_gui(root)

# Add Create Account button
button_create_account = tk.Button(root, text="Create Account", command=lambda: create_account_gui(root))
button_create_account.grid(row=3, column=0, columnspan=2, pady=10)

# Run main loop
root.mainloop()