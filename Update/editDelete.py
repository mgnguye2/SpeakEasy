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


def open_edit_gui(post_id, post_content, listbox, post_ids):
   if post_id is None:
       return


   edit_window = tk.Toplevel()
   edit_window.title("Edit Post")


   tk.Label(edit_window, text="Edit Post").pack(pady=10)


   topic_label = tk.Label(edit_window, text="Edit Topic:")
   topic_label.pack(pady=5)
   topic_text = tk.Entry(edit_window)
   topic_text.pack(pady=5)
  
   content_label = tk.Label(edit_window, text="Edit Message:")
   content_label.pack(pady=5)
   content_text = tk.Text(edit_window, height=10, width=50)
   content_text.pack(pady=10)
   content_text.insert(tk.END, post_content)


   def save_changes():
       new_topic = topic_text.get().strip()
       new_content = content_text.get("1.0", tk.END).strip()
       if not new_topic or not new_content:
           messagebox.showerror("Error", "Topic and Message content cannot be empty.")
           return


       try:
           connection = get_db_connection()
           cursor = connection.cursor()


           # Get boardID using messageID
           cursor.execute("SELECT boardID FROM main WHERE messageID = %s", (post_id,))
           board_id = cursor.fetchone()[0]


           # Update topic in board table
           cursor.execute("UPDATE board SET topic = %s WHERE boardID = %s", (new_topic, board_id))
          
           # Update message in main table
           cursor.execute("UPDATE main SET message = %s WHERE messageID = %s", (new_content, post_id))
          
           connection.commit()
           cursor.close()
           connection.close()
           messagebox.showinfo("Success", "Post updated successfully!")
           edit_window.destroy()
           refresh_listbox(listbox, post_ids)
       except mysql.connector.Error as err:
           messagebox.showerror("Error", f"Database Error: {err}")


   tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)


def open_delete_gui(post_id, post_content, listbox, post_ids):
   if post_id is None:
       return


   delete_window = tk.Toplevel()
   delete_window.title("Delete Post")


   tk.Label(delete_window, text="Are you sure you want to delete this post?").pack(pady=10)


   def confirm_delete():
       try:
           connection = get_db_connection()
           cursor = connection.cursor()


           # Get boardID using messageID
           cursor.execute("SELECT boardID FROM main WHERE messageID = %s", (post_id,))
           board_id = cursor.fetchone()[0]


           # Delete from main table
           cursor.execute("DELETE FROM main WHERE messageID = %s", (post_id,))
           connection.commit()


           # Check if there are any other rows with the same boardID in the main table
           cursor.execute("SELECT COUNT(*) FROM main WHERE boardID = %s", (board_id,))
           count = cursor.fetchone()[0]


           # If no other rows exist with the same boardID, delete from board table
           if count == 0:
               cursor.execute("DELETE FROM board WHERE boardID = %s", (board_id,))
               connection.commit()


           cursor.close()
           connection.close()
           messagebox.showinfo("Success", "Post deleted successfully!")
           delete_window.destroy()
           refresh_listbox(listbox, post_ids)
       except mysql.connector.Error as err:
           messagebox.showerror("Error", f"Database Error: {err}")


   tk.Button(delete_window, text="Confirm Delete", command=confirm_delete).pack(pady=10)


def refresh_listbox(listbox, post_ids):
   listbox.delete(0, tk.END)  # Clear existing items
   post_ids.clear()  # Clear existing post IDs
   try:
       connection = get_db_connection()
       cursor = connection.cursor()
       cursor.execute("SELECT messageID, message FROM main")
       posts = cursor.fetchall()
       cursor.close()
       connection.close()


       for post in posts:
           post_id, post_content = post
           post_ids.append(post_id)
           listbox.insert(tk.END, post_content)
   except mysql.connector.Error as err:
       messagebox.showerror("Error", f"Database Error: {err}")
