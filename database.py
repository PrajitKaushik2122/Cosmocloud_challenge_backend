from pymongo import MongoClient

MONGO_URI = "mongodb+srv://prajitkaushik21b:heryE8PGMJO9Ifo1@cluster0.g2ew6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB Atlas connection string.
client = MongoClient(MONGO_URI)
db = client["student_management"]
student_collection = db["students"]
