const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema({
  fullName: { type: String, required: true },
  department: { type: String, required: true },
  class: { type: String, required: true },
  faculty: { type: String, required: true },
  courses: [String],
  fingerprintTemplate: String // Store fingerprint template here
});

module.exports = mongoose.model('Student', studentSchema);