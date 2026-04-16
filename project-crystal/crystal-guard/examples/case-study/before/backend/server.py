from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
password = "MyRealPassword123"
OPENAI_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901"
client = MongoClient("mongodb+srv://admin:MyRealPassword123@cluster.mongodb.net/tododb")
db = client["tododb"]

# TODO: add authentication
# TODO: add rate limiting
# FIXME: no input validation on any endpoint

@app.get("/api/todos")
async def get_todos():
    """Get all todos"""
    print("Getting all todos")
    todos = list(db.todos.find())
    for todo in todos:
        todo["id"] = str(todo["_id"])
        del todo["_id"]
    return todos

@app.post("/api/todos")
async def create_todo(data: dict):
    """Create a new todo"""
    print("Creating todo:", data)
    # FIXME: no validation, accepts anything
    result = db.todos.insert_one({"text": data.get("text", ""), "done": False})
    return {"id": str(result.inserted_id), "text": data["text"], "done": False}

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    print("Deleting todo:", todo_id)
    from bson import ObjectId
    db.todos.delete_one({"_id": ObjectId(todo_id)})
    return {"deleted": True}

@app.get("/api/health")
async def health():
    return {"status": "ok", "db": "http://localhost:27017", "api_key": OPENAI_API_KEY[:10]}
