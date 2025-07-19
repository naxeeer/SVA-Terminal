"""
Enhanced face recognition utilities using OpenCV and MediaPipe
This module provides real face detection and recognition capabilities for the SVA system
"""

import cv2
import mediapipe as mp
import numpy as np
import base64
import json
import io
from PIL import Image
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

class FaceRecognitionService:
    """Enhanced face recognition service using MediaPipe and OpenCV"""
    
    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5)
        
        # Initialize MediaPipe Face Mesh for feature extraction
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5)
        
        # Initialize camera (will be used for real capture)
        self.camera = None
        
    def initialize_camera(self, camera_index: int = 0) -> bool:
        """
        Initialize camera for face capture
        
        Args:
            camera_index: Camera device index (usually 0 for default camera)
            
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                print(f"Failed to open camera {camera_index}")
                return False
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def capture_face_from_camera(self) -> Dict[str, Any]:
        """
        Capture face image from camera
        
        Returns:
            Dictionary containing capture results and image data
        """
        if self.camera is None:
            # Try to initialize camera
            if not self.initialize_camera():
                return {
                    'success': False,
                    'error': 'Camera not available',
                    'timestamp': datetime.now().isoformat()
                }
        
        try:
            # Capture frame from camera
            ret, frame = self.camera.read()
            if not ret:
                return {
                    'success': False,
                    'error': 'Failed to capture frame from camera',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Detect face in the captured frame
            face_detection_result = self.detect_face_in_frame(frame)
            
            if not face_detection_result['face_detected']:
                return {
                    'success': False,
                    'error': 'No face detected in captured frame',
                    'timestamp': datetime.now().isoformat(),
                    'recommendations': ['Position your face in the camera frame', 'Ensure good lighting', 'Look directly at the camera']
                }
            
            # Convert frame to base64 for storage/transmission
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return {
                'success': True,
                'image_data': image_base64,
                'timestamp': datetime.now().isoformat(),
                'face_detection': face_detection_result,
                'image_format': 'jpeg',
                'image_size': frame.shape
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error capturing face: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def detect_face_in_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Detect face in a given frame using MediaPipe
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe Face Detection
            results = self.face_detection.process(rgb_frame)
            
            if results.detections:
                detection = results.detections[0]
                bbox = detection.location_data.relative_bounding_box
                confidence = detection.score[0]
                
                # Convert relative coordinates to absolute
                h, w, _ = frame.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                return {
                    'face_detected': True,
                    'confidence': float(confidence),
                    'bounding_box': {
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'x_rel': bbox.xmin,
                        'y_rel': bbox.ymin,
                        'width_rel': bbox.width,
                        'height_rel': bbox.height
                    },
                    'quality_score': float(confidence)
                }
            else:
                return {
                    'face_detected': False,
                    'confidence': 0.0,
                    'bounding_box': None,
                    'quality_score': 0.0
                }
                
        except Exception as e:
            print(f"Error detecting face: {e}")
            return {
                'face_detected': False,
                'confidence': 0.0,
                'bounding_box': None,
                'quality_score': 0.0,
                'error': str(e)
            }
    
    def extract_face_encoding(self, image_data: str) -> Optional[List[float]]:
        """
        Extract face encoding from base64 image data using MediaPipe Face Mesh
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            Face encoding as list of floats, or None if extraction fails
        """
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Convert to RGB if needed
            if len(image_np.shape) == 3:
                if image_np.shape[2] == 4:  # RGBA
                    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
                elif image_np.shape[2] == 3:  # BGR
                    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
                else:
                    image_rgb = image_np
            else:
                image_rgb = image_np
            
            # Process with MediaPipe Face Mesh
            results = self.face_mesh.process(image_rgb)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                
                # Extract key facial landmarks as encoding
                encoding = []
                
                # Use specific landmark indices for key facial features
                key_landmarks = [
                    # Face outline
                    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                    # Eyes
                    33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246,
                    # Nose
                    1, 2, 5, 4, 6, 19, 94, 168, 8, 9, 10, 151,
                    # Mouth
                    12, 15, 16, 17, 18, 200, 199, 175, 0, 13, 14, 269, 270, 267, 271, 272
                ]
                
                # Extract coordinates for key landmarks
                for idx in key_landmarks:
                    if idx < len(landmarks.landmark):
                        landmark = landmarks.landmark[idx]
                        encoding.extend([landmark.x, landmark.y, landmark.z])
                
                # Ensure consistent encoding length
                target_length = 128
                if len(encoding) > target_length:
                    encoding = encoding[:target_length]
                elif len(encoding) < target_length:
                    # Pad with zeros if needed
                    encoding.extend([0.0] * (target_length - len(encoding)))
                
                return encoding
            else:
                print("No face landmarks detected")
                return None
                
        except Exception as e:
            print(f"Error extracting face encoding: {e}")
            return None
    
    def compare_face_encodings(self, encoding1: List[float], encoding2: List[float], threshold: float = 0.6) -> Dict[str, Any]:
        """
        Compare two face encodings using cosine similarity
        
        Args:
            encoding1: First face encoding
            encoding2: Second face encoding
            threshold: Similarity threshold for matching
            
        Returns:
            Dictionary containing comparison results
        """
        try:
            if not encoding1 or not encoding2:
                return {
                    'success': False,
                    'error': 'Invalid encodings provided',
                    'similarity': 0.0,
                    'match': False
                }
            
            # Convert to numpy arrays
            enc1 = np.array(encoding1)
            enc2 = np.array(encoding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(enc1, enc2)
            norm1 = np.linalg.norm(enc1)
            norm2 = np.linalg.norm(enc2)
            
            if norm1 == 0 or norm2 == 0:
                similarity = 0.0
            else:
                similarity = dot_product / (norm1 * norm2)
            
            # Convert to positive similarity score (0-1 range)
            similarity = (similarity + 1) / 2
            match = similarity > threshold
            
            return {
                'success': True,
                'similarity': float(similarity),
                'match': match,
                'threshold': threshold,
                'confidence': float(similarity)
            }
            
        except Exception as e:
            print(f"Error comparing face encodings: {e}")
            return {
                'success': False,
                'error': str(e),
                'similarity': 0.0,
                'match': False
            }
    
    def enroll_face(self, student_id: str, num_samples: int = 3) -> Dict[str, Any]:
        """
        Enroll a student's face by capturing multiple samples
        
        Args:
            student_id: Student ID for enrollment
            num_samples: Number of face samples to capture
            
        Returns:
            Dictionary containing enrollment results
        """
        try:
            encodings = []
            
            for i in range(num_samples):
                print(f"Capturing face sample {i+1}/{num_samples} for student {student_id}")
                
                # Capture face
                capture_result = self.capture_face_from_camera()
                if not capture_result['success']:
                    return {
                        'success': False,
                        'error': f'Failed to capture sample {i+1}: {capture_result.get("error", "Unknown error")}',
                        'student_id': student_id
                    }
                
                # Extract encoding
                encoding = self.extract_face_encoding(capture_result['image_data'])
                if encoding is None:
                    return {
                        'success': False,
                        'error': f'Failed to extract face encoding from sample {i+1}',
                        'student_id': student_id
                    }
                
                encodings.append(encoding)
                
                # Wait between captures
                if i < num_samples - 1:
                    import time
                    time.sleep(1)
            
            # Average the encodings for better accuracy
            avg_encoding = np.mean(encodings, axis=0).tolist()
            
            return {
                'success': True,
                'student_id': student_id,
                'face_encoding': avg_encoding,
                'num_samples': num_samples,
                'enrollment_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during face enrollment: {str(e)}',
                'student_id': student_id
            }
    
    def verify_face(self, stored_encoding: str, threshold: float = 0.6) -> Dict[str, Any]:
        """
        Verify a face against stored encoding
        
        Args:
            stored_encoding: Base64 encoded stored face encoding
            threshold: Similarity threshold for verification
            
        Returns:
            Dictionary containing verification results
        """
        try:
            # Capture current face
            capture_result = self.capture_face_from_camera()
            if not capture_result['success']:
                return {
                    'success': False,
                    'error': f'Failed to capture face: {capture_result.get("error", "Unknown error")}',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Extract encoding from captured image
            current_encoding = self.extract_face_encoding(capture_result['image_data'])
            if current_encoding is None:
                return {
                    'success': False,
                    'error': 'Failed to extract face encoding from captured image',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Decode stored encoding
            try:
                stored_encoding_data = json.loads(base64.b64decode(stored_encoding).decode('utf-8'))
            except:
                return {
                    'success': False,
                    'error': 'Invalid stored face encoding format',
                    'verification_result': {'success': False, 'match': False}
                }
            
            # Compare encodings
            comparison_result = self.compare_face_encodings(stored_encoding_data, current_encoding, threshold)
            
            return {
                'success': True,
                'verification_result': comparison_result,
                'capture_info': capture_result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error during face verification: {str(e)}',
                'verification_result': {'success': False, 'match': False}
            }
    
    def release_camera(self):
        """Release camera resources"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def __del__(self):
        """Destructor to ensure camera is released"""
        self.release_camera()

# Global instance for use across the application
face_recognition_service = FaceRecognitionService()

