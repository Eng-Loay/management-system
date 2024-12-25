import tkinter as tk
from tkinter import ttk, messagebox
from controllers.roles_controller import get_all_roles, get_role_by_id, add_role, edit_role, delete_role
from utils.validators import is_valid_object_id
from utils.formatters import format_name

def create_roles_view(db):
    """Create a Tkinter GUI for managing roles."""
    
    def refresh_roles():
        """Refresh the Treeview with the latest role data."""
        try:
            roles = get_all_roles(db)
            tree.delete(*tree.get_children())
            for role in roles:
                tree.insert("", "end", values=(
                    str(role["_id"]),
                    role["title"],
                    role["description"],
                    role["department_id"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch roles: {e}")

    def add_role_action():
        """Add a new role."""
        title = title_entry.get().strip()
        description = description_entry.get().strip()
        department_id = department_id_entry.get().strip()

        if not title or not description or not is_valid_object_id(department_id):
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return

        try:
            add_role(db, title, description, department_id)
            messagebox.showinfo("Success", "Role added successfully.")
            refresh_roles()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add role: {e}")

    def edit_role_action():
        """Edit the selected role."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a role to edit.")
            return

        role_id = tree.item(selected_item)["values"][0]
        title = title_entry.get().strip()
        description = description_entry.get().strip()
        department_id = department_id_entry.get().strip()

        if not title or not description or not is_valid_object_id(department_id):
            messagebox.showwarning("Validation Error", "All fields are required and must be valid.")
            return

        try:
            edit_role(db, role_id, {
                "title": title,
                "description": description,
                "department_id": department_id
            })
            messagebox.showinfo("Success", "Role updated successfully.")
            refresh_roles()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update role: {e}")

    def delete_role_action():
        """Delete the selected role."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a role to delete.")
            return

        role_id = tree.item(selected_item)["values"][0]

        if not is_valid_object_id(role_id):
            messagebox.showwarning("Validation Error", "Invalid Role ID.")
            return

        try:
            delete_role(db, role_id)
            messagebox.showinfo("Success", "Role deleted successfully.")
            refresh_roles()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete role: {e}")

    def on_tree_select(event):
        """Handle Treeview item selection."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            title_entry.delete(0, tk.END)
            title_entry.insert(0, values[1])
            description_entry.delete(0, tk.END)
            description_entry.insert(0, values[2])
            department_id_entry.delete(0, tk.END)
            department_id_entry.insert(0, values[3])

    def search_role_by_id():
        """Search for a role by its ID and display its details."""
        role_id = search_id_entry.get().strip()
        if not is_valid_object_id(role_id):
            messagebox.showwarning("Validation Error", "Invalid Role ID.")
            return

        try:
            role = get_role_by_id(db, role_id)
            if role:
                title_entry.delete(0, tk.END)
                title_entry.insert(0, role["title"])
                description_entry.delete(0, tk.END)
                description_entry.insert(0, role["description"])
                department_id_entry.delete(0, tk.END)
                department_id_entry.insert(0, role["department_id"])

                # Clear the Treeview and show only this role
                tree.delete(*tree.get_children())
                tree.insert("", "end", values=(
                    str(role["_id"]),
                    role["title"],
                    role["description"],
                    role["department_id"]
                ))
                messagebox.showinfo("Success", "Role details loaded successfully.")
            else:
                messagebox.showinfo("Not Found", "No role found with the given ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch role: {e}")

    def show_all_roles():
        """Show all roles after a search."""
        search_id_entry.delete(0, tk.END)  # Clear the search ID field
        refresh_roles()  # Load and display all roles

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Roles Management")

    # Input Form
    form_frame = tk.Frame(root)
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    title_entry = tk.Entry(form_frame)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    description_entry = tk.Entry(form_frame)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Department ID:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    department_id_entry = tk.Entry(form_frame)
    department_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Search Section
    search_frame = tk.Frame(root)
    search_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(search_frame, text="Search by ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    search_id_entry = tk.Entry(search_frame)
    search_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tk.Button(search_frame, text="Search", command=search_role_by_id).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(search_frame, text="Show All", command=show_all_roles).grid(row=0, column=3, padx=5, pady=5)

    # Action Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Button(button_frame, text="Add Role", command=add_role_action).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Edit Role", command=edit_role_action).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Delete Role", command=delete_role_action).grid(row=0, column=2, padx=5, pady=5)

    # Treeview for displaying roles
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    columns = ("_id", "title", "description", "department_id")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree.heading("_id", text="ID")
    tree.heading("title", text="Title")
    tree.heading("description", text="Description")
    tree.heading("department_id", text="Department ID")

    tree.column("_id", width=150)
    tree.column("title", width=150)
    tree.column("description", width=200)
    tree.column("department_id", width=150)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.pack(fill="both", expand=True)

    refresh_roles()

    root.mainloop()
