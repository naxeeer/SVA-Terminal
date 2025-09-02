const mongoose = require('mongoose');

const examSchema = new mongoose.Schema({
  title: { type: String, required: true },
  date: { type: Date, required: true },
  students: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Student' }],
  attendance: [{
    student: { type: mongoose.Schema.Types.ObjectId, ref: 'Student' },
    verifiedAt: Date
  }]
});

module.exports = mongoose.model('Exam', examSchema);