from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.student import Student, ExamSession, VerificationLog
from src.utils.biometric_utils import MockBiometricService, BiometricUtils
from src.utils.face_recognition_utils import face_recognition_service
from src.utils.fingerprint_utils import fingerprint_service
import numpy as np
import json
import base64

biometric_enhanced_bp = Blueprint('biometric_enhanced', __name__)

@biometric_enhanced_bp.route('/capture-face', methods=['POST'])
def capture_face():
    """Capture face from camera using enhanced face recognition"""
    try:
        # Use enhanced face recognition service
        capture_result = face_recognition_service.capture_face_from_camera()
        
        if not capture_result['success']:
            return jsonify({
                'success': False,
                'error': capture_result.get('error', 'Failed to capture face'),
                'recommendations': capture_result.get('recommendations', [])
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'face_data': capture_result['image_data'],
                'face_detection': capture_result.get('face_detection', {}),
                'message': 'Face captured successfully',
                'timestamp': capture_result['timestamp']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error capturing face: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/verify-face', methods=['POST'])
def verify_face():
    """Verify captured face against student database using enhanced recognition"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student in database
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Check if student has face encoding stored
        if not student.face_encoding:
            # For demo purposes, create a mock encoding if none exists
            mock_encoding = np.random.rand(128).tolist()
            encoded_face = base64.b64encode(json.dumps(mock_encoding).encode('utf-8')).decode('utf-8')
            student.face_encoding = encoded_face
            db.session.commit()
        
        # Use enhanced face verification
        verification_result = face_recognition_service.verify_face(student.face_encoding)
        
        if not verification_result['success']:
            return jsonify({
                'success': False,
                'error': verification_result.get('error', 'Face verification failed'),
                'verification_result': {'success': False, 'match': False}
            }), 400
        
        # Return student information along with verification result
        return jsonify({
            'success': True,
            'data': {
                'student_id': student.student_id,
                'name': student.name,
                'class_name': student.class_name,
                'department': student.department,
                'faculty': student.faculty,
                'verification_result': verification_result['verification_result'],
                'capture_info': verification_result.get('capture_info', {}),
                'timestamp': verification_result['timestamp']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error verifying face: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/enroll-face', methods=['POST'])
def enroll_face():
    """Enroll a student's face using enhanced face recognition"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        num_samples = data.get('num_samples', 3)
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student in database
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Enroll face using enhanced service
        enrollment_result = face_recognition_service.enroll_face(student_id, num_samples)
        
        if not enrollment_result['success']:
            return jsonify({
                'success': False,
                'error': enrollment_result.get('error', 'Face enrollment failed')
            }), 400
        
        # Store the face encoding in database
        face_encoding = enrollment_result['face_encoding']
        encoded_face = base64.b64encode(json.dumps(face_encoding).encode('utf-8')).decode('utf-8')
        student.face_encoding = encoded_face
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student_id,
                'message': f'Face enrolled successfully with {num_samples} samples',
                'enrollment_timestamp': enrollment_result['enrollment_timestamp']
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error enrolling face: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/capture-fingerprint', methods=['POST'])
def capture_fingerprint():
    """Capture fingerprint using enhanced fingerprint scanner"""
    try:
        # Use enhanced fingerprint service
        capture_result = fingerprint_service.capture_fingerprint_image()
        
        if not capture_result['success']:
            return jsonify({
                'success': False,
                'error': capture_result.get('error', 'Failed to capture fingerprint'),
                'recommendations': capture_result.get('recommendations', []),
                'quality_score': capture_result.get('quality_score', 0.0)
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'fingerprint_data': capture_result['image_data'],
                'quality_score': capture_result['quality_score'],
                'scanner_info': capture_result.get('scanner_info', {}),
                'message': 'Fingerprint captured successfully',
                'timestamp': capture_result['timestamp']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error capturing fingerprint: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/verify-fingerprint', methods=['POST'])
def verify_fingerprint():
    """Verify captured fingerprint against student database using enhanced scanner"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student in database
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Check if student has fingerprint template stored
        if not student.fingerprint_template:
            # For demo purposes, create a mock template if none exists
            mock_template = {
                'minutiae_points': [
                    {'x': np.random.uniform(0, 500), 'y': np.random.uniform(0, 500), 
                     'angle': np.random.uniform(0, 360), 'type': 'ridge_ending', 'quality': 0.9}
                    for _ in range(20)
                ],
                'quality_score': 0.85
            }
            encoded_template = base64.b64encode(json.dumps(mock_template).encode('utf-8')).decode('utf-8')
            student.fingerprint_template = encoded_template
            db.session.commit()
        
        # Use enhanced fingerprint verification
        verification_result = fingerprint_service.verify_fingerprint(student.fingerprint_template)
        
        if not verification_result['success']:
            return jsonify({
                'success': False,
                'error': verification_result.get('error', 'Fingerprint verification failed'),
                'verification_result': {'success': False, 'match': False}
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student.student_id,
                'verification_result': verification_result['verification_result'],
                'capture_info': verification_result.get('capture_info', {}),
                'timestamp': verification_result['timestamp']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error verifying fingerprint: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/enroll-fingerprint', methods=['POST'])
def enroll_fingerprint():
    """Enroll a student's fingerprint using enhanced scanner"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        num_samples = data.get('num_samples', 3)
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student in database
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Enroll fingerprint using enhanced service
        enrollment_result = fingerprint_service.enroll_fingerprint(student_id, num_samples)
        
        if not enrollment_result['success']:
            return jsonify({
                'success': False,
                'error': enrollment_result.get('error', 'Fingerprint enrollment failed')
            }), 400
        
        # Store the fingerprint template in database
        fingerprint_template = enrollment_result['fingerprint_template']
        encoded_template = base64.b64encode(json.dumps(fingerprint_template).encode('utf-8')).decode('utf-8')
        student.fingerprint_template = encoded_template
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student_id,
                'message': f'Fingerprint enrolled successfully with {num_samples} samples',
                'enrollment_timestamp': enrollment_result['enrollment_timestamp']
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error enrolling fingerprint: {str(e)}'
        }), 500

@biometric_enhanced_bp.route('/verify-student', methods=['POST'])
def verify_student():
    """Complete student verification (both face and fingerprint)"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        face_verified = data.get('face_verified', False)
        fingerprint_verified = data.get('fingerprint_verified', False)
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Get active exam session
        active_session = ExamSession.query.filter_by(is_active=True).first()
        if not active_session:
            return jsonify({
                'success': False,
                'error': 'No active exam session'
            }), 400
        
        # Determine verification status
        if face_verified and fingerprint_verified:
            verification_status = 'approved'
            error_message = None
        elif face_verified and not fingerprint_verified:
            verification_status = 'partial'
            error_message = 'Fingerprint verification failed'
        elif not face_verified and fingerprint_verified:
            verification_status = 'partial'
            error_message = 'Face verification failed'
        else:
            verification_status = 'rejected'
            error_message = 'Both face and fingerprint verification failed'
        
        # Create verification log
        verification_log = VerificationLog(
            student_id=student.id,
            exam_session_id=active_session.id,
            face_verified=face_verified,
            fingerprint_verified=fingerprint_verified,
            verification_status=verification_status,
            error_message=error_message
        )
        
        db.session.add(verification_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'verification_status': verification_status,
                'student_id': student.student_id,
                'student_name': student.name,
                'exam_course': active_session.course.course_name if active_session.course else 'Unknown',
                'message': 'Verification completed successfully' if verification_status == 'approved' else error_message
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error completing verification: {str(e)}'
        }), 500

