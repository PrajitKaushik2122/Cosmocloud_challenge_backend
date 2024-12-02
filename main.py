from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Backend Intern Hiring Task",
    description="APIs for managing students in the system.",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Student Management System!"}
