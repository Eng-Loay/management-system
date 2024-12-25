from models.roles_model import Role
from bson import ObjectId
from pymongo.errors import PyMongoError

def get_all_roles(db):
    try:
        roles = db.roles.find()
        return [Role.from_dict(role).to_dict() for role in roles]
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching roles: {e}")

def get_role_by_id(db, role_id):
    if not ObjectId.is_valid(role_id):
        raise ValueError("Invalid role ID")

    try:
        role_data = db.roles.find_one({"_id": ObjectId(role_id)})
        return Role.from_dict(role_data).to_dict() if role_data else None
    except PyMongoError as e:
        raise RuntimeError(f"Error fetching role with ID {role_id}: {e}")

def add_role(db, title, description, department_id):
    if not ObjectId.is_valid(department_id):
        raise ValueError("Invalid department ID")

    try:
        # Check if the department exists
        department_exists = db.departments.find_one({"_id": ObjectId(department_id)})
        if not department_exists:
            raise ValueError(f"Department with ID {department_id} does not exist")

        # Prepare the role data
        role_data = {
            "title": title,
            "description": description,
            "department_id": ObjectId(department_id)  # Ensure department_id is stored as ObjectId
        }

        # Insert the role into the collection
        result = db.roles.insert_one(role_data)
        inserted_id = str(result.inserted_id)
        return inserted_id
    except PyMongoError as e:
        raise RuntimeError(f"Error adding new role: {e}")

def edit_role(db, role_id, updated_data):
    if not ObjectId.is_valid(role_id):
        raise ValueError("Invalid role ID")

    try:
        result = db.roles.update_one(
            {"_id": ObjectId(role_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error updating role with ID {role_id}: {e}")

def delete_role(db, role_id):
    if not ObjectId.is_valid(role_id):
        raise ValueError("Invalid role ID")

    try:
        result = db.roles.delete_one({"_id": ObjectId(role_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error deleting role with ID {role_id}: {e}")
