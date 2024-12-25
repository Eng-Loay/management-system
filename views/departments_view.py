import tkinter as tk
from tkinter import ttk, messagebox
from controllers.departments_controller import get_all_departments, get_department_by_id, add_department, edit_department, delete_department
from utils.validators import is_valid_object_id
from utils.formatters import format_name

def create_departments_view(db):
    """Create a Tkinter GUI for managing departments."""
    def refresh_departments():
        """Refresh the Treeview with the latest department data."""
        try:
            departments = get_all_departments(db)
            tree.delete(*tree.get_children())
            for department in departments:
                tree.insert("", "end", values=(
                    str(department["_id"]),
                    department["name"],
                    department["description"],
                    department["company_id"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch departments: {e}")

    def add_department_action():
        """Add a new department."""
        name = format_name(name_entry.get().strip())
        description = description_entry.get().strip()
        company_id = company_id_entry.get().strip()

        if not name or not description or not is_valid_object_id(company_id):
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return

        try:
            add_department(db, name, description, company_id)
            messagebox.showinfo("Success", "Department added successfully.")
            refresh_departments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department: {e}")
    def show_all_departments():
        """Show all departments."""
        refresh_departments()
    def edit_department_action():
        """Edit the selected department."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a department to edit.")
            return

        department_id = tree.item(selected_item)["values"][0]
        name = format_name(name_entry.get().strip())
        description = description_entry.get().strip()
        company_id = company_id_entry.get().strip()

        if not name or not description or not is_valid_object_id(company_id):
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return

        try:
            edit_department(db, department_id, {
                "name": name,
                "description": description,
                "company_id": company_id
            })
            messagebox.showinfo("Success", "Department updated successfully.")
            refresh_departments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update department: {e}")

    def delete_department_action():
        """Delete the selected department."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a department to delete.")
            return

        department_id = tree.item(selected_item)["values"][0]

        if not is_valid_object_id(department_id):
            messagebox.showwarning("Validation Error", "Invalid Department ID.")
            return

        try:
            delete_department(db, department_id)
            messagebox.showinfo("Success", "Department deleted successfully.")
            refresh_departments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete department: {e}")

    def on_tree_select(event):
        """Handle Treeview item selection."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            description_entry.delete(0, tk.END)
            description_entry.insert(0, values[2])
            company_id_entry.delete(0, tk.END)
            company_id_entry.insert(0, values[3])

    def search_department_by_id():
        """Search for a department by its ID and display its details."""
        department_id = search_id_entry.get().strip()

        if not is_valid_object_id(department_id):
            messagebox.showwarning("Validation Error", "Invalid Department ID.")
            return

        try:
            department = get_department_by_id(db, department_id)
            
            if department:
                tree.delete(*tree.get_children())
                
                tree.insert("", "end", values=(
                    str(department["_id"]),
                    department["name"],
                    department["description"],
                    department["company_id"]
                ))

                name_entry.delete(0, tk.END)
                name_entry.insert(0, department["name"])

                description_entry.delete(0, tk.END)
                description_entry.insert(0, department["description"])

                company_id_entry.delete(0, tk.END)
                company_id_entry.insert(0, department["company_id"])

                messagebox.showinfo("Success", "Department details loaded successfully.")
            else:
                messagebox.showinfo("Not Found", "No department found with the given ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch department: {e}")


    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Departments Management")

    # Input Form
    form_frame = tk.Frame(root)
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    description_entry = tk.Entry(form_frame)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Company ID:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    company_id_entry = tk.Entry(form_frame)
    company_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Search Section
    search_frame = tk.Frame(root)
    search_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(search_frame, text="Search by ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    search_id_entry = tk.Entry(search_frame)
    search_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tk.Button(search_frame, text="Search", command=search_department_by_id).grid(row=0, column=2, padx=5, pady=5)

    # Action Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Button(button_frame, text="Add Department", command=add_department_action).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Edit Department", command=edit_department_action).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Delete Department", command=delete_department_action).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Show All Departments", command=show_all_departments).grid(row=0, column=3, padx=5, pady=5)

    # Treeview for displaying departments
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    columns = ("_id", "name", "description", "company_id")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree.heading("_id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("description", text="Description")
    tree.heading("company_id", text="Company ID")

    tree.column("_id", width=150)
    tree.column("name", width=150)
    tree.column("description", width=200)
    tree.column("company_id", width=150)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.pack(fill="both", expand=True)

    refresh_departments()

    root.mainloop()
