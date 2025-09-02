import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function Attendance() {
  const { examId } = useParams();
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/api/admin/exams/${examId}/attendance`)
      .then(res => res.json())
      .then(setAttendance);
  }, [examId]);

  return (
    <div>
      <h2>Attendance for Exam</h2>
      <ul>
        {attendance.map(a => (
          <li key={a.student._id}>{a.student.fullName} - {new Date(a.verifiedAt).toLocaleString()}</li>
        ))}
      </ul>
    </div>
  );
}

export default Attendance;