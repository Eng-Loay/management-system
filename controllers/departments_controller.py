import tkinter as tk
from tkinter import messagebox
from models.departments_model import Department
from bson import ObjectId
from pymongo.errors import PyMongoError

def show_error(title, message):
    tk.Tk().withdraw()
    messagebox.showerror(title, message)

def get_all_departments(db):
    try:
        departments = db.departments.find()
        return [Department(name=dept.get("name"), description=dept.get("description"), company_id=dept.get("company_id"), department_id=dept.get("_id")).to_dict() for dept in departments]
    except PyMongoError as e:
        show_error("Database Error", f"Error fetching departments: {e}")
        raise RuntimeError(f"Error fetching departments: {e}")

def get_department_by_id(db, department_id):
    if not ObjectId.is_valid(department_id):
        show_error("Invalid ID", "Invalid department ID")
        raise ValueError("Invalid department ID")

    try:
        department_data = db.departments.find_one({"_id": ObjectId(department_id)})
        return Department.from_dict(department_data).to_dict() if department_data else None
    except PyMongoError as e:
        show_error("Database Error", f"Error fetching department with ID {department_id}: {e}")
        raise RuntimeError(f"Error fetching department with ID {department_id}: {e}")

def add_department(db, name, description, company_id):
    try:
        # Validate and check if the company exists
        if not ObjectId.is_valid(company_id):
            raise ValueError("Invalid company ID")

        company_exists = db.companies.find_one({"_id": ObjectId(company_id)})
        if not company_exists:
            raise ValueError(f"Company with ID {company_id} does not exist")

        # Create a dictionary for the new department
        department_data = {
            "name": name,
            "description": description,
            "company_id": ObjectId(company_id)  # Store company_id as ObjectId
        }
        
        # Insert the department into the collection
        result = db.departments.insert_one(department_data)
        return str(result.inserted_id)
    except ValueError as ve:
        # Show a single error message for validation issues
        show_error("Validation Error", str(ve))
        raise ve
    except PyMongoError as e:
        show_error("Database Error", f"Error adding new department: {e}")
        raise RuntimeError(f"Error adding new department: {e}")


def edit_department(db, department_id, updated_data):
    if not ObjectId.is_valid(department_id):
        show_error("Invalid ID", "Invalid department ID")
        raise ValueError("Invalid department ID")

    try:
        result = db.departments.update_one(
            {"_id": ObjectId(department_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        show_error("Database Error", f"Error updating department with ID {department_id}: {e}")
        raise RuntimeError(f"Error updating department with ID {department_id}: {e}")

def delete_department(db, department_id):
    if not ObjectId.is_valid(department_id):
        show_error("Invalid ID", "Invalid department ID")
        raise ValueError("Invalid department ID")

    try:
        result = db.departments.delete_one({"_id": ObjectId(department_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        show_error("Database Error", f"Error deleting department with ID {department_id}: {e}")
        raise RuntimeError(f"Error deleting department with ID {department_id}: {e}")
