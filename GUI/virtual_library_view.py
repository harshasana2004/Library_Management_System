import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
from database.db_connection import connect


def show_qr_popup(book_id, title, parent):
    """Generates and displays a QR code in a new window."""
    qr_window = tk.Toplevel(parent)
    qr_window.title(f"QR Code for: {title}")
    qr_window.geometry("300x350")
    qr_window.configure(bg="white")
    qr_window.grab_set()

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(book_id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_resized = img.resize((250, 250), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img_resized)

    tk.Label(qr_window, text=f"Scan for Book ID: {book_id}", font=("Arial", 12), bg="white").pack(pady=10)
    img_label = tk.Label(qr_window, image=photo, bg="white")
    img_label.image = photo
    img_label.pack(pady=10)


def show_virtual_library_window(parent):
    window = tk.Toplevel(parent)
    window.title("Virtual QR Code Library")
    window.geometry("700x500")
    window.configure(bg="#f5f5f5")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="📚 Available Books", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=15)

    tree_frame = tk.Frame(window)
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    # Use a Treeview to display books and a button
    tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author"), show="headings")
    tree.heading("ID", text="Book ID")
    tree.column("ID", width=80, anchor="center")
    tree.heading("Title", text="Title")
    tree.column("Title", width=350)
    tree.heading("Author", text="Author")
    tree.column("Author", width=200)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_selected_qr():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a book from the list to view its QR code.",
                                   parent=window)
            return

        item_values = tree.item(selected_item)['values']
        book_id = item_values[0]
        title = item_values[1]
        show_qr_popup(book_id, title, window)

    tk.Button(window, text="Show QR Code for Selected Book", command=show_selected_qr, bg="#2980b9", fg="white",
              font=("Arial", 12, "bold")).pack(pady=15)

    # Populate the list with available books
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT book_id, title, author FROM books WHERE available = TRUE ORDER BY title")
            for book in cursor.fetchall():
                tree.insert("", tk.END, values=(book['book_id'], book['title'], book['author']))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not fetch books: {e}", parent=window)
        finally:
            conn.close()
