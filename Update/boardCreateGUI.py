import tkinter as tk
from tkinter import messagebox
import mysql.connector
import loginGUI

def create_board_window():
    board_window = tk.Toplevel()
    board_window.title("Create Board")

    # Label and entry for board topic
    topic_label = tk.Label(board_window, text="Board Topic:")
    topic_label.pack(pady=5)

    topic_entry = tk.Entry(board_window)
    topic_entry.pack(pady=5)

    # Label and textbox for the post content
    post_label = tk.Label(board_window, text="Enter your post:")
    post_label.pack(pady=5)

    post_text = tk.Text(board_window, height=10, width=50)
    post_text.pack(pady=10)

    # Submit button
    submit_button = tk.Button(board_window, text="Submit", command=lambda: submit_board_and_post(topic_entry.get(), post_text.get("1.0", tk.END)))
    submit_button.pack(pady=10)

def submit_board_and_post(topic, post_content):
    # Connect to the database
    try:
        connection = mysql.connector.connect(
            host='107.180.1.16',
            user='summer2024team4',
            password='summer2024team4',
            database='summer2024team4'
        )
        cursor = connection.cursor()
        
        # Insert the new board topic into the board table
        cursor.execute("INSERT INTO board (boardID) VALUES (%s)", (topic,))
        connection.commit()
        
        # Retrieve the boardID of the newly inserted board
        cursor.execute("SELECT LAST_INSERT_ID()")
        board_id = cursor.fetchone()[0]
        
        # Insert the post into the main table
        cursor.execute("INSERT INTO main (messageID, boardID) VALUES (%s, %s)", (post_content, board_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Board and post submitted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")


def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )


def submit_board_and_post(topic, post_content, load_boards_callback, window):
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
        load_boards_callback()  # Reload boards after submission
        window.destroy()  # Close the create board window
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")