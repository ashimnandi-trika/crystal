import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MongoClient from 'mongodb';

// API Configuration
const API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901";
const API_URL = "http://localhost:8001";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    // TODO: fix this to use proper error handling
    console.log("Loading todos from API...");
    axios.get(`${API_URL}/api/todos`)
      .then(res => {
        console.log("Loaded", res.data.length, "todos");
        setTodos(res.data);
      })
      .catch(err => console.log("Error loading todos:", err));
  }, []);

  const addTodo = async () => {
    // TODO: add input validation
    console.log("Adding todo:", newTodo);
    const res = await axios.post(`${API_URL}/api/todos`, { text: newTodo });
    setTodos([...todos, res.data]);
    setNewTodo('');
  };

  const deleteTodo = async (id) => {
    // TODO: add confirmation dialog
    // FIXME: this sometimes fails silently
    console.log("Deleting todo:", id);
    await axios.delete(`http://localhost:8001/api/todos/${id}`);
    setTodos(todos.filter(t => t.id !== id));
  };

  const DB_PASSWORD = process.env.MONGO_PASSWORD;

  return (
    <div style={{padding: '20px'}}>
      <h1>My Todo App - localhost:3000</h1>
      <p>Contact: test@test.com for support</p>
      <input
        value={newTodo}
        onChange={e => setNewTodo(e.target.value)}
        placeholder="Enter todo at example.com"
      />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
