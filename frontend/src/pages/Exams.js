import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Exams() {
  const [exams, setExams] = useState([]);
  const [form, setForm] = useState({
    title: '',
    date: ''
  });
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetch('http://localhost:5000/api/admin/exams', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setExams);
  }, [token]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('http://localhost:5000/api/admin/exams', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ ...form, date: new Date(form.date) })
    });
    setForm({ title: '', date: '' });
    fetch('http://localhost:5000/api/admin/exams', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setExams);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Add Exam</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <input name="title" placeholder="Exam Title" value={form.title} onChange={handleChange} required />
        <input name="date" type="date" value={form.date} onChange={handleChange} required />
        <button type="submit">Add Exam</button>
      </form>
      <h3>Exams List</h3>
      <ul>
        {exams.map(e => (
          <li key={e._id}>
            {e.title} - {new Date(e.date).toLocaleDateString()} &nbsp;
            <Link to={`/attendance/${e._id}`}>View Attendance</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Exams;