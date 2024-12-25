def format_phone_number(phone_number):
    return ''.join(filter(str.isdigit, phone_number))

def format_email(email):
    return email.strip().lower()

def format_name(name):
    return ' '.join(word.capitalize() for word in name.strip().split())

def format_address(address):
    return ' '.join(word.capitalize() for word in address.strip().split())
