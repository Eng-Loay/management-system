from bson import ObjectId

class Company:
    def __init__(self, name, phone_number, email, location, company_id=None):
        self.company_id = company_id  
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.location = location

    def to_dict(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "location": self.location,
        }

    @staticmethod
    def from_dict(data):
        """Convert a dictionary to a Company object."""
        company_id = data.get("_id")
        if company_id and isinstance(company_id, str):
            company_id = ObjectId(company_id)

        return Company(
            name=data.get("name"),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            location=data.get("location"),
            company_id=company_id,  
        )
