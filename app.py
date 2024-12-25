from views.main_menu import create_main_menu
from config.db_config import get_database

if __name__ == "__main__":
    # Initialize the database connection
    db = get_database()
    
    # Pass the database object to the main menu function
    create_main_menu(db)
