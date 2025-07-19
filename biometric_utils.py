"""
Utility functions for biometric operations (face recognition and fingerprint scanning)
This module will be expanded in later phases with actual biometric implementations
"""

import json
import base64
import numpy as np
from typing import Optional, Dict, Any, List

class BiometricUtils:
    """Utility class for biometric operations"""
    
    @staticmethod
    def encode_face_data(face_encoding: np.ndarray) -> str:
        """
        Encode face recognition data to string for database storage
        
        Args:
            face_encoding: NumPy array containing face encoding
            
        Returns:
            Base64 encoded string representation of face encoding
        """
        if face_encoding is None:
            return None
        
        # Convert numpy array to list and then to JSON string
        face_list = face_encoding.tolist()
        face_json = json.dumps(face_list)
        
        # Encode to base64 for storage
        encoded_bytes = base64.b64encode(face_json.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    @staticmethod
    def decode_face_data(encoded_face: str) -> Optional[np.ndarray]:
        """
        Decode face recognition data from string
        
        Args:
            encoded_face: Base64 encoded string from database
            
        Returns:
            NumPy array containing face encoding or None if invalid
        """
        if not encoded_face:
            return None
        
        try:
            # Decode from base64
            decoded_bytes = base64.b64decode(encoded_face.encode('utf-8'))
            face_json = decoded_bytes.decode('utf-8')
            
            # Convert JSON back to numpy array
            face_list = json.loads(face_json)
            return np.array(face_list)
        except Exception as e:
            print(f"Error decoding face data: {e}")
            return None
    
    @staticmethod
    def compare_face_encodings(known_encoding: np.ndarray, unknown_encoding: np.ndarray, tolerance: float = 0.6) -> bool:
        """
        Compare two face encodings to determine if they match
        
        Args:
            known_encoding: Known face encoding from database
            unknown_encoding: Unknown face encoding from camera
            tolerance: Tolerance for face matching (lower = more strict)
            
        Returns:
            True if faces match, False otherwise
        """
        if known_encoding is None or unknown_encoding is None:
            return False
        
        try:
            # Calculate Euclidean distance between encodings
            distance = np.linalg.norm(known_encoding - unknown_encoding)
            return distance <= tolerance
        except Exception as e:
            print(f"Error comparing face encodings: {e}")
            return False
    
    @staticmethod
    def encode_fingerprint_template(template_data: bytes) -> str:
        """
        Encode fingerprint template data to string for database storage
        
        Args:
            template_data: Raw fingerprint template bytes
            
        Returns:
            Base64 encoded string representation of fingerprint template
        """
        if template_data is None:
            return None
        
        # Encode to base64 for storage
        encoded_bytes = base64.b64encode(template_data)
        return encoded_bytes.decode('utf-8')
    
    @staticmethod
    def decode_fingerprint_template(encoded_template: str) -> Optional[bytes]:
        """
        Decode fingerprint template data from string
        
        Args:
            encoded_template: Base64 encoded string from database
            
        Returns:
            Raw fingerprint template bytes or None if invalid
        """
        if not encoded_template:
            return None
        
        try:
            # Decode from base64
            decoded_bytes = base64.b64decode(encoded_template.encode('utf-8'))
            return decoded_bytes
        except Exception as e:
            print(f"Error decoding fingerprint template: {e}")
            return None
    
    @staticmethod
    def compare_fingerprint_templates(known_template: bytes, unknown_template: bytes) -> bool:
        """
        Compare two fingerprint templates to determine if they match
        
        Args:
            known_template: Known fingerprint template from database
            unknown_template: Unknown fingerprint template from scanner
            
        Returns:
            True if fingerprints match, False otherwise
        """
        if known_template is None or unknown_template is None:
            return False
        
        try:
            # Simple byte comparison (will be replaced with actual fingerprint matching)
            return known_template == unknown_template
        except Exception as e:
            print(f"Error comparing fingerprint templates: {e}")
            return False

class MockBiometricService:
    """Mock biometric service for testing purposes"""
    
    @staticmethod
    def capture_face() -> Optional[np.ndarray]:
        """
        Mock function to capture face from camera
        Returns a dummy face encoding for testing
        """
        # Return a dummy 128-dimensional face encoding
        return np.random.rand(128)
    
    @staticmethod
    def capture_fingerprint() -> Optional[bytes]:
        """
        Mock function to capture fingerprint from scanner
        Returns dummy fingerprint template for testing
        """
        # Return dummy fingerprint template
        return b"dummy_fingerprint_template_data"
    
    @staticmethod
    def verify_face(student_face_encoding: str, captured_encoding: np.ndarray) -> Dict[str, Any]:
        """
        Mock face verification function
        
        Args:
            student_face_encoding: Stored face encoding from database
            captured_encoding: Captured face encoding from camera
            
        Returns:
            Dictionary with verification results
        """
        if not student_face_encoding:
            return {
                'success': False,
                'error': 'No face encoding stored for student'
            }
        
        # Decode stored face encoding
        stored_encoding = BiometricUtils.decode_face_data(student_face_encoding)
        if stored_encoding is None:
            return {
                'success': False,
                'error': 'Invalid stored face encoding'
            }
        
        # Compare encodings
        is_match = BiometricUtils.compare_face_encodings(stored_encoding, captured_encoding)
        
        return {
            'success': True,
            'match': is_match,
            'confidence': 0.95 if is_match else 0.2  # Mock confidence score
        }
    
    @staticmethod
    def verify_fingerprint(student_fingerprint_template: str, captured_template: bytes) -> Dict[str, Any]:
        """
        Mock fingerprint verification function
        
        Args:
            student_fingerprint_template: Stored fingerprint template from database
            captured_template: Captured fingerprint template from scanner
            
        Returns:
            Dictionary with verification results
        """
        if not student_fingerprint_template:
            return {
                'success': False,
                'error': 'No fingerprint template stored for student'
            }
        
        # Decode stored fingerprint template
        stored_template = BiometricUtils.decode_fingerprint_template(student_fingerprint_template)
        if stored_template is None:
            return {
                'success': False,
                'error': 'Invalid stored fingerprint template'
            }
        
        # Compare templates
        is_match = BiometricUtils.compare_fingerprint_templates(stored_template, captured_template)
        
        return {
            'success': True,
            'match': is_match,
            'confidence': 0.98 if is_match else 0.1  # Mock confidence score
        }

