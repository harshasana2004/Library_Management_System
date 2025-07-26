import tkinter as tk
from tkinter import messagebox
from database.db_connection import connect

def _add_student_to_db(name, email, contact, window):
    conn = connect()
    if not conn:
        messagebox.showerror("Database Error", "Database connection failed.", parent=window)
        return
    try:
        cursor = conn.cursor()
        query = "INSERT INTO students (name, email, contact_number) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, contact))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!", parent=window)
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add student: {e}", parent=window)
    finally:
        conn.close()

def show_add_student_window(parent):
    window = tk.Toplevel(parent)
    window.title("Add Student")
    window.geometry("350x300")
    window.configure(bg="#f0f0f0")
    window.transient(parent)
    window.grab_set()

    tk.Label(window, text="Enter Student Details", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    tk.Label(window, text="Name:", bg="#f0f0f0").pack()
    name_entry = tk.Entry(window, width=30)
    name_entry.pack(pady=5)

    tk.Label(window, text="Email:", bg="#f0f0f0").pack()
    email_entry = tk.Entry(window, width=30)
    email_entry.pack(pady=5)

    tk.Label(window, text="Contact Number:", bg="#f0f0f0").pack()
    contact_entry = tk.Entry(window, width=30)
    contact_entry.pack(pady=5)

    def on_submit():
        name = name_entry.get()
        email = email_entry.get()
        contact = contact_entry.get()
        if not (name and email and contact):
            messagebox.showwarning("Validation Error", "Please fill all fields.", parent=window)
            return
        _add_student_to_db(name, email, contact, window)

    tk.Button(window, text="Add Student", command=on_submit, bg="#4caf50", fg="white", width=20).pack(pady=20)