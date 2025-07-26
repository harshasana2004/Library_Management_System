import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import connect
from datetime import date


def _process_return(issue_id, book_id, window):
    conn = connect()
    if not conn:
        messagebox.showerror("Error", "Database connection failed.", parent=window)
        return
    cursor = conn.cursor()
    try:
        today = date.today()
        # Update issued_books and books table in one transaction
        cursor.execute(
            "UPDATE issued_books SET returned = TRUE, return_date = %s WHERE issue_id = %s",
            (today, issue_id)
        )
        cursor.execute("UPDATE books SET available = TRUE WHERE book_id = %s", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully!", parent=window)
        window.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"An error occurred: {e}", parent=window)
    finally:
        conn.close()


def show_return_workflow_window(parent):
    window = tk.Toplevel(parent)
    window.title("Return a Book")
    window.geometry("700x450")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="Return a Book", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    search_frame = tk.Frame(window, bg="#f5f5f5")
    search_frame.pack(pady=5, fill="x", padx=20)
    tk.Label(search_frame, text="Enter Student ID:", font=("Arial", 12), bg="#f5f5f5").pack(side=tk.LEFT)
    student_id_entry = tk.Entry(search_frame, font=("Arial", 12))
    student_id_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

    tree = ttk.Treeview(window, columns=("Issue ID", "Book ID", "Title", "ISBN", "Due Date"), show="headings")
    tree.heading("Issue ID", text="Issue ID")
    tree.column("Issue ID", width=80, anchor="center")
    tree.heading("Book ID", text="Book ID")
    tree.column("Book ID", width=80, anchor="center")
    tree.heading("Title", text="Title")
    tree.column("Title", width=250)
    tree.heading("ISBN", text="ISBN")
    tree.column("ISBN", width=120)
    tree.heading("Due Date", text="Due Date")
    tree.column("Due Date", width=100, anchor="center")
    tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    def find_borrowed_books():
        student_id = student_id_entry.get()
        if not student_id.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid numeric Student ID.", parent=window)
            return

        conn = connect()
        if not conn: return
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT ib.issue_id, b.book_id, b.title, b.isbn, ib.due_date
                FROM issued_books ib
                JOIN books b ON ib.book_id = b.book_id
                WHERE ib.student_id = %s AND ib.returned = FALSE
            """
            cursor.execute(query, (student_id,))
            results = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)

            if not results:
                messagebox.showinfo("Info", "No borrowed books found for this student.", parent=window)
            else:
                for row in results:
                    tree.insert("", tk.END,
                                values=(row['issue_id'], row['book_id'], row['title'], row['isbn'], row['due_date']))
        finally:
            conn.close()

    def on_return():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a book to return.", parent=window)
            return
        values = tree.item(selected_item)["values"]
        issue_id = values[0]
        book_id = values[1]
        _process_return(issue_id, book_id, window)

    btn_frame = tk.Frame(window, bg="#f5f5f5")
    btn_frame.pack(pady=10, fill="x", padx=20)
    tk.Button(btn_frame, text="🔍 Find Borrowed Books", command=find_borrowed_books, bg="#2980b9", fg="white",
              font=("Arial", 12)).pack(side=tk.LEFT, expand=True, padx=5)
    tk.Button(btn_frame, text="📥 Return Selected Book", command=on_return, bg="#27ae60", fg="white",
              font=("Arial", 12)).pack(side=tk.RIGHT, expand=True, padx=5)
