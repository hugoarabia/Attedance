import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
import re
from datetime import datetime

# Initialize Tkinter root window
root = tk.Tk()
root.title("Professor Registration and Login")
root.geometry("800x400")
root.configure(bg="lightgray")

# Initialize SQLite connection
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()  # Create a cursor object to interact with the database

# Create necessary tables (professors, students, attendance, and attendance_datetime)
cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')  # Table for storing professor usernames and passwords

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    name TEXT,
                    student_number TEXT PRIMARY KEY,
                    section TEXT,
                    course TEXT,
                    year_level TEXT)''')  # Table for storing student information

cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    student_number TEXT,
                    status TEXT,
                    FOREIGN KEY(student_number) REFERENCES students(student_number))''')  # Table to store attendance status

cursor.execute('''CREATE TABLE IF NOT EXISTS attendance_datetime (
                    student_number TEXT,
                    attendance_time TEXT,
                    FOREIGN KEY(student_number) REFERENCES students(student_number))''')  # Table to store the datetime of attendance events

conn.commit()  # Commit the changes to the database

# Professor login flag
is_professor_logged_in = False  # This flag checks if the professor is logged in

# Function to open the student registration window
def open_student_registration():
    if not is_professor_logged_in:
        messagebox.showerror("Access Denied", "You must log in as a professor first.")
        return

    student_window = tk.Toplevel(root)  # Create a new window for student registration
    student_window.title("Student Registration")
    student_window.geometry("600x500")
    student_window.configure(bg="lightgray")

    # Define the fields and their validation patterns
    fields = [
        ("Name", "(?i)^[A-Za-z ]+$"),  # Name should contain only letters and spaces
        ("Student No", "(?i)^[A-Za-z0-9]+$"),  # Student number can be alphanumeric
        ("Section", "(?i)^[A-Za-z0-9]+$"),  # Section can be alphanumeric
        ("Course", "(?i)^[A-Za-z ]+$"),  # Course should contain only letters and spaces
        ("Year Level", "(?i)^(First Year|Second Year|Third Year|Fourth Year)$")  # Validates year level
    ]

    entries = {}  # Dictionary to store the entry widgets for each field

    # Function to validate and register the student
    def validate_and_register_student():
        # Validate each field based on its regex pattern
        for field, pattern in fields:
            value = entries[field].get().strip()  # Get the entered value and strip any extra spaces
            if not re.match(pattern, value, re.IGNORECASE):  # If the value doesn't match the pattern
                messagebox.showerror("Input Error", f"Invalid input for {field}. Please try again.")
                return

        # Retrieve the values from the entry fields
        name = entries["Name"].get()
        student_number = entries["Student No"].get()
        section = entries["Section"].get()
        course = entries["Course"].get()
        year_level = entries["Year Level"].get()

        try:
            # Insert the student details into the database
            cursor.execute("INSERT INTO students (name, student_number, section, course, year_level) VALUES (?, ?, ?, ?, ?)",
                           (name, student_number, section, course, year_level))
            conn.commit()  # Commit the changes
            messagebox.showinfo("Success", "Student registered successfully!")  # Show success message
            for entry in entries.values():
                entry.delete(0, tk.END)  # Clear the entry fields after registration

            # After successful registration, open a new window with options
            show_registration_options()

        except sqlite3.IntegrityError:  # If the student number already exists in the database
            messagebox.showerror("Error", "Student number already exists.")

    # Create the entry fields and labels for each field
    for field, pattern in fields:
        label = tk.Label(student_window, text=field, font=("Arial", 12), bg="lightgray")
        label.pack(pady=5)
        entry = tk.Entry(student_window, font=("Arial", 12), width=30)
        entry.pack(pady=5)
        entries[field] = entry

    # Register button to trigger the validation and registration process
    register_button = tk.Button(student_window, text="Register Student", font=("Arial", 12), bg="#4682B4", fg="white", command=validate_and_register_student)
    register_button.pack(pady=20)

# Function to show the registration options after successful registration
def show_registration_options():
    options_window = tk.Toplevel(root)  # Create a new window with options
    options_window.title("Registration Options")
    options_window.geometry("400x300")
    options_window.configure(bg="lightgray")

    def go_back_to_main():
        options_window.destroy()  # Close the options window
        root.deiconify()  # Show the main window again

    def register_another_student():
        options_window.destroy()  # Close the options window
        open_student_registration()  # Open the student registration window again

    def log_in_and_record_attendance():
        options_window.destroy()  # Close the options window
        login_professor()  # Open the professor login to record attendance

    # Buttons for different options after successful registration
    go_back_button = tk.Button(options_window, text="Go Back to Main Menu", font=("Arial", 12), bg="#4682B4", fg="white", command=go_back_to_main)
    go_back_button.pack(pady=10)

    register_another_button = tk.Button(options_window, text="Register Another Student", font=("Arial", 12), bg="#4682B4", fg="white", command=register_another_student)
    register_another_button.pack(pady=10)

    record_attendance_button = tk.Button(options_window, text="Log in and Record Attendance", font=("Arial", 12), bg="#4682B4", fg="white", command=log_in_and_record_attendance)
    record_attendance_button.pack(pady=10)

# Function for professor registration
def register_professor():
    username = username_entry_reg.get().strip().lower()  # Get and sanitize the username input
    password = password_entry_reg.get().strip()  # Get and sanitize the password input

    if not username or not password:  # Check if either field is empty
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash the password

    try:
        # Insert the professor's username and hashed password into the database
        cursor.execute("INSERT INTO professors (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Professor registered successfully!")  # Show success message
        username_entry_reg.delete(0, tk.END)  # Clear the input fields
        password_entry_reg.delete(0, tk.END)

        # After successful registration, open a new window with options
        show_registration_options()

    except sqlite3.IntegrityError:  # If the username already exists in the database
        messagebox.showerror("Error", "Username already exists.")

# Function for professor login
def login_professor():
    global is_professor_logged_in  # Reference the global variable for login status
    username = username_entry_log.get().strip().lower()  # Get and sanitize the username input
    password = password_entry_log.get().strip()  # Get and sanitize the password input

    if not username or not password:  # Check if either field is empty
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    cursor.execute("SELECT password FROM professors WHERE username = ?", (username,))  # Fetch the stored password
    professor = cursor.fetchone()  # Get the professor's record

    if not professor:  # If no professor is found with the entered username
        messagebox.showerror("Error", "No account found. Please register first.")
        return

    if bcrypt.checkpw(password.encode('utf-8'), professor[0]):  # Check if the entered password matches the stored password
        messagebox.showinfo("Success", "Login successful!")  # Show success message
        is_professor_logged_in = True  # Set the login flag to True
        open_student_registration()  # Open the student registration window
    else:
        messagebox.showerror("Error", "Invalid password. Please try again.")

# Layout for Registration and Login
frame = tk.Frame(root, bg="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

# Frame for Professor Registration
reg_frame = tk.Frame(frame, bg="lightgray")
reg_frame.pack(side="left", padx=40)

register_label = tk.Label(reg_frame, text="Professor Registration", font=("Helvetica", 14, "bold"), bg="lightgray")
register_label.pack(pady=10)
username_entry_reg = tk.Entry(reg_frame, font=("Arial", 12), width=30)
username_entry_reg.pack(pady=5)
password_entry_reg = tk.Entry(reg_frame, font=("Arial", 12), width=30, show="*")  # Hide password input with asterisks
password_entry_reg.pack(pady=5)

# Checkbox to toggle password visibility
show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(reg_frame, text="Show Password", variable=show_password_var, command=lambda: password_entry_reg.config(show="" if show_password_var.get() else "*"))
show_password_check.pack()

# Register button to trigger the registration process
register_button = tk.Button(reg_frame, text="Register", font=("Arial", 12), bg="#4682B4", fg="white", command=register_professor)
register_button.pack(pady=20)

# Frame for Professor Login
login_frame = tk.Frame(frame, bg="lightgray")
login_frame.pack(side="right", padx=40)

login_label = tk.Label(login_frame, text="Professor Login", font=("Helvetica", 14, "bold"), bg="lightgray")
login_label.pack(pady=10)
username_entry_log = tk.Entry(login_frame, font=("Arial", 12), width=30)
username_entry_log.pack(pady=5)
password_entry_log = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")  # Hide password input with asterisks
password_entry_log.pack(pady=5)

# Login button to trigger the login process
login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), bg="#4682B4", fg="white", command=login_professor)
login_button.pack(pady=20)

if __name__ == "__main__":
    root.mainloop()  # Start the Tkinter main event loop
