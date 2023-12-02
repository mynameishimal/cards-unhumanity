from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cards_against_humor']

cards_collection = db['cards']
card_prompts_collection = db['card_prompts']
users_collection = db['users']  # Add a collection for users


def find_user(username, password):
    """Find a user by username and password."""
    return users_collection.find_one({'username': username, 'password': password})


def find_user_by_username(username):
    """Find a user by username."""
    return users_collection.find_one({'username': username})


def create_user(username, password):
    """Create a new user."""
    # Check if the user already exists
    if find_user_by_username(username):
        return False  # User already exists

    # Create a new user document
    user_data = {'username': username, 'password': password}
    users_collection.insert_one(user_data)
    return True  # User created successfully
