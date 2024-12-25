import tkinter as tk
from tkinter import ttk, messagebox
from controllers.employees_controller import get_all_employees, get_employee_by_id, add_employee, edit_employee, delete_employee
from utils.validators import is_valid_object_id
from utils.formatters import format_name
import bcrypt

def create_employees_view(db):
    """Create a Tkinter GUI for managing employees."""

    def refresh_employees():
        """Refresh the Treeview with the latest employee data."""
        try:
            employees = get_all_employees(db)
            tree.delete(*tree.get_children())
            for employee in employees:
                tree.insert("", "end", values=(
                    str(employee["_id"]),
                    employee["name"],
                    employee["email"],
                    employee["phone_number"],
                    employee["department_id"],
                    employee["hashed_password"],  
                    employee["nationality"]  
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employees: {e}")

    def add_employee_action():
        """Add a new employee."""
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone_number = phone_entry.get().strip()
        department_id = department_id_entry.get().strip()
        raw_password = password_entry.get().strip()
        nationality = nationality_entry.get().strip()

        if not name or not email or not phone_number or not is_valid_object_id(department_id) or not raw_password or not nationality:
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return

        try:
            add_employee(db, name, email, raw_password, nationality, phone_number, department_id)
            messagebox.showinfo("Success", "Employee added successfully.")
            refresh_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {e}")

    def edit_employee_action():
        """Edit the selected employee."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an employee to edit.")
            return

        employee_id = tree.item(selected_item)["values"][0]
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone_number = phone_entry.get().strip()
        department_id = department_id_entry.get().strip()
        raw_password = password_entry.get().strip() 
        nationality = nationality_entry.get().strip()
        if not name or not email or not phone_number or not is_valid_object_id(department_id) or not nationality:
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return
        if raw_password:
            if isinstance(raw_password, str):  
                raw_password = raw_password.encode('utf-8')  
            hashed_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())  
        else:
            hashed_password = None  
        try:
            edit_employee(db, employee_id, {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "department_id": department_id,
                "hashed_password": hashed_password,
                "nationality": nationality
            })
            messagebox.showinfo("Success", "Employee updated successfully.")
            refresh_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {e}")

    def delete_employee_action():
        """Delete the selected employee."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an employee to delete.")
            return

        employee_id = tree.item(selected_item)["values"][0]

        if not is_valid_object_id(employee_id):
            messagebox.showwarning("Validation Error", "Invalid Employee ID.")
            return

        try:
            delete_employee(db, employee_id)
            messagebox.showinfo("Success", "Employee deleted successfully.")
            refresh_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete employee: {e}")

    def on_tree_select(event):
        """Handle Treeview item selection."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, values[2])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, values[3])
            department_id_entry.delete(0, tk.END)
            department_id_entry.insert(0, values[4])

    def search_employee_by_id():
        """Search for an employee by its ID and display its details."""
        employee_id = search_id_entry.get().strip()
        if not is_valid_object_id(employee_id):
            messagebox.showwarning("Validation Error", "Invalid Employee ID.")
            return

        try:
            employee = get_employee_by_id(db, employee_id)
            if employee:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, employee["name"])
                email_entry.delete(0, tk.END)
                email_entry.insert(0, employee["email"])
                phone_entry.delete(0, tk.END)
                phone_entry.insert(0, employee["phone_number"])
                department_id_entry.delete(0, tk.END)
                department_id_entry.insert(0, employee["department_id"])
                messagebox.showinfo("Success", "Employee details loaded successfully.")
                tree.delete(*tree.get_children())
                tree.insert("", "end", values=(employee["_id"], employee["name"], employee["email"], employee["phone_number"], employee["department_id"], employee["hashed_password"], employee["nationality"]))
            else:
                messagebox.showinfo("Not Found", "No employee found with the given ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employee: {e}")

    def show_all_employees():
        """Show all employees after a search."""
        search_id_entry.delete(0, tk.END)  
        refresh_employees()  

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Employees Management")

    # Input Form
    form_frame = tk.Frame(root)
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    phone_entry = tk.Entry(form_frame)
    phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Department ID:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    department_id_entry = tk.Entry(form_frame)
    department_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    password_entry = tk.Entry(form_frame, show="*")  # Password field (hidden input)
    password_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Nationality:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    nationality_entry = tk.Entry(form_frame)
    nationality_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

    # Search Section
    search_frame = tk.Frame(root)
    search_frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(search_frame, text="Search by ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    search_id_entry = tk.Entry(search_frame)
    search_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tk.Button(search_frame, text="Search", command=search_employee_by_id).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(search_frame, text="Show All", command=show_all_employees).grid(row=0, column=3, padx=5, pady=5)

    # Action Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Button(button_frame, text="Add Employee", command=add_employee_action).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Edit Employee", command=edit_employee_action).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Delete Employee", command=delete_employee_action).grid(row=0, column=2, padx=5, pady=5)

    # Treeview for displaying employees
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    columns = ("_id", "name", "email", "phone_number", "department_id", "hashed_password", "nationality")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree.heading("_id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("email", text="Email")
    tree.heading("phone_number", text="Phone Number")
    tree.heading("department_id", text="Department ID")
    tree.heading("hashed_password", text="Hashed Password") 
    tree.heading("nationality", text="Nationality")  

    tree.column("_id", width=150)
    tree.column("name", width=150)
    tree.column("email", width=200)
    tree.column("phone_number", width=150)
    tree.column("department_id", width=150)
    tree.column("hashed_password", width=200)  
    tree.column("nationality", width=150)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.pack(fill="both", expand=True)

    refresh_employees()

    root.mainloop()
