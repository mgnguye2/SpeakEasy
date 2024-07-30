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

def open_admin_review_gui():
    review_window = tk.Toplevel()
    review_window.title("Admin Review")
    review_window.geometry("500x400")  # Adjust default size here

    listbox = tk.Listbox(review_window)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_pending_requests():
        listbox.delete(0, tk.END)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT memberID FROM member WHERE admin_request = 1")
            requests = cursor.fetchall()
            cursor.close()
            connection.close()
            
            for req in requests:
                listbox.insert(tk.END, f"MemberID: {req[0]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

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
            load_pending_requests()
            messagebox.showinfo("Success", "Request reviewed successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def approve_selected():
        review_request("approve")

    def deny_selected():
        review_request("deny")

    approve_button = tk.Button(review_window, text="Approve", command=approve_selected, width=15, height=2)
    approve_button.pack(side=tk.LEFT, padx=10, pady=10)

    deny_button = tk.Button(review_window, text="Deny", command=deny_selected, width=15, height=2)
    deny_button.pack(side=tk.RIGHT, padx=10, pady=10)

    load_pending_requests()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_admin_review_gui()
    root.mainloop()
