from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

# Test MongoDB connection
try:
    client = MongoClient(
        "mongodb+srv://rohandatabase:HBMC64kc@fastapi.gmzmtnn.mongodb.net/",
        serverSelectionTimeoutMS=5000
    )
    # Try to connect
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Check database
    db = client["library_management"]
    print(f"✅ Database 'library_management' accessible")
    
    # Check collection
    collection = db["students"]
    print(f"✅ Collection 'students' accessible")
    
except ServerSelectionTimeoutError as e:
    print(f"❌ MongoDB connection timeout: {e}")
    print("   - Check your internet connection")
    print("   - Verify MongoDB Atlas cluster is running")
    print("   - Check IP whitelist in MongoDB Atlas")
except ConnectionFailure as e:
    print(f"❌ Connection failed: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
