import tkinter as tk
from tkinter import messagebox
import mysql.connector



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
    listbox.pack(padx=10, pady=10)

    def load_boards():
        try:
            # Connect to the MySQL database and load boards
            conn = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM boards')
            boards = cursor.fetchall()
            for board in boards:
                listbox.insert(tk.END, board[0])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def open_board(event):
        selected_board_index = listbox.curselection()
        if selected_board_index:
            selected_board_name = listbox.get(selected_board_index)
            display_board_content(selected_board_name)

    def display_board_content(board_name):
        try:
            # Connect to the MySQL database and fetch the content of the selected board
            conn = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = conn.cursor()
            cursor.execute(
                'SELECT content FROM boards WHERE name = %s', (board_name,))
            board_content = cursor.fetchone()
            cursor.close()
            conn.close()

            # Display the content in a new window
            board_window = tk.Toplevel(discussion_board_window)
            board_window.title(board_name)

            content_label = tk.Label(board_window, text="Board Content:")
            content_label.pack(pady=5)

            text_box = tk.Text(board_window, height=10, width=40)
            text_box.pack(padx=10, pady=10)
            if board_content:
                text_box.insert(tk.END, board_content[0])

            def save_content():
                new_content = text_box.get("1.0", tk.END)
                try:
                    conn = mysql.connector.connect(
                        host="107.180.1.16",
                        user="summer2024team4",
                        password="summer2024team4",
                        database="summer2024team4"
                    )
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE boards SET content = %s WHERE name = %s', (new_content, board_name))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo(
                        "Success", "Content saved successfully")
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")

            save_button = tk.Button(
                board_window, text="Save", command=save_content)
            save_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    listbox.bind('<<ListboxSelect>>', open_board)

    load_boards()

    # Entry widget for new board name
    new_board_entry = tk.Entry(discussion_board_window)