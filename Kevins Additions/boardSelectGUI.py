import tkinter as tk
from tkinter import messagebox

# Sample data for discussion boards
discussion_boards = ["Board 1", "Board 2", "Board 3", "Board 4"]

# Function to create the discussion board GUI
def create_discussion_board_gui(root):
    # Close the login window
    root.destroy()
    
    # Create a new window for the discussion boards
    discussion_board_window = tk.Tk()
    discussion_board_window.title("Discussion Boards")
    
    label = tk.Label(discussion_board_window, text="Discussion Boards")
    label.pack(pady=10)
    
    listbox = tk.Listbox(discussion_board_window)
    for board in discussion_boards:
        listbox.insert(tk.END, board)
    listbox.pack(padx=10, pady=10)
    
    def logout():
        discussion_board_window.destroy()
        import main
        main.main()

    button_logout = tk.Button(discussion_board_window, text="Logout", command=logout)
    button_logout.pack(pady=10)
    
    discussion_board_window.mainloop()