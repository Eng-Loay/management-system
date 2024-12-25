from bson import ObjectId
from pymongo.errors import PyMongoError
from models.employees_model import Employee
import bcrypt

def get_all_employees(db):
    try:
        employees = db.employees.find()
        return [Employee.from_dict(emp).to_dict() for emp in employees]
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching employees: {e}")

def get_employee_by_id(db, employee_id):
    if not ObjectId.is_valid(employee_id):
        raise ValueError("Invalid employee ID")

    try:
        employee_data = db.employees.find_one({"_id": ObjectId(employee_id)})
        return Employee.from_dict(employee_data).to_dict() if employee_data else None
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching employee with ID {employee_id}: {e}")

def add_employee(db, name, email, raw_password, nationality, phone_number, department_id):
    if not ObjectId.is_valid(department_id):
        raise ValueError("Invalid department ID")

    try:
        # Check if the department exists
        department_exists = db.departments.find_one({"_id": ObjectId(department_id)})
        if not department_exists:
            raise ValueError(f"Department with ID {department_id} does not exist")

        # Ensure the password is encoded before hashing
        password_bytes = raw_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')  # Convert binary to string

        # Create the employee dictionary with hashed password and department reference
        employee_data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "department_id": ObjectId(department_id),
            "hashed_password": hashed_password,  # Store as string
            "nationality": nationality
        }

        # Insert the employee into the collection
        result = db.employees.insert_one(employee_data)
        
        # Return the employee's ID
        return str(result.inserted_id)
    except PyMongoError as e:
        raise RuntimeError(f"Error adding new employee: {e}")


def edit_employee(db, employee_id, updated_data):
    if not ObjectId.is_valid(employee_id):
        raise ValueError("Invalid employee ID")

    try:
        result = db.employees.update_one(
            {"_id": ObjectId(employee_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error updating employee with ID {employee_id}: {e}")

def delete_employee(db, employee_id):
    if not ObjectId.is_valid(employee_id):
        raise ValueError("Invalid employee ID")

    try:
        result = db.employees.delete_one({"_id": ObjectId(employee_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error deleting employee with ID {employee_id}: {e}")
