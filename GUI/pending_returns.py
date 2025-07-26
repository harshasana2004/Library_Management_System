import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database.db_connection import connect


def _fetch_pending_returns(window):
    conn = connect()
    if not conn:
        messagebox.showerror("Database Error", "Database connection failed.", parent=window)
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                b.title, s.name, ib.issue_date, ib.due_date
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.book_id
            JOIN students s ON ib.student_id = s.student_id
            WHERE ib.returned = FALSE
            ORDER BY ib.due_date ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Database Error", str(e), parent=window)
        return []
    finally:
        conn.close()


def show_pending_returns_window(parent):
    window = tk.Toplevel(parent)
    window.title("Pending & Overdue Returns")
    window.geometry("800x450")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="❗ Pending Book Returns", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    tree = ttk.Treeview(window, columns=("Title", "Student", "Issue Date", "Due Date", "Status"), show="headings")
    tree.heading("Title", text="Title")
    tree.column("Title", width=250)
    tree.heading("Student", text="Student Name")
    tree.column("Student", width=150)
    tree.heading("Issue Date", text="Issue Date")
    tree.column("Issue Date", width=100, anchor="center")
    tree.heading("Due Date", text="Due Date")
    tree.column("Due Date", width=100, anchor="center")
    tree.heading("Status", text="Status")
    tree.column("Status", width=100, anchor="center")

    tree.tag_configure('overdue', foreground='red', font=('Arial', 10, 'bold'))
    tree.tag_configure('pending', foreground='orange')

    pending_books = _fetch_pending_returns(window)
    today = date.today()

    for row in pending_books:
        due = row['due_date']
        status_tag = "pending"
        status_text = "Pending"
        if due < today:
            status_tag = "overdue"
            status_text = "OVERDUE"

        tree.insert("", tk.END, values=(row['title'], row['name'], row['issue_date'], due, status_text),
                    tags=(status_tag,))

    tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)