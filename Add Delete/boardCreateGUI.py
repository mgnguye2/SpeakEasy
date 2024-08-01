import tkinter as tk
from tkinter import messagebox
import mysql.connector
import loginGUI


def create_board_window(load_boards_update):
    board_window = tk.Toplevel()
    board_window.title("Create Board")

    # Label and entry for board topic
    topic_label = tk.Label(board_window, text="Board Topic:")
    topic_label.pack(pady=5)

    topic_entry = tk.Entry(board_window)
    topic_entry.pack(pady=5)

    # Label and textbox for the post content
    post_label = tk.Label(board_window, text="Enter your message:")
    post_label.pack(pady=5)

    post_text = tk.Text(board_window, height=10, width=50)
    post_text.pack(pady=10)

    # Submit button
    submit_button = tk.Button(board_window, text="Submit", command=lambda: submit_board_and_post(topic_entry.get(), post_text.get("1.0", tk.END), load_boards_update, board_window))
    submit_button.pack(pady=10)



def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )


def submit_board_and_post(topic, post_content, load_boards_update, window):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO board (active, topic) VALUES (1, %s)", (topic,))
        connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        board_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO main (message, boardID, vote, active, memberID) VALUES (%s, %s, 0, 1, %s)",
            (post_content, board_id, loginGUI.current_member_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Board and post submitted successfully!")
        load_boards_update()  # Reload boards after submission
        window.destroy()  # Close the create board window
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")