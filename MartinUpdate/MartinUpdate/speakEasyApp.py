import tkinter as tk
from tkinter import messagebox
import createAccountGUI
import loginGUI
import adminReview
import editDelete
import boardCreateGUI
import mysql.connector

class SpeakEasyApp(tk.Tk):
    def __init__(self, is_admin=False, member_id=None):
        super().__init__()
        self.title("SpeakEasy Discussions")
        self.geometry("1000x600")
        self.is_admin = is_admin
        self.current_member_id = member_id

        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_left_sidebar()
        self.create_right_sidebar()
        self.create_content_area()

    def create_left_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.sections = {
            "General Discussion": ["Company News", "General Inquiries", "Miscellaneous Topics"],
            "Team Updates": ["Project Progress Reports", "Team Achievements", "Upcoming Milestones"],
            "Q&A and Troubleshooting": ["Technical Support Questions", "Process Clarifications", "Help with Tools and Software"],
            "Training and Development": ["Upcoming Training Sessions", "Learning Resources", "Career Advice"],
            "HR Announcements": ["Policy Updates", "Benefits Information", "Important Dates"],
            "Company Culture and Events": ["Company Event Announcements", "Team-Building Activities", "Cultural Initiatives"],
            "Mount Olympus": ["Shout-Outs for Exceptional Work", "Celebrating Achievements", "Peer Recognition"],
            "Health and Wellness": ["Wellness Tips", "Mental Health Resources", "Fitness Challenges"],
            "Innovation Lab": ["Proposals for New Projects", "Innovative Solutions to Problems", "Creative Ideas for the Workplace"],
            "Project Hub": ["Project Status Updates", "Collaborative Brainstorming Sessions", "Detailed Project Plans", "Requests for Project Assistance"]
        }

        self.buttons = {}
        for section in self.sections:
            btn = tk.Button(self.sidebar, text=section, command=lambda sec=section: self.show_section(sec))
            btn.pack(fill=tk.X)
            self.buttons[section] = btn

    def create_right_sidebar(self):
        self.right_sidebar = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.right_sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.add_admin_buttons()

    def add_admin_buttons(self):
        # Display the User ID
        user_id_label = tk.Label(self.right_sidebar, text=f"User ID: {self.current_member_id}", bg="lightgray", anchor='w')
        user_id_label.pack(fill=tk.X, pady=(10, 10))

        btn_create_board = tk.Button(self.right_sidebar, text="Create Board", command=self.create_board)
        btn_create_board.pack(fill=tk.X)

        btn_edit = tk.Button(self.right_sidebar, text="Edit", command=self.edit_post)
        btn_edit.pack(fill=tk.X)

        btn_delete = tk.Button(self.right_sidebar, text="Delete", command=self.delete_post)
        btn_delete.pack(fill=tk.X)

        if self.is_admin:
            btn_review_admin = tk.Button(self.right_sidebar, text="Review Admin Requests", command=self.review_admin_requests)
            btn_review_admin.pack(fill=tk.X)
        
        # Add a spacer to push the logout button to the bottom
        spacer = tk.Frame(self.right_sidebar, height=50, bg="lightgray")
        spacer.pack(fill=tk.BOTH, expand=True)

        btn_logout = tk.Button(self.right_sidebar, text="Logout", command=self.logout)
        btn_logout.pack(side=tk.BOTTOM, fill=tk.X)

    def create_content_area(self):
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_section(self, section):
        self.clear_content_area()
        label = tk.Label(self.content_area, text=section, font=("Arial", 18))
        label.pack(pady=10)

        for subcategory in self.sections[section]:
            sub_label = tk.Label(self.content_area, text=subcategory, font=("Arial", 14))
            sub_label.pack(anchor="w", padx=20, pady=5)

            thread_button = tk.Button(self.content_area, text=f"Add Thread in {subcategory}", command=lambda sub=subcategory: self.add_thread(sub))
            thread_button.pack(anchor="w", padx=40, pady=2)

    def add_thread(self, subcategory):
        new_thread_window = tk.Toplevel(self)
        new_thread_window.title(f"New Thread in {subcategory}")
        new_thread_window.geometry("400x300")

        tk.Label(new_thread_window, text="Thread Title:").pack(pady=10)
        title_entry = tk.Entry(new_thread_window)
        title_entry.pack(pady=5)

        tk.Label(new_thread_window, text="Thread Content:").pack(pady=10)
        content_text = tk.Text(new_thread_window, height=10, width=40)
        content_text.pack(pady=5)

        def save_thread():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if title and content:
                self.save_thread_to_db(title, content, subcategory)
                tk.messagebox.showinfo("Thread Created", f"Thread '{title}' created in {subcategory}")
                new_thread_window.destroy()
            else:
                tk.messagebox.showwarning("Input Error", "Please fill in both title and content.")

        save_button = tk.Button(new_thread_window, text="Save Thread", command=save_thread)
        save_button.pack(pady=20)

    def save_thread_to_db(self, title, content, subcategory):
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO main (memberID, boardID, vote, active, message) VALUES (%s, %s, 1, 1, %s)",
                           (self.current_member_id, self.get_board_id(subcategory), content))
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def get_board_id(self, subcategory):
        board_mapping = {
            "General Discussion": 1,
            "Team Updates": 2,
            "Q&A and Troubleshooting": 3,
            "Training and Development": 4,
            "HR Announcements": 5,
            "Company Culture and Events": 6,
            "Mount Olympus": 7,
            "Health and Wellness": 8,
            "Innovation Lab": 9,
            "Project Hub": 10,
        }
        return board_mapping.get(subcategory, 1)  # Default to 1 if not found

    def logout(self):
        self.clear_content_area()
        label = tk.Label(self.content_area, text="You have been logged out.", font=("Arial", 18))
        label.pack(pady=10)
        self.after(2000, self.destroy)

    def create_board(self):
        self.clear_content_area()
        self.show_create_board_gui()

    def show_create_board_gui(self):
        category_label = tk.Label(self.content_area, text="Select Board Category:")
        category_label.pack(pady=5)

        board_mapping = {
        "General Discussion": 1,
        "Team Updates": 2,
        "Q&A and Troubleshooting": 3,
        "Training and Development": 4,
        "HR Announcements": 5,
        "Company Culture and Events": 6,
        "Mount Olympus": 7,
        "Health and Wellness": 8,
        "Innovation Lab": 9,
        "Project Hub": 10,
        }

        categories = list(board_mapping.keys())
        selected_category = tk.StringVar(value=categories[0])
        category_dropdown = tk.OptionMenu(self.content_area, selected_category, *categories)
        category_dropdown.pack(pady=5)

        topic_label = tk.Label(self.content_area, text="Enter Topic:")
        topic_label.pack(pady=5)

        topic_entry = tk.Entry(self.content_area)
        topic_entry.pack(pady=5)

        post_label = tk.Label(self.content_area, text="Enter your starting post:")
        post_label.pack(pady=5)

        post_text = tk.Text(self.content_area, height=10, width=50)
        post_text.pack(pady=10)

        submit_button = tk.Button(
        self.content_area,
        text="Submit",
        command=lambda: self.submit_board_and_post(
            board_mapping[selected_category.get()],  # Correctly get the integer board ID
            topic_entry.get(),
            post_text.get("1.0", tk.END)
            )
        )
        submit_button.pack(pady=10)

    def submit_board_and_post(self, category, topic, post_content):
        try:
            connection = boardCreateGUI.get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO board (boardID, active, messageCount, voteCount, topic) VALUES (%s, 1, 0, 0, %s)",
                (category, topic))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            topic_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO main (message, boardID, vote, active, memberID, boardSubID) VALUES (%s, %s, 0, 1, %s, %s)",
                (post_content, category, self.current_member_id, topic_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Board and post submitted successfully!")
            self.show_section("Project Hub")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

    def edit_post(self):
        self.clear_content_area()
        self.show_edit_post_gui()

    def show_edit_post_gui(self):
        listbox = tk.Listbox(self.content_area, width=100, height=20)
        listbox.pack(padx=10, pady=10)
        post_ids = []
        editDelete.refresh_listbox(listbox, post_ids)

        def on_edit():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a post to edit.")
                return
            post_id = post_ids[selected_index[0]]
            post_content = listbox.get(selected_index)
            editDelete.open_edit_gui(post_id, post_content, listbox, post_ids)

        edit_button = tk.Button(self.content_area, text="Edit", command=on_edit)
        edit_button.pack(pady=10)

    def delete_post(self):
        self.clear_content_area()
        self.show_delete_post_gui()

    def show_delete_post_gui(self):
        listbox = tk.Listbox(self.content_area, width=100, height=20)
        listbox.pack(padx=10, pady=10)
        post_ids = []
        editDelete.refresh_listbox(listbox, post_ids)

        def on_delete():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a post to delete.")
                return
            post_id = post_ids[selected_index[0]]
            post_content = listbox.get(selected_index)
            editDelete.open_delete_gui(post_id, post_content, listbox, post_ids)

        delete_button = tk.Button(self.content_area, text="Delete", command=on_delete)
        delete_button.pack(pady=10)

    def review_admin_requests(self):
        self.clear_content_area()
        self.show_admin_review_gui()

    def show_admin_review_gui(self):
        listbox = tk.Listbox(self.content_area)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        def load_pending_requests():
            listbox.delete(0, tk.END)  # Clear current items
            try:
                connection = adminReview.get_db_connection()
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
                connection = adminReview.get_db_connection()
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
                messagebox.showerror("Database Error", f"Error: {err}")

        approve_button = tk.Button(self.content_area, text="Approve", command=lambda: review_request("approve"), width=15, height=2)
        approve_button.pack(side=tk.LEFT, padx=10, pady=10)

        deny_button = tk.Button(self.content_area, text="Deny", command=lambda: review_request("deny"), width=15, height=2)
        deny_button.pack(side=tk.RIGHT, padx=10, pady=10)

        load_pending_requests()

    def clear_right_sidebar(self):
        for widget in self.right_sidebar.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SpeakEasyApp(is_admin=True, member_id=1)  # Change to `False` and provide member_id if not admin
    app.mainloop()
