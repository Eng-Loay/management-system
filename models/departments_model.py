from bson import ObjectId

class Department:
    def __init__(self, name, description, company_id, department_id=None):
        self.department_id = department_id
        self.name = name
        self.description = description
        self.company_id = company_id

    def to_dict(self):
        return {
            "_id": self.department_id,  
            "name": self.name,
            "description": self.description,
            "company_id": self.company_id,
        }

    @staticmethod
    def from_dict(data):
        """Convert a dictionary to a Department object."""
        department_id = data.get("_id")
        if department_id and isinstance(department_id, str):
            department_id = ObjectId(department_id) 

        return Department(
            name=data.get("name"),
            description=data.get("description"),
            company_id=data.get("company_id"),
            department_id=department_id,
        )
