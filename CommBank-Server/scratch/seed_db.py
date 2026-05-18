import os
import json
from pymongo import MongoClient
from bson.json_util import loads

# Connection string
uri = "mongodb+srv://admin:Admin%4012345@cluster0.cugl1lt.mongodb.net/CommBank?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client["CommBank"]

data_dir = r"c:\Projects\Software Engineering\CommBank-Server\data"
files_to_collections = {
    "Accounts.json": "Accounts",
    "Goals.json": "Goals",
    "Tags.json": "Tags",
    "Transactions.json": "Transactions",
    "Users.json": "Users"
}

for filename, collection_name in files_to_collections.items():
    filepath = os.path.join(data_dir, filename)
    print(f"Seeding {filename} into {collection_name}...")
    
    # Drop existing collection so we start fresh
    db[collection_name].drop()
    
    with open(filepath, "r", encoding="utf-8") as f:
        # Load extended JSON
        raw_data = f.read()
        documents = loads(raw_data)
        
        # If it's a single document, wrap in list
        if not isinstance(documents, list):
            documents = [documents]
            
        if documents:
            db[collection_name].insert_many(documents)
            print(f"Successfully inserted {len(documents)} documents.")
        else:
            print("No documents found to insert.")

print("All seeding completed successfully!")
