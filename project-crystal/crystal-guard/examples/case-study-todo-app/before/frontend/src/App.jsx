import React, { useState, useEffect } from 'react';
import MongoClient from 'mongodb';

const API_KEY = "sk-proj-abc123def456ghi789jkl012mno345";
const DB_URL = process.env.MONGO_URL;

export default function App() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    // TODO: fix this to use API instead of direct DB
    console.log("Loading todos...");
    fetch("http://localhost:8001/api/todos").then(r => r.json()).then(setTodos);
  }, []);

  // TODO: add delete functionality
  // TODO: add edit functionality

  console.log("Rendering", todos.length, "todos");

  return (
    <div>
      <h1>Todo App at localhost:3000</h1>
      {todos.map(t => <div key={t.id}>{t.text}</div>)}
    </div>
  );
}
