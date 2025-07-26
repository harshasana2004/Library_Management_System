import tkinter as tk
from tkinter import messagebox
from datetime import date
from database.db_connection import connect

# Import the workflow and management windows
from GUI.issue_workflow import show_issue_workflow_window
from GUI.return_workflow import show_return_workflow_window
from GUI.virtual_library_view import show_virtual_library_window
from GUI.management_view import show_management_window


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Library System")
        self.root.geometry("550x600")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # --- Header ---
        header_frame = tk.Frame(self.root, bg="#2c3e50")
        header_frame.pack(pady=20)
        tk.Label(header_frame, text="📚", font=("Arial", 36), bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Label(header_frame, text="College Library System", font=("Arial", 22, "bold"), bg="#2c3e50",
                 fg="white").pack(side=tk.LEFT)

        # --- Live Statistics Dashboard ---
        stats_frame = tk.LabelFrame(self.root, text="Live Library Stats", font=("Arial", 12, "bold"), bg="#34495e",
                                    fg="white", padx=15, pady=10)
        stats_frame.pack(pady=10, padx=20, fill="x")

        self.total_books_label = self.create_stat_label(stats_frame, "Total Books:")
        self.issued_books_label = self.create_stat_label(stats_frame, "Books on Loan:")
        self.students_label = self.create_stat_label(stats_frame, "Registered Students:")
        self.overdue_label = self.create_stat_label(stats_frame, "Books Overdue:")

        # --- Main Workflow Buttons ---
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(padx=20, pady=15, fill="x")

        main_button_style = {"font": ("Arial", 14, "bold"), "width": 25, "height": 2, "bd": 0, "fg": "white",
                             "activebackground": "#3498db"}

        tk.Button(buttons_frame, text="📤 Issue a Book", command=lambda: self.open_window(show_issue_workflow_window),
                  bg="#2980b9", **main_button_style).pack(pady=8, fill="x")
        tk.Button(buttons_frame, text="📥 Return a Book", command=lambda: self.open_window(show_return_workflow_window),
                  bg="#2980b9", **main_button_style).pack(pady=8, fill="x")

        # --- Secondary / Helper Buttons ---
        secondary_button_style = {"font": ("Arial", 11), "width": 25, "height": 2, "bd": 0, "fg": "white",
                                  "activebackground": "#95a5a6"}

        secondary_frame = tk.Frame(self.root, bg="#2c3e50")
        secondary_frame.pack(padx=20, pady=5, fill="x")

        tk.Button(secondary_frame, text="📖 View Virtual QR Library",
                  command=lambda: self.open_window(show_virtual_library_window), bg="#7f8c8d",
                  **secondary_button_style).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(secondary_frame, text="⚙️ Admin & Management",
                  command=lambda: self.open_window(show_management_window), bg="#7f8c8d",
                  **secondary_button_style).pack(side=tk.RIGHT, expand=True, padx=5)

        # Initial stats update
        self.update_stats()

    def create_stat_label(self, parent, text):
        """Helper function to create a consistent label for the dashboard."""
        frame = tk.Frame(parent, bg="#34495e")
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=text, font=("Arial", 11), bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT)
        value_label = tk.Label(frame, text="--", font=("Arial", 11, "bold"), bg="#34495e", fg="white")
        value_label.pack(side=tk.RIGHT)
        return value_label

    def update_stats(self):
        """Fetches the latest stats from the database and updates the dashboard."""
        conn = connect()
        if not conn:
            messagebox.showerror("Database Error", "Could not connect to the database to update stats.")
            return

        try:
            cursor = conn.cursor()

            # Get total books
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]
            self.total_books_label.config(text=str(total_books))

            # Get issued books
            cursor.execute("SELECT COUNT(*) FROM books WHERE available = FALSE")
            issued_books = cursor.fetchone()[0]
            self.issued_books_label.config(text=str(issued_books))

            # Get total students
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]
            self.students_label.config(text=str(total_students))

            # Get overdue books
            today = date.today()
            cursor.execute("SELECT COUNT(*) FROM issued_books WHERE returned = FALSE AND due_date < %s", (today,))
            overdue_books = cursor.fetchone()[0]
            self.overdue_label.config(text=f"{overdue_books} ❗", fg="#e74c3c" if overdue_books > 0 else "white")

        except Exception as e:
            print(f"Error updating stats: {e}")
        finally:
            conn.close()

    def open_window(self, window_function):
        """Opens a new window and updates stats when it's closed."""
        window_function(self.root)
        # When the sub-window is closed, this function will continue.
        # We update the stats to reflect any changes made.
        self.update_stats()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
