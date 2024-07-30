import tkinter as tk  # For GUI components
from tkinter import messagebox  # For displaying messages
import mysql.connector  # For database interactions

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="107.180.1.16",
        user="summer2024team4",
        password="summer2024team4",
        database="summer2024team4"
    )

# Function to create and manage the admin review GUI
def open_admin_review_gui():
    review_window = tk.Toplevel()  # Create a new top-level window
    review_window.title("Admin Review")  # Set the window title
    review_window.geometry("500x400")  # Set window size

    # Listbox to display pending admin requests
    listbox = tk.Listbox(review_window)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Function to load and display pending admin requests
    def load_pending_requests():
        listbox.delete(0, tk.END)  # Clear current items
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT memberID FROM member WHERE admin_request = 1")
            requests = cursor.fetchall()
            cursor.close()
            connection.close()
            
            # Add requests to the listbox
            for req in requests:
                listbox.insert(tk.END, f"MemberID: {req[0]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    # Function to review a selected admin request (approve or deny)
    def review_request(action):
        selected = listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Warning", "No request selected")
            return

        member_id = selected.split(": ")[1]
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            if action == "approve":
                cursor.execute("UPDATE member SET admin = 1, admin_request = 0 WHERE memberID = %s", (member_id,))
            else:
                cursor.execute("UPDATE member SET admin_request = 0 WHERE memberID = %s", (member_id,))
            connection.commit()
            cursor.close()
            connection.close()
            load_pending_requests()  # Refresh the list of requests
            messagebox.showinfo("Success", "Request reviewed successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    # Functions to handle approval and denial of requests
    def approve_selected():
        review_request("approve")

    def deny_selected():
        review_request("deny")

    # Buttons to approve or deny selected requests
    approve_button = tk.Button(review_window, text="Approve", command=approve_selected, width=15, height=2)
    approve_button.pack(side=tk.LEFT, padx=10, pady=10)

    deny_button = tk.Button(review_window, text="Deny", command=deny_selected, width=15, height=2)
    deny_button.pack(side=tk.RIGHT, padx=10, pady=10)

    load_pending_requests()  # Load requests when the window opens

# Main function to run the admin review GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    open_admin_review_gui()  # Open the admin review window
    root.mainloop()  # Start the GUI event loop
