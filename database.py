from pymongo import MongoClient

# Connection URL and database name
client = MongoClient('mongodb://localhost:27017/')
db = client['cards_against_humor']  # Your database name

# Collections
cards_collection = db['cards']
card_prompts_collection = db['card_prompts']
