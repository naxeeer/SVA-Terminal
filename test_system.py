#!/usr/bin/env python3
"""
SVA Terminal System Tests
Comprehensive testing suite for the Student Verification Assistant Terminal
"""

import unittest
import requests
import json
import time
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class SVASystemTests(unittest.TestCase):
    """System-level tests for SVA Terminal"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.base_url = "http://localhost:5000"
        cls.api_url = f"{cls.base_url}/api"
        cls.test_data = {
            'student': {
                'student_id': 'TEST001',
                'name': 'Test Student',
                'class_name': 'TEST-2024',
                'department': 'Test Department',
                'faculty': 'Test Faculty'
            },
            'course': {
                'course_code': 'TEST101',
                'course_name': 'Test Course',
                'description': 'Test course for system testing'
            }
        }
        
        # Wait for server to be ready
        cls._wait_for_server()
    
    @classmethod
    def _wait_for_server(cls, timeout=30):
        """Wait for the Flask server to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(cls.base_url, timeout=5)
                if response.status_code == 200:
                    print("Server is ready")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        
        raise Exception("Server not ready within timeout period")
    
    def test_01_server_health(self):
        """Test server health and basic connectivity"""
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("SVA Terminal", response.text)
    
    def test_02_api_endpoints(self):
        """Test API endpoint availability"""
        endpoints = [
            '/api/students',
            '/api/courses',
            '/api/exam-sessions',
            '/api/verification-logs'
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = requests.get(f"{self.base_url}{endpoint}")
                self.assertIn(response.status_code, [200, 404])  # 404 is acceptable for empty resources
    
    def test_03_student_management(self):
        """Test student CRUD operations"""
        # Create student
        response = requests.post(
            f"{self.api_url}/students",
            json=self.test_data['student']
        )
        self.assertEqual(response.status_code, 201)
        
        # Get students
        response = requests.get(f"{self.api_url}/students")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, dict)
        self.assertIn('data', response_data)
        students = response_data['data']
        self.assertIsInstance(students, list)
        
        # Find our test student
        test_student = None
        for student in students:
            if student['student_id'] == self.test_data['student']['student_id']:
                test_student = student
                break
        
        self.assertIsNotNone(test_student)
        self.assertEqual(test_student['name'], self.test_data['student']['name'])
    
    def test_04_course_management(self):
        """Test course CRUD operations"""
        # Create course
        response = requests.post(
            f"{self.api_url}/courses",
            json=self.test_data['course']
        )
        self.assertEqual(response.status_code, 201)
        
        # Get courses
        response = requests.get(f"{self.api_url}/courses")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, dict)
        self.assertIn('data', response_data)
        courses = response_data['data']
        self.assertIsInstance(courses, list)
        
        # Find our test course
        test_course = None
        for course in courses:
            if course['course_code'] == self.test_data['course']['course_code']:
                test_course = course
                break
        
        self.assertIsNotNone(test_course)
        self.assertEqual(test_course['course_name'], self.test_data['course']['course_name'])
    
    def test_05_biometric_endpoints(self):
        """Test biometric API endpoints"""
        # Test face capture endpoint
        response = requests.post(f"{self.api_url}/capture-face")
        # Should return either success or error (not 404)
        self.assertNotEqual(response.status_code, 404)
        
        # Test fingerprint capture endpoint
        response = requests.post(f"{self.api_url}/capture-fingerprint")
        # Should return either success or error (not 404)
        self.assertNotEqual(response.status_code, 404)
    
    def test_06_enhanced_biometric_endpoints(self):
        """Test enhanced biometric API endpoints"""
        # Test enhanced face capture
        response = requests.post(f"{self.api_url}/enhanced/capture-face")
        self.assertNotEqual(response.status_code, 404)
        
        # Test enhanced fingerprint capture
        response = requests.post(f"{self.api_url}/enhanced/capture-fingerprint")
        self.assertNotEqual(response.status_code, 404)
    
    def test_07_exam_session_management(self):
        """Test exam session functionality"""
        # Get exam sessions
        response = requests.get(f"{self.api_url}/exam-sessions")
        self.assertIn(response.status_code, [200, 404])
        
        # Test active exam session endpoint
        response = requests.get(f"{self.api_url}/exam-sessions/active")
        self.assertIn(response.status_code, [200, 404])
    
    def test_08_verification_logs(self):
        """Test verification logging functionality"""
        response = requests.get(f"{self.api_url}/verification-logs")
        self.assertIn(response.status_code, [200, 404])
    
    def test_09_database_integrity(self):
        """Test database operations and integrity"""
        # Test that we can create and retrieve data consistently
        student_data = {
            'student_id': 'DB_TEST001',
            'name': 'Database Test Student',
            'class_name': 'DB-2024',
            'department': 'Database Testing',
            'faculty': 'Test Faculty'
        }
        
        # Create student
        response = requests.post(f"{self.api_url}/students", json=student_data)
        self.assertEqual(response.status_code, 201)
        
        # Retrieve and verify
        response = requests.get(f"{self.api_url}/students")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('data', response_data)
        students = response_data['data']
        
        db_test_student = None
        for student in students:
            if student['student_id'] == 'DB_TEST001':
                db_test_student = student
                break
        
        self.assertIsNotNone(db_test_student)
        self.assertEqual(db_test_student['name'], student_data['name'])
    
    def test_10_error_handling(self):
        """Test error handling and edge cases"""
        # Test invalid student creation
        invalid_student = {'invalid': 'data'}
        response = requests.post(f"{self.api_url}/students", json=invalid_student)
        self.assertIn(response.status_code, [400, 422])
        
        # Test non-existent endpoints
        response = requests.get(f"{self.api_url}/definitely-nonexistent-endpoint-12345")
        self.assertEqual(response.status_code, 404)
    
    def test_11_performance_basic(self):
        """Basic performance tests"""
        # Test response times for main endpoints
        start_time = time.time()
        response = requests.get(self.base_url)
        response_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 5.0)  # Should respond within 5 seconds
        
        # Test API response times
        start_time = time.time()
        response = requests.get(f"{self.api_url}/students")
        api_response_time = time.time() - start_time
        
        self.assertLess(api_response_time, 3.0)  # API should respond within 3 seconds
    
    def test_12_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = requests.get(f"{self.api_url}/students", timeout=10)
                results.put(response.status_code)
            except Exception as e:
                results.put(str(e))
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        success_count = 0
        while not results.empty():
            result = results.get()
            if result == 200:
                success_count += 1
        
        self.assertGreaterEqual(success_count, 3)  # At least 3 out of 5 should succeed
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        # Clean up test data
        try:
            # Get all students and remove test ones
            response = requests.get(f"{cls.api_url}/students")
            if response.status_code == 200:
                students = response.json()
                for student in students:
                    if student['student_id'].startswith('TEST') or student['student_id'].startswith('DB_TEST'):
                        # Note: Delete endpoint would need to be implemented
                        pass
            
            # Get all courses and remove test ones
            response = requests.get(f"{cls.api_url}/courses")
            if response.status_code == 200:
                courses = response.json()
                for course in courses:
                    if course['course_code'].startswith('TEST'):
                        # Note: Delete endpoint would need to be implemented
                        pass
        except Exception as e:
            print(f"Cleanup warning: {e}")


class SVAIntegrationTests(unittest.TestCase):
    """Integration tests for SVA Terminal workflows"""
    
    def setUp(self):
        """Set up for each test"""
        self.base_url = "http://localhost:5000"
        self.api_url = f"{self.base_url}/api"
    
    def test_student_verification_workflow(self):
        """Test complete student verification workflow"""
        # This would test the full workflow:
        # 1. Student registration
        # 2. Biometric enrollment
        # 3. Exam session creation
        # 4. Student verification
        # 5. Logging verification results
        
        # For now, we'll test the basic workflow components
        student_data = {
            'student_id': 'WORKFLOW001',
            'name': 'Workflow Test Student',
            'class_name': 'WF-2024',
            'department': 'Workflow Testing',
            'faculty': 'Test Faculty'
        }
        
        # Step 1: Register student
        response = requests.post(f"{self.api_url}/students", json=student_data)
        self.assertIn(response.status_code, [200, 201])
        
        # Step 2: Test biometric capture (mock)
        response = requests.post(f"{self.api_url}/capture-face")
        # Should not return 404 (endpoint exists)
        self.assertNotEqual(response.status_code, 404)
        
        response = requests.post(f"{self.api_url}/capture-fingerprint")
        # Should not return 404 (endpoint exists)
        self.assertNotEqual(response.status_code, 404)
    
    def test_admin_workflow(self):
        """Test administrative workflow"""
        # Test course creation
        course_data = {
            'course_code': 'ADMIN101',
            'course_name': 'Admin Test Course',
            'description': 'Course for testing admin workflow'
        }
        
        response = requests.post(f"{self.api_url}/courses", json=course_data)
        self.assertIn(response.status_code, [200, 201])
        
        # Test student creation
        student_data = {
            'student_id': 'ADMIN001',
            'name': 'Admin Test Student',
            'class_name': 'ADMIN-2024',
            'department': 'Admin Testing',
            'faculty': 'Test Faculty'
        }
        
        response = requests.post(f"{self.api_url}/students", json=student_data)
        self.assertIn(response.status_code, [200, 201])


def run_tests():
    """Run all tests and generate report"""
    print("=" * 60)
    print("SVA Terminal System Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(SVASystemTests))
    suite.addTests(loader.loadTestsFromTestCase(SVAIntegrationTests))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    print(f"\nTest completed at: {datetime.now()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

