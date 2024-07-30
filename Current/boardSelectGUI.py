import tkinter as tk
from tkinter import messagebox
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

def create_board_select_gui(board_id):
    board_select_window = tk.Toplevel()
    board_select_window.title("View Board")

    listbox = tk.Listbox(board_select_window)
    listbox.pack(padx=10, pady=10)

    def load_posts():
        listbox.delete(0, tk.END)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT message FROM main WHERE boardID = %s", (board_id,))
            posts = cursor.fetchall()
            cursor.close()
            connection.close()

            for post in posts:
                listbox.insert(tk.END, post[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    load_posts()

    post_label = tk.Label(board_select_window, text="Enter your post:")
    post_label.pack(pady=5)

    post_text = tk.Text(board_select_window, height=5, width=50)
    post_text.pack(pady=10)

    def submit_post():
        post_content = post_text.get("1.0", tk.END).strip()
        if not post_content:
            messagebox.showwarning("Warning", "Post content cannot be empty.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO main (message, boardID) VALUES (%s, %s)", (post_content, board_id))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Post submitted successfully!")
            load_posts()
            post_text.delete("1.0", tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    submit_button = tk.Button(board_select_window, text="Submit", command=submit_post)
    submit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_board_select_gui(1)  # Example boardID to test the GUI
    root.mainloop()
