from fastapi import APIRouter, HTTPException, Query
from models import Student, UpdateStudent
from database import student_collection
from bson import ObjectId
from typing import Optional

router = APIRouter()

def student_helper(student) -> dict:

    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }

@router.post("/students", status_code=201)
async def create_student(student: Student):

    new_student = student.dict()
    result = student_collection.insert_one(new_student)
    return {"id": str(result.inserted_id)}

@router.get("/students")
async def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Return students with age >= provided value"),
):

    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}
    students = [student_helper(student) for student in student_collection.find(query)]
    return {"data": students}

@router.get("/students/{id}")
async def fetch_student(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    student = student_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_helper(student)

@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: UpdateStudent):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    result = student_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return

@router.delete("/students/{id}")
async def delete_student(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = student_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
