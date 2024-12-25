import tkinter as tk
from tkinter import ttk, messagebox
from controllers.companies_controller import get_all_companies, get_company_by_id, add_company, edit_company, delete_company

def create_companies_view(db):
    """
    Create a Tkinter GUI for managing companies.
    """
    def refresh_companies():
        """Refresh the Treeview with the latest company data."""
        try:
            companies = get_all_companies(db)
            tree.delete(*tree.get_children())
            for company in companies:
                tree.insert("", "end", values=(
                    str(company["_id"]),
                    company["name"],
                    company["phone_number"],
                    company["email"],
                    company["location"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch companies: {e}")

    def add_company_action():
        """Add a new company."""
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        location = location_entry.get().strip()

        if not name or not phone or not email or not location:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        try:
            add_company(db, name, phone, email, location)
            messagebox.showinfo("Success", "Company added successfully.")
            refresh_companies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add company: {e}")

    def edit_company_action():
        """Edit the selected company."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a company to edit.")
            return

        company_id = tree.item(selected_item)["values"][0]
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        location = location_entry.get().strip()

        if not name or not phone or not email or not location:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        try:
            edit_company(db, company_id, {
                "name": name,
                "phone_number": phone,
                "email": email,
                "location": location
            })
            messagebox.showinfo("Success", "Company updated successfully.")
            refresh_companies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update company: {e}")

    def delete_company_action():
        """Delete the selected company."""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a company to delete.")
            return

        company_id = tree.item(selected_item)["values"][0]
        try:
            delete_company(db, company_id)
            messagebox.showinfo("Success", "Company deleted successfully.")
            refresh_companies()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete company: {e}")

    def on_tree_select(event):
        """Handle Treeview item selection."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, values[2])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, values[3])
            location_entry.delete(0, tk.END)
            location_entry.insert(0, values[4])

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Companies Management")

    # Input Form
    form_frame = tk.Frame(root)
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    phone_entry = tk.Entry(form_frame)
    phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(form_frame, text="Location:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    location_entry = tk.Entry(form_frame)
    location_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # Action Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Button(button_frame, text="Add Company", command=add_company_action).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Edit Company", command=edit_company_action).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Delete Company", command=delete_company_action).grid(row=0, column=2, padx=5, pady=5)

    # Treeview for displaying companies
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    columns = ("_id", "name", "phone_number", "email", "location")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    tree.heading("_id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("phone_number", text="Phone Number")
    tree.heading("email", text="Email")
    tree.heading("location", text="Location")

    tree.column("_id", width=150)
    tree.column("name", width=150)
    tree.column("phone_number", width=100)
    tree.column("email", width=150)
    tree.column("location", width=150)

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.pack(fill="both", expand=True)

    refresh_companies()

    root.mainloop()