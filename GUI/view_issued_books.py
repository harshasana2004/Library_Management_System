import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import connect


def _fetch_issued_books(window):
    try:
        conn = connect()
        if not conn:
            messagebox.showerror("Database Error", "Database connection failed.", parent=window)
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ib.issue_id, s.name AS student_name, b.title AS book_title,
                   ib.issue_date, ib.due_date
            FROM issued_books ib
            JOIN students s ON ib.student_id = s.student_id
            JOIN books b ON ib.book_id = b.book_id
            WHERE ib.returned = FALSE
            ORDER BY ib.issue_date DESC
        """)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        messagebox.showerror("Database Error", str(e), parent=window)
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def show_view_issued_books_window(parent):
    window = tk.Toplevel(parent)
    window.title("Currently Issued Books")
    window.geometry("800x450")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="📋 All Currently Issued Books", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    cols = ("Issue ID", "Student Name", "Book Title", "Issue Date", "Due Date")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
    tree.column("Issue ID", width=80, anchor="center")
    tree.column("Student Name", width=180)
    tree.column("Book Title", width=300)
    tree.column("Issue Date", width=120, anchor="center")
    tree.column("Due Date", width=120, anchor="center")

    tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    rows = _fetch_issued_books(window)
    for row in rows:
        tree.insert("", "end", values=(
        row['issue_id'], row['student_name'], row['book_title'], row['issue_date'], row['due_date']))