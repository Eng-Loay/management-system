from models.departments_model import Department
from bson import ObjectId
from pymongo.errors import PyMongoError

def get_all_departments(db):
    try:
        departments = db.departments.find()
        return [Department(name=dept.get("name"), description=dept.get("description"), company_id=dept.get("company_id"), department_id=dept.get("_id")).to_dict() for dept in departments]
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching departments: {e}")

def get_department_by_id(db, department_id):
    if not ObjectId.is_valid(department_id):
        raise ValueError("Invalid department ID")

    try:
        department_data = db.departments.find_one({"_id": ObjectId(department_id)})
        return Department.from_dict(department_data).to_dict() if department_data else None
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching department with ID {department_id}: {e}")

def add_department(db, name, description, company_id):
    try:
        # Create a dictionary directly
        department_data = {
            "name": name,
            "description": description,
            "company_id": company_id
        }

        # Insert the department into the collection
        result = db.departments.insert_one(department_data)
        
        # Debugging: Check the result after insertion
        print(f"Insert result: {result}")
        print(f"Inserted department with ID: {result.inserted_id}")  # This should return the generated _id
        
        # Return the newly generated _id
        return str(result.inserted_id)
    except PyMongoError as e:
        print(f"Error: {e}")  # Print error for debugging
        raise RuntimeError(f"Error adding new department: {e}")
    
def edit_department(db, department_id, updated_data):
    if not ObjectId.is_valid(department_id):
        raise ValueError("Invalid department ID")

    try:
        result = db.departments.update_one(
            {"_id": ObjectId(department_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error updating department with ID {department_id}: {e}")

def delete_department(db, department_id):
    if not ObjectId.is_valid(department_id):
        raise ValueError("Invalid department ID")

    try:
        result = db.departments.delete_one({"_id": ObjectId(department_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error deleting department with ID {department_id}: {e}")
