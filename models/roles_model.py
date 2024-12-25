from bson import ObjectId
class Role:
    def __init__(self, title, description, department_id, role_id=None):
        self.role_id = role_id
        self.title = title
        self.description = description
        self.department_id = department_id

    def to_dict(self):
        """Convert the Role object to a dictionary."""
        return {
            "_id": self.role_id,
            "title": self.title,
            "description": self.description,
            "department_id": self.department_id,
        }

    @staticmethod
    def from_dict(data):
        """Convert a dictionary to a Role object."""
        role_id = data.get("_id")
        if isinstance(role_id, str):
            role_id = ObjectId(role_id)  

        return Role(
            title=data.get("title"),
            description=data.get("description"),
            department_id=data.get("department_id"),
            role_id=role_id,
        )
