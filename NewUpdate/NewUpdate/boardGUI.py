import tkinter as tk  # For GUI components
from tkinter import messagebox  # For dialog boxes
import mysql.connector  # For database operations
import adminReview  # Import the admin review module
import editDelete  # Import the edit and delete module
import loginGUI
import boardCreateGUI
import boardSelectGUI  # Import the board select module

def discussion_board_gui(is_admin=False):
    discussion_board_window = tk.Tk()
    discussion_board_window.title("Discussion Boards")
    discussion_board_window.geometry("600x400")

    button_frame = tk.Frame(discussion_board_window)
    button_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    listbox = tk.Listbox(discussion_board_window)
    listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_info_frame = tk.Frame(discussion_board_window)
    user_info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

    member_id_label = tk.Label(user_info_frame, text=f"User ID: {loginGUI.current_member_id}")
    member_id_label.pack(pady=5)

    board_ids = []

    def load_boards():
        listbox.delete(0, tk.END)
        board_ids.clear()
        try:
            connection = boardCreateGUI.get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT boardID, topic FROM board")
            boards = cursor.fetchall()
            cursor.close()
            connection.close()

            for board in boards:
                board_id, topic = board
                board_ids.append(board_id)
                listbox.insert(tk.END, topic)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def logout():
        discussion_board_window.destroy()
        import main
        main.main()

    def open_board_selection(event):
        selected_index = listbox.curselection()
        if not selected_index:
            return
        board_id = board_ids[selected_index[0]]
        board_topic = listbox.get(selected_index)
        boardSelectGUI.create_board_select_gui(board_id, board_topic)

    listbox.bind('<Double-1>', open_board_selection)  # Bind double-click event to open board selection

    button_logout = tk.Button(button_frame, text="Logout", command=logout, width=20, height=2)
    button_logout.pack(pady=5)

    create_board_button = tk.Button(button_frame, text="Create Board", command=lambda: boardCreateGUI.create_board_window(load_boards), width=20, height=2)
    create_board_button.pack(pady=5)

    def edit_board():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a board to edit.")
            return
        board_id = board_ids[selected_index[0]]
        board_content = listbox.get(selected_index)
        editDelete.open_edit_gui(board_id, board_content, listbox, board_ids)

    def delete_board():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a board to delete.")
            return
        board_id = board_ids[selected_index[0]]
        board_content = listbox.get(selected_index)
        editDelete.open_delete_gui(board_id, board_content, listbox, board_ids)

    edit_button = tk.Button(button_frame, text="Edit", command=edit_board, width=20, height=2)
    edit_button.pack(pady=5)

    delete_button = tk.Button(button_frame, text="Delete", command=delete_board, width=20, height=2)
    delete_button.pack(pady=5)

    if is_admin:
        review_button = tk.Button(button_frame, text="Review Admin Requests", command=adminReview.open_admin_review_gui, width=20, height=2)
        review_button.pack(pady=5)

    load_boards()
    discussion_board_window.mainloop()