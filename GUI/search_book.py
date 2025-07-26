import tkinter as tk
from tkinter import messagebox, scrolledtext
from database.db_connection import connect


def _search_books(keyword, result_text, window):
    if not keyword:
        messagebox.showwarning("Input Error", "Please enter a search keyword.", parent=window)
        return

    conn = connect()
    if conn is None:
        messagebox.showerror("Database Error", "Failed to connect to the database.", parent=window)
        return

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT title, author, isbn, available FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s"
        search_term = f"%{keyword}%"
        cursor.execute(query, (search_term, search_term, search_term))
        results = cursor.fetchall()

        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        if results:
            for row in results:
                status = "Available ✅" if row['available'] else "Issued ❌"
                result_text.insert(tk.END,
                                   f"Title: {row['title']}\nAuthor: {row['author']}\nISBN: {row['isbn']}\nStatus: {status}\n\n")
        else:
            result_text.insert(tk.END, "No books found matching your criteria.")
        result_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", str(e), parent=window)
    finally:
        if conn and conn.is_connected():
            conn.close()


def show_search_book_window(parent):
    window = tk.Toplevel(parent)
    window.title("🔍 Search Book")
    window.geometry("500x500")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="Enter Title / Author / ISBN:", font=("Arial", 12), bg="#f5f5f5").pack(pady=10)
    entry_search = tk.Entry(window, font=("Arial", 12), width=40)
    entry_search.pack(pady=5)

    result_text = scrolledtext.ScrolledText(window, width=60, height=20, font=("Arial", 10), state=tk.DISABLED)
    result_text.pack(pady=10)

    tk.Button(window, text="Search", font=("Arial", 12, "bold"), bg="#2196f3", fg="white",
              command=lambda: _search_books(entry_search.get().strip(), result_text, window)).pack(pady=10)