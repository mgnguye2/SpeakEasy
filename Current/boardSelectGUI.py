import tkinter as tk  # For GUI components
from tkinter import messagebox  # For dialog boxes
import mysql.connector  # For database operations

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to create the board selection GUI
def create_board_select_gui(board_id):
    # Create a new top-level window for the board view
    board_select_window = tk.Toplevel()
    board_select_window.title("View Board")

    # Create and pack a listbox to display posts
    listbox = tk.Listbox(board_select_window)
    listbox.pack(padx=10, pady=10)

    # Function to load posts from the database into the listbox
    def load_posts():
        listbox.delete(0, tk.END)  # Clear existing posts
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT message FROM main WHERE boardID = %s", (board_id,))
            posts = cursor.fetchall()
            cursor.close()
            connection.close()

            # Insert posts into the listbox
            for post in posts:
                listbox.insert(tk.END, post[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    load_posts()  # Load posts when the window is created

    # Label and text widget for entering a new post
    post_label = tk.Label(board_select_window, text="Enter your post:")
    post_label.pack(pady=5)
    post_text = tk.Text(board_select_window, height=5, width=50)
    post_text.pack(pady=10)

    # Function to submit a new post to the database
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
            load_posts()  # Reload posts after submission
            post_text.delete("1.0", tk.END)  # Clear the text field
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    # Button to submit a new post
    submit_button = tk.Button(board_select_window, text="Submit", command=submit_post)
    submit_button.pack(pady=10)

# Main execution to create a sample board GUI window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    create_board_select_gui(1)  # Create the GUI for board ID 1
    root.mainloop()
