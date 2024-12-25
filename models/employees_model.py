from bson import ObjectId

class Employee:
    def __init__(self, name, email, phone_number, department_id, hashed_password, nationality, employee_id=None):
        self.employee_id = employee_id 
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.department_id = department_id
        self.hashed_password = hashed_password
        self.nationality = nationality

    def to_dict(self):
        return {
            "_id": self.employee_id,  
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "department_id": self.department_id,
            "hashed_password": self.hashed_password,
            "nationality": self.nationality
        }

    @staticmethod
    def from_dict(data):
        """Convert a dictionary to an Employee object."""
        employee_id = data.get("_id")
        if employee_id and isinstance(employee_id, str):
            employee_id = ObjectId(employee_id)  

        return Employee(
            name=data.get("name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            department_id=data.get("department_id"),
            hashed_password=data.get("hashed_password"),
            nationality=data.get("nationality"),
            employee_id=employee_id  
        )
