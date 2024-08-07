import tkinter as tk  # For GUI components
from tkinter import messagebox
import mysql.connector
import loginGUI

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to create the board selection GUI
def create_board_select_gui(board_id, board_topic):
    # Create a new top-level window for the board view
    board_select_window = tk.Toplevel()
    board_select_window.title(f"View Board: {board_topic}")
    board_select_window.geometry("600x400")  # Set window size

    # Create a frame to hold the posts and scrollbar
    posts_frame = tk.Frame(board_select_window)
    posts_frame.pack(fill=tk.BOTH, expand=True)

    # Create a listbox and scrollbar for the posts
    listbox = tk.Listbox(posts_frame, selectmode=tk.SINGLE)
    scrollbar = tk.Scrollbar(posts_frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Dictionary to map listbox index to messageID
    message_id_map = {}

    # Function to load posts and their replies from the database
    def load_posts():
        listbox.delete(0, tk.END)  # Clear existing posts
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT messageID, message, originalPostID FROM main WHERE boardID = %s ORDER BY messageID", (board_id,))
            posts = cursor.fetchall()
            cursor.close()
            connection.close()

            for index, (post_id, message, original_post_id) in enumerate(posts):
                if original_post_id is None:
                    listbox.insert(tk.END, message)  # Display original post
                else:
                    listbox.insert(tk.END, f"↳ {message}")  # Display reply with indent
                message_id_map[index] = post_id

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    # Function to open the reply window
    def open_reply_window(original_post_id):
        reply_window = tk.Toplevel(board_select_window)
        reply_window.title("Reply to Post")
        reply_window.geometry("400x200")

        reply_text = tk.Text(reply_window, height=5, width=40)
        reply_text.pack(pady=10, padx=10)

        def submit_reply():
            reply_content = reply_text.get("1.0", tk.END).strip()
            if not reply_content:
                messagebox.showwarning("Warning", "Reply content cannot be empty.")
                return

            try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO main (message, boardID, originalPostID, memberID) VALUES (%s, %s, %s, %s)",
                               (reply_content, board_id, original_post_id, loginGUI.current_member_id))
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", "Reply submitted successfully!")
                reply_window.destroy()
                load_posts()  # Reload posts and replies
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database Error: {err}")

        submit_button = tk.Button(reply_window, text="Submit", command=submit_reply)
        submit_button.pack(pady=10)

    # Function to handle double-click on listbox
    def on_listbox_double_click(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_message_id = message_id_map[selected_index[0]]
            open_reply_window(selected_message_id)

    # Bind double-click event to the listbox
    listbox.bind("<Double-1>", on_listbox_double_click)

    load_posts()  # Load posts and replies when the window is created

    # Label and text widget for entering a new post
    post_label = tk.Label(board_select_window, text="Enter your post:")
    post_label.pack(pady=5)
    post_text = tk.Text(board_select_window, height=5, width=50)
    post_text.pack(pady=10, padx=10)

    # Function to submit a new post to the database
    def submit_post():
        post_content = post_text.get("1.0", tk.END).strip()
        if not post_content:
            messagebox.showwarning("Warning", "Post content cannot be empty.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO main (message, boardID, originalPostID, memberID) VALUES (%s, %s, NULL, %s)",
                           (post_content, board_id, loginGUI.current_member_id))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Post submitted successfully!")
            load_posts()  # Reload posts and replies
            post_text.delete("1.0", tk.END)  # Clear the text field
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    # Button to submit a new post
    submit_button = tk.Button(board_select_window, text="Submit", command=submit_post)
    submit_button.pack(pady=10)

