-- Drop the database if it exists to ensure a fresh start
DROP DATABASE IF EXISTS library_db;

-- Create the new database
CREATE DATABASE library_db;

-- Switch to the new database
USE library_db;

-- Create the tables with improved structure
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(100) UNIQUE NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contact_number VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    book_id INT,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    returned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE RESTRICT
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
--  POPULATE THE DATABASE WITH DEFAULT DATA
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Insert Sample Books
INSERT INTO books (title, author, isbn) VALUES
('The Pragmatic Programmer', 'Andrew Hunt, David Thomas', '9780201616224'),
('Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '9780132350884'),
('Design Patterns: Elements of Reusable Object-Oriented Software', 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides', '9780201633610'),
('Introduction to the Theory of Computation', 'Michael Sipser', '9781133187790'),
('Artificial Intelligence: A Modern Approach', 'Stuart Russell, Peter Norvig', '9780136042594'),
('Database System Concepts', 'Abraham Silberschatz, Henry F. Korth, S. Sudarshan', '9780078022159'),
('Operating System Concepts', 'Abraham Silberschatz, Peter B. Galvin, Greg Gagne', '9781118063330'),
('Computer Networking: A Top-Down Approach', 'James F. Kurose, Keith W. Ross', '9780133594140');

-- Insert Sample Students
INSERT INTO students (name, email, contact_number) VALUES
('Rohan Verma', 'rohan.v@example.edu', '9876543210'),
('Priya Sharma', 'priya.s@example.edu', '9876543211'),
('Anjali Singh', 'anjali.s@example.edu', '9876543212'),
('Vikram Rathore', 'vikram.r@example.edu', '9876543213');