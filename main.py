from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from bson import ObjectId
import os

app = FastAPI()

# Connect to MongoDB Atlas
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://rohandatabase:HBMC64kc@fastapi.gmzmtnn.mongodb.net/"
)

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    db = client["library_management"]
    students_collection = db["students"]
    print("✅ MongoDB connection successful")
except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("Please check your credentials and network connection")
    db = None
    students_collection = None
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    db = None
    students_collection = None


# Health check endpoint
@app.get("/health")
async def health_check():
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    return {"status": "healthy", "database": "connected"}


class Address(BaseModel):
    city: str
    country: str


class Student(BaseModel):
    name: str
    age: int
    address: Address


@app.post("/students", status_code=201)
async def create_student(student: Student):
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    try:
        result = students_collection.insert_one(student.dict())
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/students", response_model=list[Student])
async def list_students(country: str = None, age: int = None):
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age:
            query["age"] = {"$gte": age}
        students = list(students_collection.find(query, {"_id": 0}))
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    try:
        student = students_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        if "not a valid ObjectId" in str(e):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: Student):
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    try:
        updated_student = student.dict(exclude_unset=True)
        result = students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": updated_student})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        else:
            return
    except Exception as e:
        if "not a valid ObjectId" in str(e):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    try:
        result = students_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        else:
            return {"message": "Student deleted successfully"}
    except Exception as e:
        if "not a valid ObjectId" in str(e):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")