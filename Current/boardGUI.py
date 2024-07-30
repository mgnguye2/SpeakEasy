import tkinter as tk
from tkinter import messagebox
import mysql.connector
import adminReview

def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

def create_discussion_board_gui(root, is_admin=False):
    root.destroy()
    
    discussion_board_window = tk.Tk()
    discussion_board_window.title("Discussion Boards")
    discussion_board_window.geometry("600x400")  # Adjust default size here
    
    label = tk.Label(discussion_board_window, text="Discussion Boards", font=("Arial", 16))
    label.pack(pady=10)

    listbox = tk.Listbox(discussion_board_window)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_boards():
        listbox.delete(0, tk.END)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT topic FROM board")
            boards = cursor.fetchall()
            cursor.close()
            connection.close()
            
            for board in boards:
                listbox.insert(tk.END, board[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def logout():
        discussion_board_window.destroy()
        import main
        main.main()

    button_logout = tk.Button(discussion_board_window, text="Logout", command=logout, width=20, height=2)
    button_logout.pack(pady=10)

    def open_create_board_window():
        create_board_window = tk.Toplevel(discussion_board_window)
        create_board_window.title("Create Board")

        topic_label = tk.Label(create_board_window, text="Board Topic:")
        topic_label.pack(pady=5)

        topic_entry = tk.Entry(create_board_window)
        topic_entry.pack(pady=5)

        post_label = tk.Label(create_board_window, text="Enter your post:")
        post_label.pack(pady=5)

        post_text = tk.Text(create_board_window, height=10, width=50)
        post_text.pack(pady=10)

        submit_button = tk.Button(create_board_window, text="Submit", command=lambda: submit_board_and_post(topic_entry.get(), post_text.get("1.0", tk.END), create_board_window))
        submit_button.pack(pady=10)

    def submit_board_and_post(topic, post_content, window):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO board (topic) VALUES (%s)", (topic,))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            board_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO main (message, boardID) VALUES (%s, %s)", (post_content, board_id))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Board and post submitted successfully!")
            load_boards()
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    create_board_button = tk.Button(discussion_board_window, text="Create Board", command=open_create_board_window, width=20, height=2)
    create_board_button.pack(pady=10)

    if is_admin:
        review_button = tk.Button(discussion_board_window, text="Review Admin Requests", command=adminReview.open_admin_review_gui, width=20, height=2)
        review_button.pack(pady=10)

    load_boards()
    discussion_board_window.mainloop()
