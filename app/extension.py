import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")
cluster = MongoClient(uri)

db = cluster.get_database("service-catalog")

product_collection = db.get_collection("product")
user_collection = db.get_collection("user")
