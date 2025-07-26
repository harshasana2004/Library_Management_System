import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import connect

def _delete_book(book_id, tree, window):
    conn = connect()
    if not conn:
        messagebox.showerror("Error", "Database connection failed.", parent=window)
        return

    cursor = conn.cursor()
    try:
        # Check if the book is currently issued
        cursor.execute("SELECT * FROM issued_books WHERE book_id = %s AND returned = FALSE", (book_id,))
        if cursor.fetchone():
            messagebox.showwarning("Cannot Delete", "Book is currently issued and cannot be deleted.", parent=window)
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete book ID {book_id}?", parent=window)
        if confirm:
            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully!", parent=window)
            # Refresh the search to remove the deleted book
            for item in tree.get_children():
                if tree.item(item)['values'][0] == book_id:
                    tree.delete(item)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}", parent=window)
    finally:
        conn.close()

def _search_books(title, tree, window):
    conn = connect()
    if not conn:
        messagebox.showerror("Error", "Database connection failed.", parent=window)
        return

    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT book_id, title, author, isbn FROM books WHERE title LIKE %s OR author LIKE %s"
        search_term = f"%{title}%"
        cursor.execute(query, (search_term, search_term))
        results = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        if not results:
            messagebox.showinfo("No Results", "No books found matching your search.", parent=window)
        else:
            for row in results:
                tree.insert("", tk.END, values=(row['book_id'], row['title'], row['author'], row['isbn']))
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=window)
    finally:
        conn.close()

def show_delete_book_window(parent):
    window = tk.Toplevel(parent)
    window.title("Delete Book")
    window.geometry("700x400")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="🗑️ Delete Book", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    search_frame = tk.Frame(window, bg="#f5f5f5")
    search_frame.pack(pady=5, fill="x", padx=20)
    tk.Label(search_frame, text="Search Book Title/Author:", font=("Arial", 12), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

    tree = ttk.Treeview(window, columns=("ID", "Title", "Author", "ISBN"), show="headings")
    tree.heading("ID", text="ID")
    tree.column("ID", width=50, anchor="center")
    tree.heading("Title", text="Title")
    tree.column("Title", width=250)
    tree.heading("Author", text="Author")
    tree.column("Author", width=200)
    tree.heading("ISBN", text="ISBN")
    tree.column("ISBN", width=150, anchor="center")
    tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    def on_search():
        title = search_entry.get()
        if title:
            _search_books(title, tree, window)
        else:
            messagebox.showwarning("Input Required", "Please enter a title or author to search.", parent=window)

    def on_delete():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book from the list to delete.", parent=window)
            return
        book_id = tree.item(selected_item)["values"][0]
        _delete_book(book_id, tree, window)

    btn_frame = tk.Frame(window, bg="#f5f5f5")
    btn_frame.pack(pady=10, fill="x", padx=20)
    tk.Button(btn_frame, text="🔍 Search", command=on_search, bg="#2196f3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, expand=True, padx=5)
    tk.Button(btn_frame, text="🗑️ Delete Selected", command=on_delete, bg="#f44336", fg="white", font=("Arial", 12)).pack(side=tk.RIGHT, expand=True, padx=5)