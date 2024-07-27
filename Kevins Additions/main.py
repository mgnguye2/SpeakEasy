import tkinter as tk
from loginGUI import create_login_gui, login
from createAccountGUI import create_account_gui
from boardSelectGUI import create_discussion_board_gui

def open_discussion_board_gui(root):
    create_discussion_board_gui(root)

def login_and_open_board(entry_user, entry_password, root):
    if login(entry_user, entry_password):
        open_discussion_board_gui(root)

# Create main window
def main():
    root = tk.Tk()
    root.title("Login")
    
    # Create and place widgets for login
    entry_user, entry_password = create_login_gui(root)
    
    # Add Create Account button
    button_create_account = tk.Button(root, text="Create Account", command=lambda: create_account_gui(root))
    button_create_account.grid(row=3, column=0, columnspan=2, pady=10)
    
    # Update login button to open discussion board GUI
    button_login = tk.Button(root, text="Login", command=lambda: login_and_open_board(entry_user, entry_password, root))
    button_login.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Run main loop
    root.mainloop()

if __name__ == "__main__":
    main()