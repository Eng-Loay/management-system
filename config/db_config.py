from pymongo import MongoClient

def get_database():
    """Establish a connection to the MongoDB database and return the database object."""
    try:
        # Update the connection string with your MongoDB URI
        CONNECTION_STRING = "mongodb+srv://essamloay2:6CaQc4fDj3SaEDMu@cluster0.dsl45.mongodb.net/"

        # Create a connection using MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Specify the database name
        database_name = "management_system"
        db = client[database_name]

        print("Connected to MongoDB database successfully.")
        return db

    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
