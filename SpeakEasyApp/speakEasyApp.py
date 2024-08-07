import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import main
import edit_delete_board
import admin_review

class SpeakEasyApp(tk.Tk):
    def __init__(self, is_admin=False, member_id=None):
        """
        Initialize the SpeakEasyApp with an optional admin flag and member ID.
        Set up the main window and call the function to create the main frame.
        """
        super().__init__()
        self.title("SpeakEasy Discussions")
        self.geometry("1200x800")
        self.is_admin = is_admin
        self.current_member_id = member_id
        self.vote_buttons = {}
        self.report_buttons = {}
        self.reply_buttons = {}

        self.kudo_points = self.get_kudo_points()
        self.create_main_frame()

    def get_kudo_points(self):
        """
        Retrieve the current kudo points for the logged-in member from the database.
        Returns 0 if an error occurs or no points are found.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )

            cursor = connection.cursor()

            cursor.execute("""
                SELECT votes
                FROM member
                WHERE memberID = %s
            """, (self.current_member_id,))

            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result:
                return result[0]
            else:
                return 0
            
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")
            return 0

    def create_main_frame(self):
        """
        Create the main frame of the application, including the sidebars and content area.
        """
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_left_sidebar()
        self.create_right_sidebar()
        self.create_content_area()

    def update_kudo_points(self):
        """
        Update the kudo points displayed on the UI by fetching the latest points from the database.
        """
        new_kudo_points = self.get_kudo_points()
        self.kudo_label.config(text=f"Kudo Points(KP): {new_kudo_points}")

    def create_left_sidebar(self):
        """
        Create the left sidebar with buttons for different discussion sections and an image logo.
        """
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

        # Load and resize the image
        image_path = "SpeakEasy1.png"  # Ensure this path is correct
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Add the image to the sidebar
        image_label = tk.Label(self.sidebar, image=photo, bg="lightgray")
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=20)

    def create_right_sidebar(self):
        """
        Create the right sidebar with admin options, logout button, and display of the user's ID and kudo points.
        """
        self.right_sidebar = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.right_sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.add_admin_buttons()

    def add_admin_buttons(self):
        """
        Add buttons for admin functionalities like creating boards, editing posts, managing members, etc.
        Also, display user ID and kudo points.
        """
        # Display the User ID
        user_id_label = tk.Label(self.right_sidebar, text=f"User ID: {self.current_member_id}", bg="lightgray", anchor='w')
        user_id_label.pack(fill=tk.X, pady=(10, 10))

        # Display the vote count 
        self.kudo_label = tk.Label(self.right_sidebar, text=f"Kudo Points(KP): {self.kudo_points}", bg="lightgray", anchor='w')
        self.kudo_label.pack(fill=tk.X, pady=(10, 10))

        if self.is_admin:
            btn_create_board = tk.Button(self.right_sidebar, text="Create Board", command=self.create_board)
            btn_create_board.pack(fill=tk.X)

            btn_edit = tk.Button(self.right_sidebar, text="Edit", command=self.edit_post)
            btn_edit.pack(fill=tk.X)

            btn_delete = tk.Button(self.right_sidebar, text="Delete", command=self.delete_post)
            btn_delete.pack(fill=tk.X)

            btn_review_admin = tk.Button(self.right_sidebar, text="Review Admin Requests", command=self.review_admin_requests)
            btn_review_admin.pack(fill=tk.X)

            btn_review_reported = tk.Button(self.right_sidebar, text="Review Reported Posts", command=self.review_reported_posts)
            btn_review_reported.pack(fill=tk.X)

            btn_manage_members = tk.Button(self.right_sidebar, text="Manage Members", command=self.manage_members)
            btn_manage_members.pack(fill=tk.X)
        
            # Add a spacer to push the logout button to the bottom
            spacer = tk.Frame(self.right_sidebar, height=50, bg="lightgray")
            spacer.pack(fill=tk.BOTH, expand=True)

            btn_logout = tk.Button(self.right_sidebar, text="Logout", command=self.logout)
            btn_logout.pack(side=tk.BOTTOM, fill=tk.X)

        else:
            # Add a spacer to push the logout button to the bottom
            spacer = tk.Frame(self.right_sidebar, height=50, bg="lightgray")
            spacer.pack(fill=tk.BOTH, expand=True)

            btn_logout = tk.Button(self.right_sidebar, text="Logout", command=self.logout)
            btn_logout.pack(side=tk.BOTTOM, fill=tk.X)

    def create_content_area(self):
        """
        Create the main content area where discussions and other content will be displayed.
        """
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear_content_area(self):
        """
        Clear all widgets from the content area.
        """
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_section(self, section):
        """
        Display the topics under the selected section and fetch related data from the database.
        """
        self.clear_content_area()
        label = tk.Label(self.content_area, text=section, font=("Arial", 18))
        label.pack(pady=10)

        # Retrieve topics based on the selected section
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Get the boardID based on the section
            board_id = self.get_board_id(section)

            # Fetch topics (subcategories) from the database
            cursor.execute("""
                SELECT topic 
                FROM board 
                WHERE boardID = %s
            """, (board_id,))
            
            topics = cursor.fetchall()
            cursor.close()
            connection.close()

            # Create buttons for each topic
            for topic in topics:
                topic_name = topic[0]
                topic_button = tk.Button(self.content_area, text=topic_name, command=lambda t=topic_name: self.view_discussion_board(t))
                topic_button.pack(anchor="w", padx=20, pady=5)
                
        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def add_thread(self, subcategory):
        """
        Open a window to create a new thread in the specified subcategory.
        """
        new_thread_window = tk.Toplevel(self)
        new_thread_window.title(f"New Thread in {subcategory}")
        new_thread_window.geometry("700x500")

        tk.Label(new_thread_window, text="Thread Title:").pack(pady=10)
        title_entry = tk.Entry(new_thread_window, width=80)
        title_entry.pack(pady=5)

        tk.Label(new_thread_window, text="Thread Content:").pack(pady=10)
        content_text = tk.Text(new_thread_window, height=15, width=70)
        content_text.pack(pady=5)

        def save_thread():
            """
            Save the new thread to the database.
            """
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
        """
        Save the new thread to the database under the specified subcategory.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Get the boardSubID based on the subcategory (topic)
            cursor.execute("""
                SELECT subID
                FROM board
                WHERE topic = %s
            """, (subcategory,))
            
            result = cursor.fetchone()
            if not result:
                tk.messagebox.showerror("Error", "The specified topic does not exist.")
                return

            board_sub_id = result[0]

            # Insert the new thread into the main table, including msgTitle
            cursor.execute("""
                INSERT INTO main (memberID, boardID, vote, active, message, boardSubID, msgTitle)
                VALUES (%s, %s, 0, 1, %s, %s, %s)
            """, (self.current_member_id, self.get_board_id(subcategory), content, board_sub_id, title))
            
            connection.commit()
            cursor.close()
            connection.close()

            # Refresh the discussion board to show the new thread
            self.view_discussion_board(subcategory)

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def get_board_id(self, section):
        """
        Get the board ID associated with a specific section.
        """
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
        return board_mapping.get(section, 1)  # Default to 1 if not found

    def logout(self):
        """
        Log the user out by clearing the content area and showing a logout message.
        """
        self.clear_content_area()
        label = tk.Label(self.content_area, text="You have been logged out.", font=("Arial", 18))
        label.pack(pady=10)
        self.after(2000, self.redirect_to_login)

    def redirect_to_login(self):
        """
        Redirect to the login screen by destroying the current session and reopening the login.
        """
        self.destroy()
        main.main()

    def create_board(self):
        """
        Open the UI for creating a new discussion board.
        """
        self.clear_content_area()
        self.show_create_board_gui()

    def show_create_board_gui(self):
        """
        Display the UI for creating a new board, including selecting a category and providing a topic and initial post.
        """
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
        """
        Submit the newly created board and its initial post to the database.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
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
        """
        Open the UI for editing a post.
        """
        self.clear_content_area()
        self.show_edit_post_gui()

    def show_edit_post_gui(self):
        """
        Display the UI for selecting and editing a post.
        """
        listbox = tk.Listbox(self.content_area, width=100, height=20)
        listbox.pack(padx=10, pady=10)
        post_ids = []
        edit_delete_board.refresh_listbox(listbox, post_ids)

        def on_edit():
            """
            Open the edit UI for the selected post.
            """
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a post to edit.")
                return
            post_id = post_ids[selected_index[0]]
            post_content = listbox.get(selected_index)
            edit_delete_board.open_edit_gui(post_id, post_content, listbox, post_ids)

        edit_button = tk.Button(self.content_area, text="Edit", command=on_edit)
        edit_button.pack(pady=10)

    def delete_post(self):
        """
        Open the UI for deleting a post.
        """
        self.clear_content_area()
        self.show_delete_post_gui()

    def show_delete_post_gui(self):
        """
        Display the UI for selecting and deleting a post.
        """
        listbox = tk.Listbox(self.content_area, width=100, height=20)
        listbox.pack(padx=10, pady=10)
        post_ids = []
        edit_delete_board.refresh_listbox(listbox, post_ids)

        def on_delete():
            """
            Delete the selected post.
            """
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a post to delete.")
                return
            post_id = post_ids[selected_index[0]]
            post_content = listbox.get(selected_index)
            edit_delete_board.open_delete_gui(post_id, post_content, listbox, post_ids)

        delete_button = tk.Button(self.content_area, text="Delete", command=on_delete)
        delete_button.pack(pady=10)

    def review_admin_requests(self):
        """
        Open the UI for reviewing admin requests.
        """
        self.clear_content_area()
        self.show_admin_review_gui()

    def show_admin_review_gui(self):
        """
        Display the UI for viewing and approving/denying admin requests.
        """
        listbox = tk.Listbox(self.content_area)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        def load_pending_requests():
            """
            Load and display pending admin requests.
            """
            listbox.delete(0, tk.END)  # Clear current items
            try:
                connection = admin_review.get_db_connection()
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
            """
            Approve or deny the selected admin request.
            """
            selected = listbox.get(tk.ACTIVE)
            if not selected:
                messagebox.showwarning("Warning", "No request selected")
                return

            member_id = selected.split(": ")[1]
            try:
                connection = admin_review.get_db_connection()
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
        """
        Clear all widgets from the right sidebar.
        """
        for widget in self.right_sidebar.winfo_children():
            widget.destroy()

    def view_discussion_board(self, topic):
        """
        Display the discussion board for the selected topic, including all related threads.
        """
        self.clear_content_area()
        self.current_topic = topic  # Store the current topic for use in other methods
        label = tk.Label(self.content_area, text=f"Discussion Board - {topic}", font=("Arial", 18))
        label.pack(pady=10)

        # Add a button to create a new thread in this subcategory
        create_thread_button = tk.Button(self.content_area, text="Create New Thread", command=lambda: self.add_thread(topic))
        create_thread_button.pack(pady=10)

        # Create a canvas for scrolling
        canvas = tk.Canvas(self.content_area)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        posts_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=posts_frame, anchor="nw")

        # Update the canvas scroll region when new widgets are added
        posts_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Enable scrolling with the mouse wheel
        def on_mouse_wheel(event):
            if event.num == 5 or event.delta == -120:  # Scroll down
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:   # Scroll up
                canvas.yview_scroll(-1, "units")

        # Bind mouse wheel event to the canvas
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows and MacOS with newer Tkinter versions
        canvas.bind_all("<Button-4>", on_mouse_wheel)    # Other systems (Linux)
        canvas.bind_all("<Button-5>", on_mouse_wheel)    # Other systems (Linux)

        # Initialize the vote, report, and reply buttons dictionary
        self.vote_buttons = {}
        self.report_buttons = {}
        self.reply_buttons = {}

        # Fetch and display posts from the database for the selected topic
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Get the boardSubID based on the topic
            cursor.execute("""
                SELECT b.subID
                FROM board b
                WHERE b.topic = %s
            """, (topic,))
            
            board_sub_id = cursor.fetchone()[0]

            # Fetch posts for the selected boardSubID, including memberID, msgTitle, message, vote, numberOfReplies, and report
            cursor.execute("""
                SELECT m.memberID, m.msgTitle, m.message, m.vote, m.messageID, m.report, m.numberOfReplies
                FROM main m
                WHERE m.boardSubID = %s AND m.active = 1
            """, (board_sub_id,))
            
            posts = cursor.fetchall()
            cursor.close()
            connection.close()

            # Display posts
            for post in posts:
                member_id, msg_title, message, vote, post_id, report, number_of_replies = post
                post_header = tk.Label(posts_frame, text=f"Member ID: {member_id}\n{msg_title}", font=("Arial", 10, "bold"), anchor="w", justify="left")
                post_header.pack(anchor="w", padx=20, pady=5)

                post_message = tk.Label(posts_frame, text=message, wraplength=700, justify="left")
                post_message.pack(anchor="w", padx=20, pady=5)

                # Frame for Vote, Report, and Reply buttons
                button_frame = tk.Frame(posts_frame)
                button_frame.pack(anchor="w", padx=20, pady=5)

                # Vote button
                vote_button = tk.Button(button_frame, text=f"Vote ({vote})", command=lambda pid=post_id: self.vote_post(pid))
                vote_button.pack(side=tk.LEFT)

                # Report button
                report_button = tk.Button(button_frame, text="Report", command=lambda pid=post_id: self.report_post(pid))
                report_button.pack(side=tk.LEFT)

                # Reply button with number of replies
                reply_button = tk.Button(button_frame, text=f"Reply ({number_of_replies})", command=lambda pid=post_id, msg=msg_title, mem_id=member_id, content=message: self.view_reply_board(pid, msg, mem_id, content))
                reply_button.pack(side=tk.LEFT)

                # Store the button references in the dictionaries
                self.vote_buttons[post_id] = vote_button
                self.report_buttons[post_id] = report_button
                self.reply_buttons[post_id] = reply_button

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def view_reply_board(self, original_post_id, original_msg_title, original_member_id, original_message):
        """
        Display the replies to a specific post along with options to add a new reply.
        """
        self.clear_content_area()

        # Frame for the replies and scrollable canvas
        reply_container = tk.Frame(self.content_area)
        reply_container.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        canvas = tk.Canvas(reply_container)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(reply_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas for replies
        self.replies_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.replies_frame, anchor="nw")

        # Update the canvas scroll region when new widgets are added
        self.replies_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Enable scrolling with the mouse wheel
        def on_mouse_wheel(event):
            if event.num == 5 or event.delta == -120:  # Scroll down
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:   # Scroll up
                canvas.yview_scroll(-1, "units")

        # Bind mouse wheel event to the canvas
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows and MacOS with newer Tkinter versions
        canvas.bind_all("<Button-4>", on_mouse_wheel)    # Other systems (Linux)
        canvas.bind_all("<Button-5>", on_mouse_wheel)    # Other systems (Linux)

        # Store the original post data
        self.original_post_id = original_post_id
        self.original_msg_title = original_msg_title
        self.original_member_id = original_member_id
        self.original_message = original_message

        # Fetch and display replies from the database
        self.load_replies()

        # Add a button to post a new reply
        post_reply_button = tk.Button(self.content_area, text="Post Reply", command=self.post_reply)
        post_reply_button.pack(pady=10)

        # Add a "Back" button to go back to the original board
        back_button = tk.Button(self.content_area, text="Back", command=lambda: self.view_discussion_board(self.current_topic))
        back_button.pack(pady=10)

    def save_reply_to_db(self, original_post_id, title, content):
        """
        Save a reply to the database, associated with the original post ID.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Insert the reply into the main table, including msgTitle and originalPostID
            cursor.execute("""
                INSERT INTO main (memberID, boardID, vote, active, message, originalPostID, msgTitle)
                VALUES (%s, %s, 0, 1, %s, %s, %s)
            """, (self.current_member_id, self.get_board_id(self.current_topic), content, original_post_id, title))

            # Increment the numberOfReplies for the original post
            cursor.execute("""
                UPDATE main
                SET numberOfReplies = numberOfReplies + 1
                WHERE messageID = %s
            """, (original_post_id,))

            connection.commit()
            cursor.close()
            connection.close()

            # Refresh the reply board to show the new reply
            self.view_reply_board(original_post_id, title, self.current_member_id, content)

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def vote_post(self, post_id):
        """
        Handle the voting process for a post, including checking if the user has already voted and updating the database.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Check if the user has already voted for this post
            cursor.execute("""
                SELECT COUNT(*)
                FROM votes
                WHERE userID = %s AND messageID = %s
            """, (self.current_member_id, post_id))
            
            already_voted = cursor.fetchone()[0]

            if already_voted:
                messagebox.showwarning("Already Voted", "You have already voted for this post.")
            else:
                # Record the vote in the votes table
                cursor.execute("""
                    INSERT INTO votes (userID, messageID)
                    VALUES (%s, %s)
                """, (self.current_member_id, post_id))
                
                # Update the vote count
                cursor.execute("""
                    UPDATE main
                    SET vote = vote + 1
                    WHERE messageID = %s
                """, (post_id,))

                cursor.execute("""
                    UPDATE member
                    SET votes = votes + 1
                    WHERE memberID = %s
                """, (self.current_member_id,))
                
                connection.commit()
                messagebox.showinfo("Vote Cast", "Your vote has been recorded.")

                # Fetch the new vote count and update the button text
                cursor.execute("""
                    SELECT vote
                    FROM main
                    WHERE messageID = %s
                """, (post_id,))
                new_vote_count = cursor.fetchone()[0]
                self.vote_buttons[post_id].config(text=f"Vote ({new_vote_count})")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")
        except KeyError:
            print(f"Error: Could not find post_id: {post_id} in vote_buttons.")

        self.update_kudo_points()

    def report_post(self, post_id):
        """
        Report a post, updating its status in the database.
        """
        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Check if the post has already been reported
            cursor.execute("""
                SELECT report
                FROM main
                WHERE messageID = %s
            """, (post_id,))
            
            report_status = cursor.fetchone()[0]

            if report_status == 1:
                messagebox.showwarning("Already Reported", "This post has already been reported.")
            else:
                # Update the report status
                cursor.execute("""
                    UPDATE main
                    SET report = 1
                    WHERE messageID = %s
                """, (post_id,))
                
                connection.commit()
                messagebox.showinfo("Report Submitted", "The post has been reported.")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def review_reported_posts(self):
        """
        Open the UI for reviewing reported posts.
        """
        self.clear_content_area()
        self.show_reported_posts_gui()

    def show_reported_posts_gui(self):
        """
        Display the UI for viewing and handling reported posts, allowing admins to remove or ignore reports.
        """
        # Create a frame for posts and their buttons
        posts_frame = tk.Frame(self.content_area)
        posts_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        post_ids = []

        def load_reported_posts():
            """
            Load and display posts that have been reported.
            """
            for widget in posts_frame.winfo_children():
                widget.destroy()  # Clear current items

            try:
                connection = mysql.connector.connect(
                    host="107.180.1.16",
                    user="summer2024team4",
                    password="summer2024team4",
                    database="summer2024team4"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT messageID, msgTitle, message FROM main WHERE report = 1 AND active = 1")
                posts = cursor.fetchall()
                cursor.close()
                connection.close()

                for index, post in enumerate(posts):
                    post_id, msg_title, message = post
                    post_ids.append(post_id)

                    # Create a frame for each post and its buttons
                    post_frame = tk.Frame(posts_frame)
                    post_frame.pack(fill=tk.X, pady=5)

                    # Text widget for the post content
                    post_text = tk.Text(post_frame, wrap=tk.WORD, height=5, width=80)
                    post_text.insert(tk.END, f"Post ID: {post_id} - Post Title: {msg_title}\nPost: {message}\n")
                    post_text.config(state=tk.DISABLED)  # Make it read-only
                    post_text.pack(side=tk.LEFT, padx=5)

                    # Create buttons for each post
                    button_frame = tk.Frame(post_frame)
                    button_frame.pack(side=tk.RIGHT)

                    remove_button = tk.Button(button_frame, text="Remove", command=lambda pid=post_id: remove_post(pid), width=10, height=1)
                    remove_button.pack(pady=2)

                    ignore_button = tk.Button(button_frame, text="Ignore", command=lambda pid=post_id: ignore_post(pid), width=10, height=1)
                    ignore_button.pack(pady=2)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        def remove_post(post_id):
            """
            Remove the reported post by marking it inactive in the database.
            """
            try:
                connection = mysql.connector.connect(
                    host="107.180.1.16",
                    user="summer2024team4",
                    password="summer2024team4",
                    database="summer2024team4"
                )
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE main
                    SET report = 0, active = 0
                    WHERE messageID = %s
                """, (post_id,))
                connection.commit()
                cursor.close()
                connection.close()

                messagebox.showinfo("Success", "The post has been removed.")
                load_reported_posts()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        def ignore_post(post_id):
            """
            Ignore the report for a post, removing its report status in the database.
            """
            try:
                connection = mysql.connector.connect(
                    host="107.180.1.16",
                    user="summer2024team4",
                    password="summer2024team4",
                    database="summer2024team4"
                )
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE main
                    SET report = 0
                    WHERE messageID = %s
                """, (post_id,))
                connection.commit()
                cursor.close()
                connection.close()

                messagebox.showinfo("Success", "The report flag has been removed.")
                load_reported_posts()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        load_reported_posts()

    def load_replies(self):
        """
        Load and display replies to a specific post from the database.
        """
        # Clear existing replies in the replies_frame
        for widget in self.replies_frame.winfo_children():
            widget.destroy()

        try:
            connection = mysql.connector.connect(
                host="107.180.1.16",
                user="summer2024team4",
                password="summer2024team4",
                database="summer2024team4"
            )
            cursor = connection.cursor()

            # Fetch replies for the original post, including memberID, msgTitle, and message
            cursor.execute("""
                SELECT m.memberID, m.msgTitle, m.message, m.vote, m.messageID
                FROM main m
                WHERE m.originalPostID = %s AND m.active = 1
            """, (self.original_post_id,))
            
            replies = cursor.fetchall()
            cursor.close()
            connection.close()

            # Display replies
            for reply in replies:
                reply_member_id, reply_msg_title, reply_message, reply_vote, reply_post_id = reply
                reply_header = tk.Label(self.replies_frame, text=f"Member ID: {reply_member_id}\n{reply_msg_title}", font=("Arial", 10, "bold"), anchor="w", justify="left")
                reply_header.pack(anchor="w", padx=20, pady=5)

                reply_message_label = tk.Label(self.replies_frame, text=reply_message, wraplength=700, justify="left")
                reply_message_label.pack(anchor="w", padx=20, pady=5)

                # Frame for Vote and Report buttons for replies
                reply_button_frame = tk.Frame(self.replies_frame)
                reply_button_frame.pack(anchor="w", padx=20, pady=5)

                # Vote button for replies
                reply_vote_button = tk.Button(reply_button_frame, text=f"Vote ({reply_vote})", command=lambda pid=reply_post_id: self.vote_post(pid))
                reply_vote_button.pack(side=tk.LEFT)

                # Report button for replies
                reply_report_button = tk.Button(reply_button_frame, text="Report", command=lambda pid=reply_post_id: self.report_post(pid))
                reply_report_button.pack(side=tk.LEFT)

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"Error: {err}")

    def post_reply(self):
        """
        Open a window for posting a reply to a specific post.
        """
        # Create a new window for posting a reply
        reply_window = tk.Toplevel(self)
        reply_window.title("Post Reply")
        reply_window.geometry("700x500")

        # Title input
        tk.Label(reply_window, text="Reply Title:").pack(pady=10)
        title_entry = tk.Entry(reply_window, width=80)
        title_entry.pack(pady=5)

        # Content input
        tk.Label(reply_window, text="Reply Content:").pack(pady=10)
        content_text = tk.Text(reply_window, height=15, width=70)
        content_text.pack(pady=5)

        def save_reply():
            """
            Save the reply to the database.
            """
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if title and content:
                self.save_reply_to_db(self.original_post_id, title, content)
                tk.messagebox.showinfo("Reply Posted", "Your reply has been posted.")
                reply_window.destroy()
            else:
                tk.messagebox.showwarning("Input Error", "Please fill in both title and content.")

        # Save button
        save_button = tk.Button(reply_window, text="Save Reply", command=save_reply)
        save_button.pack(pady=20)

    def manage_members(self):
        """
        Open the UI for managing members, including viewing and updating their active status.
        """
        self.clear_content_area()
        self.show_member_management_gui()

    def show_member_management_gui(self):
        """
        Display the UI for managing members, allowing admin to activate or deactivate members.
        """
        # Frame for member IDs and checkboxes
        members_frame = tk.Frame(self.content_area)
        members_frame.grid(row=0, column=0, padx=10, pady=10)

        # Load member data and checkboxes
        member_ids = []
        checkboxes = {}

        def load_members():
            """
            Load and display members from the database.
            """
            try:
                connection = mysql.connector.connect(
                    host="107.180.1.16",
                    user="summer2024team4",
                    password="summer2024team4",
                    database="summer2024team4"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT memberID, active FROM member")
                members = cursor.fetchall()
                cursor.close()
                connection.close()

                for index, member in enumerate(members):
                    member_id, active = member
                    member_ids.append(member_id)
                    
                    # Create and place label for member ID
                    member_label = tk.Label(members_frame, text=f"Member ID: {member_id}", font=14)
                    member_label.grid(row=index, column=0, sticky='w')

                    # Create and place checkbox for active status
                    var = tk.IntVar(value=active)
                    checkbox = tk.Checkbutton(members_frame, variable=var)
                    checkbox.grid(row=index, column=1, sticky='w')
                    checkboxes[member_id] = var

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        def update_members():
            """
            Update the active status of members in the database.
            """
            try:
                connection = mysql.connector.connect(
                    host="107.180.1.16",
                    user="summer2024team4",
                    password="summer2024team4",
                    database="summer2024team4"
                )
                cursor = connection.cursor()

                for member_id in member_ids:
                    active = checkboxes[member_id].get()
                    cursor.execute("""
                        UPDATE member SET active = %s WHERE memberID = %s
                    """, (active, member_id))

                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", "Member statuses updated successfully!")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        load_members()

        # Update button
        update_button = tk.Button(self.content_area, text="Update Members", command=update_members)
        update_button.grid(row=1, column=0, pady=10)

if __name__ == "__main__":
    app = SpeakEasyApp(is_admin=True, member_id=1)  # Change to `False` and provide member_id if not admin
    app.mainloop()
