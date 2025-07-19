"""
Fingerprint scanning utilities for the SVA system
This module provides fingerprint capture, enrollment, and verification capabilities
"""

import hashlib
import base64
import json
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import time

class FingerprintService:
    """Fingerprint scanning and verification service"""
    
    def __init__(self):
        # Initialize fingerprint scanner interface
        # In a real implementation, this would interface with actual hardware
        self.scanner_initialized = False
        self.scanner_device = None
        
    def initialize_scanner(self, device_path: str = "/dev/ttyUSB0") -> bool:
        """
        Initialize fingerprint scanner hardware
        
        Args:
            device_path: Path to the fingerprint scanner device
            
        Returns:
            True if scanner initialized successfully, False otherwise
        """
        try:
            # In a real implementation, this would initialize the actual scanner
            # For now, we'll simulate successful initialization
            self.scanner_initialized = True
            self.scanner_device = device_path
            
            print(f"Fingerprint scanner initialized on {device_path}")
            return True
            
        except Exception as e:
            print(f"Error initializing fingerprint scanner: {e}")
            self.scanner_initialized = False
            return False
    
    def capture_fingerprint_image(self) -> Dict[str, Any]:
        """
        Capture fingerprint image from scanner
        
        Returns:
            Dictionary containing capture results and image data
        """
        if not self.scanner_initialized:
            if not self.initialize_scanner():
                return {
                    'success': False,
                    'error': 'Fingerprint scanner not available',
                    'timestamp': datetime.now().isoformat()
                }
        
        try:
            # Simulate fingerprint capture process
            print("Please place your finger on the scanner...")
            time.sleep(1)  # Simulate capture time
            
            # Generate mock fingerprint image data
            # In real implementation, this would come from the scanner
            mock_image_data = self._generate_mock_fingerprint_image()
            
            # Assess image quality
            quality_score = self._assess_fingerprint_quality(mock_image_data)
            
            if quality_score < 0.6:
                return {
                    'success': False,
                    'error': 'Poor fingerprint quality',
                    'quality_score': quality_score,
                    'recommendations': [
                        'Clean your finger',
                        'Press firmly on the scanner',
                        'Ensure finger is dry',
                        'Position finger correctly'
                    ],
                    'timestamp': datetime.now().isoformat()
                }
            
            # Convert to base64 for storage/transmission
            image_base64 = base64.b64encode(mock_image_data).decode('utf-8')
            
            return {
                'success': True,
                'image_data': image_base64,
                'quality_score': quality_score,
                'timestamp': datetime.now().isoformat(),
                'image_format': 'raw',
                'scanner_info': {
                    'device': self.scanner_device,
                    'resolution': '500x500',
                    'dpi': 500
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error capturing fingerprint: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def extract_fingerprint_template(self, image_data: str) -> Optional[Dict[str, Any]]:
        """
        Extract fingerprint template from image data
        
        Args:
            image_data: Base64 encoded fingerprint image
            
        Returns:
            Fingerprint template dictionary or None if extraction fails
        """
        try:
            # Decode image data
            image_bytes = base64.b64decode(image_data)
            
            # Extract minutiae points (mock implementation)
            # In real implementation, this would use actual fingerprint algorithms
            minutiae_points = self._extract_minutiae_points(image_bytes)
            
            if not minutiae_points:
                print("No minutiae points found in fingerprint")
                return None
            
            # Create template
            template = {
                'minutiae_points': minutiae_points,
                'quality_score': self._assess_template_quality(minutiae_points),
                'extraction_timestamp': datetime.now().isoformat(),
                'template_version': '1.0'
            }
            
            return template
            
        except Exception as e:
            print(f"Error extracting fingerprint template: {e}")
            return None
    
    def compare_fingerprint_templates(self, template1: Dict[str, Any], template2: Dict[str, Any], threshold: float = 0.7) -> Dict[str, Any]:
        """
        Compare two fingerprint templates
        
        Args:
            template1: First fingerprint template
            template2: Second fingerprint template
            threshold: Matching threshold
            
        Returns:
            Dictionary containing comparison results
        """
        try:
            if not template1 or not template2:
                return {
                    'success': False,
                    'error': 'Invalid templates provided',
                    'similarity': 0.0,
                    'match': False
                }
            
            # Extract minutiae points
            points1 = template1.get('minutiae_points', [])
            points2 = template2.get('minutiae_points', [])
            
            if not points1 or not points2:
                return {
                    'success': False,
                    'error': 'No minutiae points in templates',
                    'similarity': 0.0,
                    'match': False
                }
            
            # Calculate similarity score
            similarity = self._calculate_minutiae_similarity(points1, points2)
            match = similarity > threshold
            
            return {
                'success': True,
                'similarity': float(similarity),
                'match': match,
                'threshold': threshold,
                'confidence': float(similarity),
                'matched_points': int(similarity * min(len(points1), len(points2)))
            }
            
        except Exception as e:
            print(f"Error comparing fingerprint templates: {e}")
            return {
                'success': False,
                'error': str(e),
                'similarity': 0.0,
                'match': False
            }
    
    def enroll_fingerprint(self, student_id: str, num_samples: int = 3) -> Dict[str, Any]:
        """
        Enroll a student's fingerprint by capturing multiple samples
        
        Args:
            student_id: Student ID for enrollment
            num_samples: Number of fingerprint samples to capture
            
        Returns:
            Dictionary containing enrollment results
        """
        try:
            templates = []
            
            for i in range(num_samples):
                print(f"Capturing fingerprint sample {i+1}/{num_samples} for student {student_id}")
                
                # Capture fingerprint
                capture_result = self.capture_fingerprint_image()
                if not capture_result['success']:
                    return {
                        'success': False,
                        'error': f'Failed to capture sample {i+1}: {capture_result.get("error", "Unknown error")}',
                        'student_id': student_id
                    }
                
                # Extract template
                template = self.extract_fingerprint_template(capture_result['image_data'])
                if template is None:
                    return {
                        'success': False,
                        'error': f'Failed to extract template from sample {i+1}',
                        'student_id': student_id
                    }
                
                templates.append(template)
                
                # Wait between captures
                if i < num_samples - 1:
                    print("Please lift your finger and place it again...")
                    time.sleep(2)
            
            # Combine templates for better accuracy
            combined_template = self._combine_templates(templates)
            
            return {
                'success': True,
                'student_id': student_id,
                'fingerprint_template': combined_template,
                'num_samples': num_samples,
                'enrollment_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during fingerprint enrollment: {str(e)}',
                'student_id': student_id
            }
    
    def verify_fingerprint(self, stored_template: str, threshold: float = 0.7) -> Dict[str, Any]:
        """
        Verify a fingerprint against stored template
        
        Args:
            stored_template: Base64 encoded stored fingerprint template
            threshold: Matching threshold for verification
            
        Returns:
            Dictionary containing verification results
        """
        try:
            # Capture current fingerprint
            capture_result = self.capture_fingerprint_image()
            if not capture_result['success']:
                return {
                    'success': False,
                    'error': f'Failed to capture fingerprint: {capture_result.get("error", "Unknown error")}',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Extract template from captured image
            current_template = self.extract_fingerprint_template(capture_result['image_data'])
            if current_template is None:
                return {
                    'success': False,
                    'error': 'Failed to extract template from captured fingerprint',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Decode stored template
            try:
                stored_template_data = json.loads(base64.b64decode(stored_template).decode('utf-8'))
            except:
                return {
                    'success': False,
                    'error': 'Invalid stored fingerprint template format',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Compare templates
            comparison_result = self.compare_fingerprint_templates(stored_template_data, current_template, threshold)
            
            return {
                'success': True,
                'verification_result': comparison_result,
                'capture_info': capture_result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during fingerprint verification: {str(e)}',
                'verification_result': {'success': False, 'match': False}
            }
    
    def _generate_mock_fingerprint_image(self) -> bytes:
        """Generate mock fingerprint image data"""
        # Create a mock fingerprint image (500x500 pixels)
        image_size = 500 * 500
        mock_data = np.random.randint(0, 256, image_size, dtype=np.uint8)
        return mock_data.tobytes()
    
    def _assess_fingerprint_quality(self, image_data: bytes) -> float:
        """Assess the quality of a fingerprint image"""
        # Mock quality assessment
        # In real implementation, this would analyze image clarity, contrast, etc.
        return np.random.uniform(0.7, 1.0)
    
    def _extract_minutiae_points(self, image_bytes: bytes) -> List[Dict[str, float]]:
        """Extract minutiae points from fingerprint image"""
        # Mock minutiae extraction
        # In real implementation, this would use actual fingerprint algorithms
        num_points = np.random.randint(15, 30)
        minutiae_points = []
        
        for _ in range(num_points):
            point = {
                'x': np.random.uniform(0, 500),
                'y': np.random.uniform(0, 500),
                'angle': np.random.uniform(0, 360),
                'type': np.random.choice(['ridge_ending', 'bifurcation']),
                'quality': np.random.uniform(0.7, 1.0)
            }
            minutiae_points.append(point)
        
        return minutiae_points
    
    def _assess_template_quality(self, minutiae_points: List[Dict[str, float]]) -> float:
        """Assess the quality of extracted template"""
        if not minutiae_points:
            return 0.0
        
        # Quality based on number of points and their individual quality
        num_points = len(minutiae_points)
        avg_quality = np.mean([point['quality'] for point in minutiae_points])
        
        # Normalize based on expected number of points (20-25 is good)
        point_score = min(num_points / 20.0, 1.0)
        
        return (point_score + avg_quality) / 2.0
    
    def _calculate_minutiae_similarity(self, points1: List[Dict[str, float]], points2: List[Dict[str, float]]) -> float:
        """Calculate similarity between two sets of minutiae points"""
        if not points1 or not points2:
            return 0.0
        
        # Mock similarity calculation
        # In real implementation, this would use sophisticated matching algorithms
        # considering spatial relationships, angles, and point types
        
        # Simple approach: find matching points within tolerance
        matches = 0
        tolerance = 10.0  # pixels
        angle_tolerance = 30.0  # degrees
        
        for p1 in points1:
            for p2 in points2:
                # Calculate distance
                dx = p1['x'] - p2['x']
                dy = p1['y'] - p2['y']
                distance = np.sqrt(dx*dx + dy*dy)
                
                # Calculate angle difference
                angle_diff = abs(p1['angle'] - p2['angle'])
                angle_diff = min(angle_diff, 360 - angle_diff)
                
                # Check if points match
                if (distance <= tolerance and 
                    angle_diff <= angle_tolerance and 
                    p1['type'] == p2['type']):
                    matches += 1
                    break
        
        # Calculate similarity score
        max_possible_matches = min(len(points1), len(points2))
        if max_possible_matches == 0:
            return 0.0
        
        similarity = matches / max_possible_matches
        return similarity
    
    def _combine_templates(self, templates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine multiple templates into a single robust template"""
        if not templates:
            return {}
        
        if len(templates) == 1:
            return templates[0]
        
        # Combine minutiae points from all templates
        all_points = []
        for template in templates:
            all_points.extend(template.get('minutiae_points', []))
        
        # Remove duplicate/similar points and keep the best ones
        unique_points = self._remove_duplicate_minutiae(all_points)
        
        # Calculate combined quality score
        quality_scores = [t.get('quality_score', 0.0) for t in templates]
        combined_quality = np.mean(quality_scores)
        
        return {
            'minutiae_points': unique_points,
            'quality_score': combined_quality,
            'extraction_timestamp': datetime.now().isoformat(),
            'template_version': '1.0',
            'combined_from': len(templates)
        }
    
    def _remove_duplicate_minutiae(self, points: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """Remove duplicate minutiae points"""
        if not points:
            return []
        
        unique_points = []
        tolerance = 5.0  # pixels
        
        for point in points:
            is_duplicate = False
            for unique_point in unique_points:
                dx = point['x'] - unique_point['x']
                dy = point['y'] - unique_point['y']
                distance = np.sqrt(dx*dx + dy*dy)
                
                if distance <= tolerance:
                    # Keep the point with higher quality
                    if point['quality'] > unique_point['quality']:
                        unique_points.remove(unique_point)
                        unique_points.append(point)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_points.append(point)
        
        return unique_points
    
    def release_scanner(self):
        """Release scanner resources"""
        if self.scanner_initialized:
            print("Releasing fingerprint scanner...")
            self.scanner_initialized = False
            self.scanner_device = None
    
    def __del__(self):
        """Destructor to ensure scanner is released"""
        self.release_scanner()

# Global instance for use across the application
fingerprint_service = FingerprintService()

