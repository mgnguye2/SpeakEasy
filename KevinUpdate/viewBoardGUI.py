import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to create the board details GUI
def create_board_details_gui(board_topic):
    board_details_window = tk.Tk()
    board_details_window.title(f"Board: {board_topic}")

    label = tk.Label(board_details_window, text=f"Posts for {board_topic}")
    label.pack(pady=10)

    listbox = tk.Listbox(board_details_window, width=100, height=20)
    listbox.pack(padx=10, pady=10)

    def load_posts():
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT main.message
                FROM board
                INNER JOIN main ON board.boardID = main.boardID
                WHERE board.topic = %s
            """, (board_topic,))
            posts = cursor.fetchall()
            cursor.close()
            connection.close()

            for post in posts:
                listbox.insert(tk.END, post[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    load_posts()

    board_details_window.mainloop()

if __name__ == "__main__":
    # This is just an example of how you might test this script standalone.
    create_board_details_gui("Example Topic")