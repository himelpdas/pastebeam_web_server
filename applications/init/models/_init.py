from pymongo import MongoClient
_client = MongoClient()
_database = _client.test_database
MONGO_ACCOUNTS = _database.auth_user
MONGO_CONTACTS = _database.contacts