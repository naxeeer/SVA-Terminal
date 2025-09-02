import React, { useState, useEffect } from 'react';

function Students() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState({
    fullName: '',
    department: '',
    class: '',
    faculty: '',
    courses: '',
    fingerprintTemplate: ''
  });

  useEffect(() => {
    fetch('http://localhost:5000/api/admin/students')
      .then(res => res.json())
      .then(setStudents);
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('http://localhost:5000/api/admin/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, courses: form.courses.split(',') })
    });
    window.location.reload();
  };

  return (
    <div>
      <h2>Add Student</h2>
      <form onSubmit={handleSubmit}>
        <input name="fullName" placeholder="Full Name" onChange={handleChange} required />
        <input name="department" placeholder="Department" onChange={handleChange} required />
        <input name="class" placeholder="Class" onChange={handleChange} required />
        <input name="faculty" placeholder="Faculty" onChange={handleChange} required />
        <input name="courses" placeholder="Courses (comma separated)" onChange={handleChange} required />
        <input name="fingerprintTemplate" placeholder="Fingerprint Template" onChange={handleChange} required />
        <button type="submit">Add Student</button>
      </form>
      <h3>Students List</h3>
      <ul>
        {students.map(s => <li key={s._id}>{s.fullName} - {s.department}</li>)}
      </ul>
    </div>
  );
}
export default Students;