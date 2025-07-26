import tkinter as tk
from GUI.add_book import show_add_book_window
from GUI.add_student import show_add_student_window
from GUI.delete_book import show_delete_book_window
from GUI.search_book import show_search_book_window
from GUI.pending_returns import show_pending_returns_window
from GUI.view_issued_books import show_view_issued_books_window


def show_management_window(parent):
    window = tk.Toplevel(parent)
    window.title("Admin & Management")
    window.geometry("400x500")
    window.configure(bg="#ecf0f1")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="⚙️ Management Dashboard", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=20)

    button_style = {"font": ("Arial", 11), "width": 30, "height": 2, "bd": 0, "fg": "white",
                    "activebackground": "#95a5a6"}

    buttons_frame = tk.Frame(window, bg="#ecf0f1")
    buttons_frame.pack(padx=20, pady=10, fill="x")

    # Define buttons for all management tasks
    admin_buttons = [
        ("➕ Add New Book", lambda: show_add_book_window(window), "#34495e"),
        ("➕ Register New Student", lambda: show_add_student_window(window), "#34495e"),
        ("🗑️ Delete a Book", lambda: show_delete_book_window(window), "#c0392b"),
        ("🔍 Search Full Catalog", lambda: show_search_book_window(window), "#f39c12"),
        ("📋 View All Issued Books", lambda: show_view_issued_books_window(window), "#7f8c8d"),
        ("❗ View Pending/Overdue Returns", lambda: show_pending_returns_window(window), "#7f8c8d"),
    ]

    for text, command, color in admin_buttons:
        tk.Button(buttons_frame, text=text, command=command, bg=color, **button_style).pack(pady=5, fill="x")
