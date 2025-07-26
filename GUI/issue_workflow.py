import tkinter as tk
from tkinter import messagebox, Toplevel
import cv2
from datetime import date, timedelta
from database.db_connection import connect


class IssueWorkflow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Issue a Book")
        self.window.geometry("500x500")
        self.window.configure(bg="#f0f0f0")
        self.window.transient(parent)
        self.window.grab_set()

        self.student_info = None
        self.book_info = None

        # --- Student Section ---
        student_frame = tk.LabelFrame(self.window, text="Step 1: Find Student", font=("Arial", 12, "bold"), padx=10,
                                      pady=10, bg="#f0f0f0")
        student_frame.pack(pady=15, padx=20, fill="x")

        tk.Label(student_frame, text="Enter Student ID:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0,
                                                                                                 padx=5, pady=5)
        self.student_id_entry = tk.Entry(student_frame, width=20, font=("Arial", 11))
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(student_frame, text="Find Student", command=self.find_student, bg="#3498db", fg="white").grid(row=0,
                                                                                                                column=2,
                                                                                                                padx=5,
                                                                                                                pady=5)

        self.student_details_label = tk.Label(student_frame, text="Student details will appear here.",
                                              font=("Arial", 10, "italic"), bg="#f0f0f0", fg="grey")
        self.student_details_label.grid(row=1, column=0, columnspan=3, pady=10)

        # --- Book Section ---
        book_frame = tk.LabelFrame(self.window, text="Step 2: Scan Book", font=("Arial", 12, "bold"), padx=10, pady=10,
                                   bg="#f0f0f0")
        book_frame.pack(pady=15, padx=20, fill="x")

        tk.Button(book_frame, text="📷 Scan Book QR Code", command=self.scan_book, font=("Arial", 12), width=30,
                  height=2).pack(pady=10)
        self.book_details_label = tk.Label(book_frame, text="Book details will appear here.",
                                           font=("Arial", 10, "italic"), bg="#f0f0f0", fg="grey")
        self.book_details_label.pack(pady=10)

        # --- Confirmation Section ---
        confirm_button = tk.Button(self.window, text="Confirm and Issue Book", command=self.confirm_issue,
                                   font=("Arial", 14, "bold"), bg="#27ae60", fg="white", height=2)
        confirm_button.pack(pady=20, padx=20, fill="x")

    def find_student(self):
        student_id = self.student_id_entry.get()
        if not student_id.isdigit():
            messagebox.showerror("Invalid ID", "Student ID must be a number.", parent=self.window)
            return

        conn = connect()
        if not conn:
            messagebox.showerror("DB Error", "Database connection failed.", parent=self.window)
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            if student:
                self.student_info = student
                self.student_details_label.config(
                    text=f"ID: {student['student_id']}, Name: {student['name']}\nEmail: {student['email']}",
                    font=("Arial", 10, "normal"), fg="black")
            else:
                self.student_info = None
                self.student_details_label.config(text="Student not found.", font=("Arial", 10, "italic"), fg="red")
        finally:
            conn.close()

    def scan_book(self):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        scanned_book_id = None
        while True:
            ret, frame = cap.read()
            if not ret: break
            data, bbox, _ = detector.detectAndDecode(frame)
            if data:
                scanned_book_id = data
                break
            cv2.imshow("Scanning... Press 'q' to cancel", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

        if scanned_book_id and scanned_book_id.isdigit():
            self.find_book(scanned_book_id)
        elif scanned_book_id:
            messagebox.showerror("Invalid QR", "QR code does not contain a valid Book ID.", parent=self.window)

    def find_book(self, book_id):
        conn = connect()
        if not conn:
            messagebox.showerror("DB Error", "Database connection failed.", parent=self.window)
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
            book = cursor.fetchone()
            if book:
                if book['available']:
                    self.book_info = book
                    self.book_details_label.config(
                        text=f"ID: {book['book_id']}, Title: {book['title']}\nAuthor: {book['author']}",
                        font=("Arial", 10, "normal"), fg="black")
                else:
                    self.book_info = None
                    self.book_details_label.config(text="This book is already issued.", font=("Arial", 10, "italic"),
                                                   fg="orange")
            else:
                self.book_info = None
                self.book_details_label.config(text="Book not found.", font=("Arial", 10, "italic"), fg="red")
        finally:
            conn.close()

    def confirm_issue(self):
        if not self.student_info:
            messagebox.showerror("Error", "A valid student must be selected.", parent=self.window)
            return
        if not self.book_info:
            messagebox.showerror("Error", "A valid and available book must be scanned.", parent=self.window)
            return

        conn = connect()
        if not conn:
            messagebox.showerror("DB Error", "Database connection failed.", parent=self.window)
            return

        try:
            cursor = conn.cursor()
            issue_date = date.today()
            due_date = issue_date + timedelta(days=14)

            # Insert into issued_books and update book availability
            cursor.execute(
                "INSERT INTO issued_books (student_id, book_id, issue_date, due_date) VALUES (%s, %s, %s, %s)",
                (self.student_info['student_id'], self.book_info['book_id'], issue_date, due_date)
            )
            cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (self.book_info['book_id'],))

            conn.commit()
            messagebox.showinfo("Success", f"Book '{self.book_info['title']}' issued to {self.student_info['name']}.",
                                parent=self.window)
            self.window.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to issue book: {e}", parent=self.window)
        finally:
            conn.close()


def show_issue_workflow_window(parent):
    IssueWorkflow(parent)
