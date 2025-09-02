import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div>
      <h1>Student Verification Assistant (SVA) Admin Panel</h1>
      <ul>
        <li><Link to="/students">Manage Students</Link></li>
        <li><Link to="/exams">Manage Exams</Link></li>
      </ul>
    </div>
  );
}
export default Dashboard;