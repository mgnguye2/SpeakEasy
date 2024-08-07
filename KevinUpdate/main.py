import tkinter as tk
import createAccountGUI
import loginGUI  # Import login-related functions and GUI setup
import boardGUI

# Main function to set up the login screen and handle the login process
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

    # Create login GUI elements using loginGUI module
    entry_user, entry_password = loginGUI.create_login_gui(root)

    frame_buttons = tk.Frame(root)
    frame_buttons.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

    button_create_account = tk.Button(frame_buttons, text="Create Account", command=lambda: createAccountGUI.create_account_gui(root), width=12, height=2)
    button_create_account.pack(side=tk.LEFT, padx=10)

    # Handle login and transition to board GUI
    def handle_login():
        is_admin = loginGUI.login(entry_user, entry_password)
        if is_admin is not None:
            root.destroy()
            boardGUI.discussion_board_gui(is_admin=is_admin)
            

    button_login = tk.Button(frame_buttons, text="Login", command=handle_login, width=12, height=2)
    button_login.pack(side=tk.LEFT, padx=10)

    # Configure the button frame to expand properly
    frame_buttons.grid_rowconfigure(0, weight=1)
    frame_buttons.grid_columnconfigure(0, weight=1)
    frame_buttons.grid_columnconfigure(1, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()