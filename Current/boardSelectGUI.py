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

    button_logout = tk.Button(discussion_board_window, text="Logout", command=logout)
    button_logout.pack(pady=10)

    def open_create_board_window():
        create_board_window = tk.Toplevel(discussion_board_window)
        create_board_window.title("Create Board")

        # Label and entry for board topic
        topic_label = tk.Label(create_board_window, text="Board Topic:")
        topic_label.pack(pady=5)

        topic_entry = tk.Entry(create_board_window)
        topic_entry.pack(pady=5)

        # Label and textbox for the post content
        post_label = tk.Label(create_board_window, text="Enter your post:")
        post_label.pack(pady=5)

        post_text = tk.Text(create_board_window, height=10, width=50)
        post_text.pack(pady=10)

        # Submit button
        submit_button = tk.Button(create_board_window, text="Submit", command=lambda: submit_board_and_post(topic_entry.get(), post_text.get("1.0", tk.END), create_board_window))
        submit_button.pack(pady=10)

    def submit_board_and_post(topic, post_content, window):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Insert the new board topic into the board table
            print(f"Inserting board topic: {topic}")
            cursor.execute("INSERT INTO board (topic) VALUES (%s)", (topic,))
            connection.commit()
            
            # Retrieve the boardID of the newly inserted board
            cursor.execute("SELECT LAST_INSERT_ID()")
            board_id = cursor.fetchone()[0]
            print(f"New boardID: {board_id}")
            
            # Insert the post into the main table
            print(f"Inserting post: {post_content} for boardID: {board_id}")
            cursor.execute("INSERT INTO main (message, boardID) VALUES (%s, %s)", (post_content, board_id))
            connection.commit()
            
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Board and post submitted successfully!")
            load_boards()  # Refresh the listbox to show the new board
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
            print(f"Database Error: {err}")

    # Add the "Create Board" button
    create_board_button = tk.Button(discussion_board_window, text="Create Board", command=open_create_board_window)
    create_board_button.pack(pady=10)

    load_boards()  # Load boards when the window is created

    discussion_board_window.mainloop()