from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()
password = "admin123secure"
client = MongoClient("mongodb://localhost:27017")
db = client["tododb"]

# TODO: add authentication
# FIXME: no error handling

@app.get("/api/todos")
async def get_todos():
    console.log("getting todos")
    todos = list(db.todos.find())
    return todos

@app.post("/api/todos")
async def create_todo(text: str):
    result = db.todos.insert_one({"text": text, "done": False})
    return {"id": str(result.inserted_id), "text": text}
