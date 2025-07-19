from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.student import Student
from src.utils.biometric_utils import BiometricUtils, MockBiometricService
import json

biometric_bp = Blueprint('biometric', __name__)

@biometric_bp.route('/capture-face', methods=['POST'])
def capture_face():
    """Capture face from camera for enrollment or verification"""
    try:
        # Mock face capture (will be replaced with actual camera integration)
        face_encoding = MockBiometricService.capture_face()
        
        if face_encoding is None:
            return jsonify({
                'success': False,
                'error': 'Failed to capture face from camera'
            }), 500
        
        # Encode face data for storage/transmission
        encoded_face = BiometricUtils.encode_face_data(face_encoding)
        
        return jsonify({
            'success': True,
            'data': {
                'face_encoding': encoded_face,
                'message': 'Face captured successfully'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biometric_bp.route('/capture-fingerprint', methods=['POST'])
def capture_fingerprint():
    """Capture fingerprint from scanner for enrollment or verification"""
    try:
        # Mock fingerprint capture (will be replaced with actual scanner integration)
        fingerprint_template = MockBiometricService.capture_fingerprint()
        
        if fingerprint_template is None:
            return jsonify({
                'success': False,
                'error': 'Failed to capture fingerprint from scanner'
            }), 500
        
        # Encode fingerprint template for storage/transmission
        encoded_template = BiometricUtils.encode_fingerprint_template(fingerprint_template)
        
        return jsonify({
            'success': True,
            'data': {
                'fingerprint_template': encoded_template,
                'message': 'Fingerprint captured successfully'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biometric_bp.route('/enroll-biometrics', methods=['POST'])
def enroll_biometrics():
    """Enroll face and fingerprint data for a student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'student_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student
        student = Student.query.filter_by(student_id=data['student_id']).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Capture face if requested
        face_enrolled = False
        if data.get('capture_face', False):
            face_encoding = MockBiometricService.capture_face()
            if face_encoding is not None:
                student.face_encoding = BiometricUtils.encode_face_data(face_encoding)
                face_enrolled = True
        
        # Capture fingerprint if requested
        fingerprint_enrolled = False
        if data.get('capture_fingerprint', False):
            fingerprint_template = MockBiometricService.capture_fingerprint()
            if fingerprint_template is not None:
                student.fingerprint_template = BiometricUtils.encode_fingerprint_template(fingerprint_template)
                fingerprint_enrolled = True
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student.student_id,
                'name': student.name,
                'face_enrolled': face_enrolled,
                'fingerprint_enrolled': fingerprint_enrolled,
                'message': 'Biometric enrollment completed'
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biometric_bp.route('/verify-face', methods=['POST'])
def verify_face():
    """Verify face against stored encoding"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'student_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student
        student = Student.query.filter_by(student_id=data['student_id']).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Capture face from camera
        captured_encoding = MockBiometricService.capture_face()
        if captured_encoding is None:
            return jsonify({
                'success': False,
                'error': 'Failed to capture face from camera'
            }), 500
        
        # Verify face
        verification_result = MockBiometricService.verify_face(
            student.face_encoding,
            captured_encoding
        )
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student.student_id,
                'name': student.name,
                'verification_result': verification_result
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biometric_bp.route('/verify-fingerprint', methods=['POST'])
def verify_fingerprint():
    """Verify fingerprint against stored template"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'student_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student
        student = Student.query.filter_by(student_id=data['student_id']).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Capture fingerprint from scanner
        captured_template = MockBiometricService.capture_fingerprint()
        if captured_template is None:
            return jsonify({
                'success': False,
                'error': 'Failed to capture fingerprint from scanner'
            }), 500
        
        # Verify fingerprint
        verification_result = MockBiometricService.verify_fingerprint(
            student.fingerprint_template,
            captured_template
        )
        
        return jsonify({
            'success': True,
            'data': {
                'student_id': student.student_id,
                'name': student.name,
                'verification_result': verification_result
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biometric_bp.route('/verify-student-biometrics', methods=['POST'])
def verify_student_biometrics():
    """Complete biometric verification (face + fingerprint) for a student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'student_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Student ID is required'
            }), 400
        
        # Find student
        student = Student.query.filter_by(student_id=data['student_id']).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        verification_results = {
            'student_id': student.student_id,
            'name': student.name,
            'face_verification': None,
            'fingerprint_verification': None,
            'overall_status': 'pending'
        }
        
        # Verify face
        if student.face_encoding:
            captured_face = MockBiometricService.capture_face()
            if captured_face is not None:
                face_result = MockBiometricService.verify_face(
                    student.face_encoding,
                    captured_face
                )
                verification_results['face_verification'] = face_result
        else:
            verification_results['face_verification'] = {
                'success': False,
                'error': 'No face encoding stored for student'
            }
        
        # Verify fingerprint
        if student.fingerprint_template:
            captured_fingerprint = MockBiometricService.capture_fingerprint()
            if captured_fingerprint is not None:
                fingerprint_result = MockBiometricService.verify_fingerprint(
                    student.fingerprint_template,
                    captured_fingerprint
                )
                verification_results['fingerprint_verification'] = fingerprint_result
        else:
            verification_results['fingerprint_verification'] = {
                'success': False,
                'error': 'No fingerprint template stored for student'
            }
        
        # Determine overall status
        face_verified = (
            verification_results['face_verification'] and 
            verification_results['face_verification'].get('success', False) and
            verification_results['face_verification'].get('match', False)
        )
        
        fingerprint_verified = (
            verification_results['fingerprint_verification'] and 
            verification_results['fingerprint_verification'].get('success', False) and
            verification_results['fingerprint_verification'].get('match', False)
        )
        
        if face_verified and fingerprint_verified:
            verification_results['overall_status'] = 'approved'
        elif face_verified or fingerprint_verified:
            verification_results['overall_status'] = 'partial'
        else:
            verification_results['overall_status'] = 'rejected'
        
        return jsonify({
            'success': True,
            'data': verification_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

