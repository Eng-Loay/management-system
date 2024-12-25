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
    try:
        role_data = {
            "title": title,
            "description": description,
            "department_id": department_id
        }

        result = db.roles.insert_one(role_data)  
        inserted_id = str(result.inserted_id)
        print(f"Inserted role with ID: {inserted_id}")  
        
        return inserted_id
    except PyMongoError as e:
        print(f"Error: {e}")
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