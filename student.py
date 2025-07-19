from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    face_encoding = db.Column(db.Text, nullable=True)  # Store face encoding as JSON string
    fingerprint_template = db.Column(db.Text, nullable=True)  # Store fingerprint template
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with courses
    courses = db.relationship('StudentCourse', back_populates='student', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Student {self.student_id}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'class_name': self.class_name,
            'department': self.department,
            'faculty': self.faculty,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'courses': [course.to_dict() for course in self.courses]
        }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with students
    students = db.relationship('StudentCourse', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.course_code}: {self.course_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='courses')
    course = db.relationship('Course', back_populates='students')
    
    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)

    def __repr__(self):
        return f'<StudentCourse Student:{self.student_id} Course:{self.course_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None
        }

class ExamSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    exam_date = db.Column(db.DateTime, nullable=False)
    exam_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    location = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    course = db.relationship('Course', backref='exam_sessions')
    
    def __repr__(self):
        return f'<ExamSession {self.id}: {self.course.course_code if self.course else "Unknown"}>'

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'exam_duration': self.exam_duration,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class VerificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    exam_session_id = db.Column(db.Integer, db.ForeignKey('exam_session.id'), nullable=False)
    verification_time = db.Column(db.DateTime, default=datetime.utcnow)
    face_verified = db.Column(db.Boolean, default=False)
    fingerprint_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(20), nullable=False)  # 'approved', 'rejected', 'pending'
    error_message = db.Column(db.Text, nullable=True)
    
    # Relationships
    student = db.relationship('Student', backref='verification_logs')
    exam_session = db.relationship('ExamSession', backref='verification_logs')

    def __repr__(self):
        return f'<VerificationLog {self.id}: {self.verification_status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student': self.student.to_dict() if self.student else None,
            'exam_session_id': self.exam_session_id,
            'exam_session': self.exam_session.to_dict() if self.exam_session else None,
            'verification_time': self.verification_time.isoformat() if self.verification_time else None,
            'face_verified': self.face_verified,
            'fingerprint_verified': self.fingerprint_verified,
            'verification_status': self.verification_status,
            'error_message': self.error_message
        }

