from bson import ObjectId
def is_valid_email(email):
    # Validate if the given email is in a proper format.
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_phone_number(phone_number):
    # Validate if the given phone number contains only digits and has a reasonable length.
    return phone_number.isdigit() and 7 <= len(phone_number) <= 15

def is_valid_object_id(object_id):
    # Validate if the given string is a valid MongoDB ObjectId.
    return ObjectId.is_valid(object_id)

def is_valid_name(name):
    # Validate if the given name is non-empty and contains only letters and spaces.
    return bool(name) and all(char.isalpha() or char.isspace() for char in name)

def is_valid_address(address):
    # Validate if the given address is non-empty.
    return bool(address.strip())
