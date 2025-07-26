import tkinter as tk
from tkinter import messagebox
from database.db_connection import connect

def _add_book_to_db(title, author, isbn, window):
    conn = connect()
    if conn is None:
        messagebox.showerror("Database Error", "Could not connect to the database.", parent=window)
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)",
            (title, author, isbn)
        )
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully.", parent=window)
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add book: {str(e)}", parent=window)
    finally:
        if conn and conn.is_connected():
            conn.close()

def show_add_book_window(parent):
    window = tk.Toplevel(parent)
    window.title("Add Book")
    window.geometry("350x300")
    window.configure(bg="#f0f0f0")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="Enter Book Details", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    tk.Label(window, text="Title:", bg="#f0f0f0").pack()
    title_entry = tk.Entry(window, width=30)
    title_entry.pack(pady=5)

    tk.Label(window, text="Author:", bg="#f0f0f0").pack()
    author_entry = tk.Entry(window, width=30)
    author_entry.pack(pady=5)

    tk.Label(window, text="ISBN:", bg="#f0f0f0").pack()
    isbn_entry = tk.Entry(window, width=30)
    isbn_entry.pack(pady=5)

    def on_submit():
        title = title_entry.get()
        author = author_entry.get()
        isbn = isbn_entry.get()
        if not (title and author and isbn):
            messagebox.showwarning("Validation Error", "Please fill in all fields.", parent=window)
            return
        _add_book_to_db(title, author, isbn, window)

    tk.Button(window, text="Add Book", command=on_submit, bg="#4caf50", fg="white", width=20).pack(pady=20)