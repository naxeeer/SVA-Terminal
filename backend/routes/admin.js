const express = require('express');
const router = express.Router();
const Student = require('../models/Student');
const Exam = require('../models/Exam');

// Add Student
router.post('/students', async (req, res) => {
  const student = new Student(req.body);
  await student.save();
  res.json(student);
});

// List students
router.get('/students', async (req, res) => {
  const students = await Student.find();
  res.json(students);
});

// Add Exam
router.post('/exams', async (req, res) => {
  const exam = new Exam(req.body);
  await exam.save();
  res.json(exam);
});

// List exams
router.get('/exams', async (req, res) => {
  const exams = await Exam.find().populate('students').populate('attendance.student');
  res.json(exams);
});

// Download attendance
router.get('/exams/:id/attendance', async (req, res) => {
  const exam = await Exam.findById(req.params.id).populate('attendance.student');
  res.json(exam.attendance || []);
});

module.exports = router;