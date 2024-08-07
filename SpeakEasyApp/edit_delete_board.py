import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to refresh the listbox with posts from the 'board' table
def refresh_listbox(listbox, post_ids):
    listbox.delete(0, tk.END)  # Clear existing items in the listbox
    post_ids.clear()  # Clear existing post IDs in the list
    try:
        # Fetch posts from the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT boardID, topic FROM board")
        posts = cursor.fetchall()
        cursor.close()
        connection.close()

        # Add posts to the listbox and post_ids list
        for post in posts:
            post_id, post_content = post
            post_ids.append(post_id)
            listbox.insert(tk.END, post_content)
    except mysql.connector.Error as err:
        # Show error message if database operation fails
        messagebox.showerror("Error", f"Database Error: {err}")

# Function to open a GUI for editing a selected post
def open_edit_gui(post_id, post_content, listbox, post_ids):
    edit_window = tk.Toplevel()  # Create a new window for editing
    edit_window.title("Edit Post")

    tk.Label(edit_window, text="Edit Post").pack(pady=10)  # Label for the edit window

    # Text widget for editing post content
    content_text = tk.Text(edit_window, height=10, width=50)
    content_text.pack(pady=10)
    content_text.insert(tk.END, post_content)  # Insert existing post content

    # Function to save changes to the post
    def save_changes():
        new_content = content_text.get("1.0", tk.END).strip()  # Get new content from text widget
        if not new_content:
            messagebox.showerror("Error", "Board content cannot be empty.")  # Show error if content is empty
            return

        try:
            # Update the post content in the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE board SET topic = %s WHERE boardID = %s", (new_content, post_id))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Board updated successfully!")  # Show success message
            edit_window.destroy()  # Close the edit window
            refresh_listbox(listbox, post_ids)  # Refresh the listbox with updated posts
        except mysql.connector.Error as err:
            # Show error message if database operation fails
            messagebox.showerror("Error", f"Database Error: {err}")

    # Button to save changes
    tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

# Function to open a GUI for confirming the deletion of a selected post
def open_delete_gui(post_id, post_content, listbox, post_ids):
    delete_window = tk.Toplevel()  # Create a new window for deletion confirmation
    delete_window.title("Delete Post")

    # Label asking for deletion confirmation
    tk.Label(delete_window, text="Are you sure you want to delete this post?").pack(pady=10)

    # Function to confirm and perform the deletion
    def confirm_delete():
        try:
            # Delete the post from the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM board WHERE boardID = %s", (post_id,))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Post deleted successfully!")  # Show success message
            delete_window.destroy()  # Close the delete window
            refresh_listbox(listbox, post_ids)  # Refresh the listbox with updated posts
        except mysql.connector.Error as err:
            # Show error message if database operation fails
            messagebox.showerror("Error", f"Database Error: {err}")

    # Button to confirm deletion
    tk.Button(delete_window, text="Confirm Delete", command=confirm_delete).pack(pady=10)