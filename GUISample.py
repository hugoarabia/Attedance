import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize Tkinter root window
root = tk.Tk()
root.title("Professor Registration and Login")
root.geometry("800x600")
root.configure(bg="lightgray")

# Create SQLite connection
conn = sqlite3.connect('professor_student.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    suffix TEXT,
    student_number TEXT PRIMARY KEY,
    course TEXT,
    section TEXT,
    year_level TEXT
)''')

# Create the professors table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
    username TEXT PRIMARY KEY,
    password TEXT
)''')
conn.commit()

# Professor login status
is_professor_logged_in = False

# Function to toggle password visibility
def toggle_password(entry, checkbox_var):
    if checkbox_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

# Function to open the student registration window
def open_student_registration():
    if not is_professor_logged_in:
        messagebox.showerror("Access Denied", "You must log in as a professor first.")
        return

    student_window = tk.Toplevel(root)
    student_window.title("Student Registration")
    student_window.geometry("600x600")
    student_window.configure(bg="lightgray")

    register_label = tk.Label(student_window, text="Student Registration", font=("Helvetica", 18, "bold"), bg="lightgray")
    register_label.pack(pady=10)

    fields = [
        ("First Name", False),
        ("Middle Name (Optional)", True),
        ("Last Name", False),
        ("Suffix (Optional)", True),
        ("Student Number", False),
        ("Course", False),
        ("Section", False),
        ("Year Level", False),
    ]

    entries = {}

    def validate_and_register_student():
        student_data = {}
        for field, is_optional in fields:
            value = entries[field].get().strip()
            if not is_optional and not value:
                messagebox.showerror("Input Error", f"{field} cannot be empty.")
                return
            student_data[field] = value if value else None  # Store None for optional fields if empty

        # Apply capitalization rules
        student_data = {
            "First Name": student_data["First Name"].title(),
            "Middle Name (Optional)": student_data["Middle Name (Optional)"].title() if student_data["Middle Name (Optional)"] else None,
            "Last Name": student_data["Last Name"].title(),
            "Suffix (Optional)": student_data["Suffix (Optional)"].title() if student_data["Suffix (Optional)"] else None,
            "Student Number": student_data["Student Number"].upper(),
            "Course": student_data["Course"].upper(),
            "Section": student_data["Section"].upper(),
            "Year Level": student_data["Year Level"].title(),
        }

        try:
            cursor.execute("""INSERT INTO students (first_name, middle_name, last_name, suffix, student_number, course, section, year_level)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
                student_data["First Name"],
                student_data["Middle Name (Optional)"],
                student_data["Last Name"],
                student_data["Suffix (Optional)"],
                student_data["Student Number"],
                student_data["Course"],
                student_data["Section"],
                student_data["Year Level"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Student registered successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student number already registered.")

    for field, is_optional in fields:
        label = tk.Label(student_window, text=field, font=("Arial", 12), bg="lightgray")
        label.pack(pady=5)
        entry = tk.Entry(student_window, font=("Arial", 12), width=30)
        entry.pack(pady=5)
        entries[field] = entry

    register_button = tk.Button(student_window, text="Register Student", font=("Arial", 12), bg="#4682B4", fg="white", command=validate_and_register_student)
    register_button.pack(pady=20)

# Function for professor registration
def register_professor():
    username = username_entry_reg.get().strip()
    password = password_entry_reg.get().strip()

    if not username or not password:
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    try:
        cursor.execute("INSERT INTO professors (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Professor registered successfully!")
        username_entry_reg.delete(0, tk.END)
        password_entry_reg.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Function for professor login
def login_professor():
    global is_professor_logged_in
    username = username_entry_log.get().strip()
    password = password_entry_log.get().strip()

    if not username or not password:
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    cursor.execute("SELECT * FROM professors WHERE username = ?", (username,))
    professor = cursor.fetchone()

    if professor and professor[1] == password:
        messagebox.showinfo("Success", "Login successful!")
        is_professor_logged_in = True
        open_student_registration()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to view all registered students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("No Students", "No students registered yet.")
        return

    student_window = tk.Toplevel(root)
    student_window.title("Registered Students")
    student_window.geometry("800x400")
    student_window.configure(bg="lightgray")

    headers = ["First Name", "Middle Name", "Last Name", "Suffix", "Student Number", "Course", "Section", "Year Level"]
    for i, header in enumerate(headers):
        tk.Label(student_window, text=header, font=("Arial", 12, "bold"), bg="lightgray").grid(row=0, column=i, padx=10, pady=5)

    for row_idx, student in enumerate(students, start=1):
        for col_idx, value in enumerate(student):
            if col_idx < 4 or col_idx == 7:  # Name fields or Year Level
                value = value.title() if value else ""
            elif col_idx >= 4 and col_idx <= 6:  # Student Number, Course, Section
                value = value.upper() if value else ""
            tk.Label(student_window, text=value, font=("Arial", 12), bg="lightgray").grid(row=row_idx, column=col_idx, padx=10, pady=5)

# UI for Registration and Login
frame = tk.Frame(root, bg="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Professor Registration UI
reg_frame = tk.Frame(frame, bg="lightgray")
reg_frame.pack(side="left", padx=40)

register_label = tk.Label(reg_frame, text="Professor Registration", font=("Helvetica", 14, "bold"), bg="lightgray")
register_label.pack(pady=10)

username_label_reg = tk.Label(reg_frame, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_reg.pack(pady=5)
username_entry_reg = tk.Entry(reg_frame, font=("Arial", 12), width=30)
username_entry_reg.pack(pady=5)

password_label_reg = tk.Label(reg_frame, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_reg.pack(pady=5)
password_entry_reg = tk.Entry(reg_frame, font=("Arial", 12), width=30, show="*")
password_entry_reg.pack(pady=5)

password_checkbox_var_reg = tk.BooleanVar()
password_checkbox_reg = tk.Checkbutton(reg_frame, text="Show Password", variable=password_checkbox_var_reg, command=lambda: toggle_password(password_entry_reg, password_checkbox_var_reg), bg="lightgray")
password_checkbox_reg.pack(pady=5)

register_button = tk.Button(reg_frame, text="Register", font=("Arial", 12), bg="#4682B4", fg="white", command=register_professor)
register_button.pack(pady=20)

# Professor Login UI
log_frame = tk.Frame(frame, bg="lightgray")
log_frame.pack(side="left", padx=40)

login_label = tk.Label(log_frame, text="Professor Login", font=("Helvetica", 14, "bold"), bg="lightgray")
login_label.pack(pady=10)

username_label_log = tk.Label(log_frame, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_log.pack(pady=5)
username_entry_log = tk.Entry(log_frame, font=("Arial", 12), width=30)
username_entry_log.pack(pady=5)

password_label_log = tk.Label(log_frame, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_log.pack(pady=5)
password_entry_log = tk.Entry(log_frame, font=("Arial", 12), width=30, show="*")
password_entry_log.pack(pady=5)

password_checkbox_var_log = tk.BooleanVar()
password_checkbox_log = tk.Checkbutton(log_frame, text="Show Password", variable=password_checkbox_var_log, command=lambda: toggle_password(password_entry_log, password_checkbox_var_log), bg="lightgray")
password_checkbox_log.pack(pady=5)

login_button = tk.Button(log_frame, text="Login", font=("Arial", 12), bg="#4682B4", fg="white", command=login_professor)
login_button.pack(pady=20)

# View Students Button
view_button = tk.Button(root, text="View Registered Students", font=("Arial", 12), bg="#4682B4", fg="white", command=view_students)
view_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

# Close the connection when done
conn.close()

