import tkinter as tk
from tkinter import messagebox
from views.departments_view import create_departments_view
from views.employees_view import create_employees_view
from views.roles_view import create_roles_view
from views.companies_view import create_companies_view

def create_main_menu(db):
    """Create the main menu window for the application. """
    def open_companies_view():
        """Open the Companies Management view."""
        try:
            create_companies_view(db)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Companies view: {e}")

    def open_departments_view():
        """Open the Departments Management view."""
        try:
            create_departments_view(db)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Departments view: {e}")

    def open_employees_view():
        """Open the Employees Management view."""
        try:
            create_employees_view(db)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Employees view: {e}")

    def open_roles_view():
        """Open the Roles Management view."""
        try:
            create_roles_view(db)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Roles view: {e}")

    root = tk.Tk()
    root.title("Management System")

    # Main Menu Buttons
    tk.Label(root, text="Welcome to the Management System", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Manage Companies", command=open_companies_view, width=30).pack(pady=10)
    tk.Button(root, text="Manage Departments", command=open_departments_view, width=30).pack(pady=10)
    tk.Button(root, text="Manage Employees", command=open_employees_view, width=30).pack(pady=10)
    tk.Button(root, text="Manage Roles", command=open_roles_view, width=30).pack(pady=10)

    tk.Button(root, text="Exit", command=root.destroy, width=30, bg="red", fg="white").pack(pady=20)

    root.mainloop()