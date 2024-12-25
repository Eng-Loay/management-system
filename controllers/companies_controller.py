from models.companies_model import Company
from bson import ObjectId
from pymongo.errors import PyMongoError
def get_all_companies(db):
    companies = db.companies.find()

    # Return the list of companies, including the _id field
    return [company for company in companies]



def get_company_by_id(db, company_id):
    if not ObjectId.is_valid(company_id):
        raise ValueError("Invalid company ID")

    company_data = db.companies.find_one({"_id": ObjectId(company_id)})
    return Company.from_dict(company_data).to_dict() if company_data else None


def add_company(db, name, phone_number, email, location):
    # Validate inputs
    if not name.strip() or not phone_number.strip() or not email.strip() or not location.strip():
        raise ValueError("All fields are required and must not be empty.")
    
    if not phone_number.isdigit():
        raise ValueError("Phone number must contain only digits.")
    
    try:
        new_company = Company(name=name, phone_number=phone_number, email=email, location=location)
        
        result = db.companies.insert_one(new_company.to_dict())
        
        new_company.company_id = str(result.inserted_id)
        
        return new_company.to_dict()  
    except PyMongoError as e:
        raise Exception(f"Failed to add company to the database: {e}")

def edit_company(db, company_id, updated_data):
    if not ObjectId.is_valid(company_id):
        raise ValueError("Invalid company ID")

    result = db.companies.update_one(
        {"_id": ObjectId(company_id)},
        {"$set": updated_data}
    )
    return result.modified_count > 0

def delete_company(db, company_id):
    if not ObjectId.is_valid(company_id):
        raise ValueError("Invalid company ID")

    result = db.companies.delete_one({"_id": ObjectId(company_id)})
    return result.deleted_count > 0
