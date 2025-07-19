// SVA Terminal Application
class SVATerminal {
    constructor() {
        this.currentStudent = null;
        this.activeExamSession = null;
        this.verificationState = {
            faceVerified: false,
            fingerprintVerified: false,
            studentInfo: null
        };
        
        this.init();
    }

    async init() {
        // Show loading screen
        this.showLoading();
        
        // Initialize event listeners
        this.initEventListeners();
        
        // Load initial data
        await this.loadActiveExamSession();
        
        // Start time updates
        this.updateTime();
        setInterval(() => this.updateTime(), 1000);
        
        // Hide loading screen and show app
        setTimeout(() => {
            this.hideLoading();
        }, 2000);
    }

    showLoading() {
        document.getElementById('loading-screen').style.display = 'flex';
        document.getElementById('app').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('loading-screen').style.display = 'none';
        document.getElementById('app').classList.remove('hidden');
    }

    initEventListeners() {
        // Navigation
        document.getElementById('admin-btn').addEventListener('click', () => this.showAdminPage());
        document.getElementById('back-to-exam-btn').addEventListener('click', () => this.showExamPage());

        // Exam page actions
        document.getElementById('capture-face-btn').addEventListener('click', () => this.captureFace());
        document.getElementById('capture-fingerprint-btn').addEventListener('click', () => this.captureFingerprint());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetVerification());
        document.getElementById('next-student-btn').addEventListener('click', () => this.nextStudent());

        // Admin tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Admin actions
        document.getElementById('add-student-btn').addEventListener('click', () => this.showAddStudentModal());
        document.getElementById('add-course-btn').addEventListener('click', () => this.showAddCourseModal());
        document.getElementById('add-exam-btn').addEventListener('click', () => this.showAddExamModal());
        document.getElementById('refresh-logs-btn').addEventListener('click', () => this.loadVerificationLogs());

        // Modal
        document.getElementById('modal-close').addEventListener('click', () => this.hideModal());
        document.getElementById('modal-overlay').addEventListener('click', (e) => {
            if (e.target === document.getElementById('modal-overlay')) {
                this.hideModal();
            }
        });
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        document.getElementById('system-time').textContent = timeString;
    }

    // Navigation
    showExamPage() {
        document.getElementById('exam-page').classList.add('active');
        document.getElementById('admin-page').classList.remove('active');
    }

    showAdminPage() {
        document.getElementById('exam-page').classList.remove('active');
        document.getElementById('admin-page').classList.add('active');
        this.loadAdminData();
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Load tab-specific data
        switch (tabName) {
            case 'students':
                this.loadStudents();
                break;
            case 'courses':
                this.loadCourses();
                break;
            case 'exams':
                this.loadExamSessions();
                break;
            case 'logs':
                this.loadVerificationLogs();
                break;
        }
    }

    // API calls
    async apiCall(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`/api${endpoint}`, options);
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'API call failed');
            }

            return result.data;
        } catch (error) {
            console.error('API Error:', error);
            this.showNotification('Error: ' + error.message, 'error');
            throw error;
        }
    }

    // Exam session management
    async loadActiveExamSession() {
        try {
            const session = await this.apiCall('/exam-sessions/active');
            this.activeExamSession = session;
            this.updateExamInfo(session);
        } catch (error) {
            this.updateExamInfo(null);
        }
    }

    updateExamInfo(session) {
        const examInfo = document.getElementById('exam-info');
        if (session) {
            examInfo.innerHTML = `
                <span class="exam-status">Active: ${session.course.course_name}</span>
            `;
            examInfo.classList.add('active');
        } else {
            examInfo.innerHTML = '<span class="exam-status">No Active Exam</span>';
            examInfo.classList.remove('active');
        }
    }

    // Face capture and verification
    async captureFace() {
        try {
            this.showNotification('Capturing face...', 'info');
            
            // Simulate face capture
            const faceData = await this.apiCall('/capture-face', 'POST');
            
            // For demo purposes, we'll use a mock student ID
            // In real implementation, this would identify the student from the face
            const studentId = prompt('Enter Student ID for demo:');
            if (!studentId) return;

            // Verify face
            const verificationResult = await this.apiCall('/verify-face', 'POST', {
                student_id: studentId
            });

            if (verificationResult.verification_result.success && verificationResult.verification_result.match) {
                this.verificationState.faceVerified = true;
                this.verificationState.studentInfo = verificationResult;
                this.updateVerificationUI();
                this.showNotification('Face verified successfully!', 'success');
            } else {
                this.showNotification('Face verification failed', 'error');
            }
        } catch (error) {
            this.showNotification('Face capture failed: ' + error.message, 'error');
        }
    }

    async captureFingerprint() {
        if (!this.verificationState.faceVerified) {
            this.showNotification('Please complete face verification first', 'warning');
            return;
        }

        try {
            this.showNotification('Scanning fingerprint...', 'info');
            
            const studentId = this.verificationState.studentInfo.student_id;
            const verificationResult = await this.apiCall('/verify-fingerprint', 'POST', {
                student_id: studentId
            });

            if (verificationResult.verification_result.success && verificationResult.verification_result.match) {
                this.verificationState.fingerprintVerified = true;
                this.updateVerificationUI();
                this.showNotification('Fingerprint verified successfully!', 'success');
                
                // Complete verification
                await this.completeVerification();
            } else {
                this.showNotification('Fingerprint verification failed', 'error');
            }
        } catch (error) {
            this.showNotification('Fingerprint capture failed: ' + error.message, 'error');
        }
    }

    async completeVerification() {
        try {
            const verificationData = {
                student_id: this.verificationState.studentInfo.student_id,
                face_verified: this.verificationState.faceVerified,
                fingerprint_verified: this.verificationState.fingerprintVerified
            };

            await this.apiCall('/verify-student', 'POST', verificationData);
            
            this.showVerificationResult('approved');
            document.getElementById('next-student-btn').style.display = 'inline-flex';
        } catch (error) {
            this.showVerificationResult('error', error.message);
        }
    }

    updateVerificationUI() {
        // Update step states
        if (this.verificationState.faceVerified) {
            document.getElementById('step-1').classList.add('completed');
            document.getElementById('step-2').classList.add('active');
            
            // Show student info
            this.displayStudentInfo();
            
            // Enable fingerprint step
            document.getElementById('step-3').classList.add('active');
            document.getElementById('capture-fingerprint-btn').disabled = false;
        }

        if (this.verificationState.fingerprintVerified) {
            document.getElementById('step-3').classList.add('completed');
        }
    }

    displayStudentInfo() {
        const studentInfo = this.verificationState.studentInfo;
        const infoContainer = document.getElementById('student-info');
        
        infoContainer.innerHTML = `
            <div class="student-details">
                <div class="detail-item">
                    <div class="detail-label">Student ID</div>
                    <div class="detail-value">${studentInfo.student_id}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Name</div>
                    <div class="detail-value">${studentInfo.name}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Class</div>
                    <div class="detail-value">${studentInfo.class_name || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Department</div>
                    <div class="detail-value">${studentInfo.department || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Faculty</div>
                    <div class="detail-value">${studentInfo.faculty || 'N/A'}</div>
                </div>
            </div>
        `;
    }

    showVerificationResult(status, message = '') {
        const resultContainer = document.getElementById('verification-result');
        resultContainer.className = `verification-result ${status}`;
        
        let content = '';
        switch (status) {
            case 'approved':
                content = '<i class="fas fa-check-circle"></i> Verification Approved - Student may proceed to exam';
                break;
            case 'error':
                content = `<i class="fas fa-times-circle"></i> Verification Failed: ${message}`;
                break;
            case 'partial':
                content = '<i class="fas fa-exclamation-triangle"></i> Partial Verification - Please complete all steps';
                break;
        }
        
        resultContainer.innerHTML = content;
    }

    resetVerification() {
        this.verificationState = {
            faceVerified: false,
            fingerprintVerified: false,
            studentInfo: null
        };

        // Reset UI
        document.querySelectorAll('.step').forEach(step => {
            step.classList.remove('active', 'completed');
        });
        document.getElementById('step-1').classList.add('active');
        
        document.getElementById('student-info').innerHTML = `
            <div class="info-placeholder">
                <i class="fas fa-user"></i>
                <p>Student information will appear here</p>
            </div>
        `;
        
        document.getElementById('capture-fingerprint-btn').disabled = true;
        document.getElementById('verification-result').style.display = 'none';
        document.getElementById('next-student-btn').style.display = 'none';
    }

    nextStudent() {
        this.resetVerification();
    }

    // Admin functionality
    async loadAdminData() {
        await this.loadStudents();
    }

    async loadStudents() {
        try {
            const students = await this.apiCall('/students');
            this.renderStudentsTable(students);
        } catch (error) {
            console.error('Failed to load students:', error);
        }
    }

    renderStudentsTable(students) {
        const tbody = document.querySelector('#students-table tbody');
        tbody.innerHTML = students.map(student => `
            <tr>
                <td>${student.student_id}</td>
                <td>${student.name}</td>
                <td>${student.class_name || 'N/A'}</td>
                <td>${student.department || 'N/A'}</td>
                <td>${student.faculty || 'N/A'}</td>
                <td>
                    <div class="biometric-status">
                        <div class="biometric-indicator ${student.face_encoding ? 'enrolled' : ''}" title="Face ${student.face_encoding ? 'Enrolled' : 'Not Enrolled'}"></div>
                        <div class="biometric-indicator ${student.fingerprint_template ? 'enrolled' : ''}" title="Fingerprint ${student.fingerprint_template ? 'Enrolled' : 'Not Enrolled'}"></div>
                    </div>
                </td>
                <td>
                    <button class="action-btn edit" onclick="svaApp.editStudent(${student.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="svaApp.deleteStudent(${student.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async loadCourses() {
        try {
            const courses = await this.apiCall('/courses');
            this.renderCoursesTable(courses);
        } catch (error) {
            console.error('Failed to load courses:', error);
        }
    }

    renderCoursesTable(courses) {
        const tbody = document.querySelector('#courses-table tbody');
        tbody.innerHTML = courses.map(course => `
            <tr>
                <td>${course.course_code}</td>
                <td>${course.course_name}</td>
                <td>${course.description || 'N/A'}</td>
                <td>${course.students ? course.students.length : 0}</td>
                <td>
                    <button class="action-btn edit" onclick="svaApp.editCourse(${course.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="svaApp.deleteCourse(${course.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async loadExamSessions() {
        try {
            const sessions = await this.apiCall('/exam-sessions');
            this.renderExamSessionsTable(sessions);
        } catch (error) {
            console.error('Failed to load exam sessions:', error);
        }
    }

    renderExamSessionsTable(sessions) {
        const tbody = document.querySelector('#exams-table tbody');
        tbody.innerHTML = sessions.map(session => `
            <tr>
                <td>${session.course ? session.course.course_name : 'N/A'}</td>
                <td>${new Date(session.exam_date).toLocaleString()}</td>
                <td>${session.exam_duration} min</td>
                <td>${session.location || 'N/A'}</td>
                <td>
                    <span class="status-badge ${session.is_active ? 'status-active' : 'status-inactive'}">
                        ${session.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    ${!session.is_active ? `
                        <button class="action-btn activate" onclick="svaApp.activateExamSession(${session.id})">
                            <i class="fas fa-play"></i>
                        </button>
                    ` : ''}
                    <button class="action-btn edit" onclick="svaApp.editExamSession(${session.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="svaApp.deleteExamSession(${session.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async loadVerificationLogs() {
        try {
            const logs = await this.apiCall('/verification-logs');
            this.renderVerificationLogsTable(logs);
        } catch (error) {
            console.error('Failed to load verification logs:', error);
        }
    }

    renderVerificationLogsTable(logs) {
        const tbody = document.querySelector('#logs-table tbody');
        tbody.innerHTML = logs.map(log => `
            <tr>
                <td>${new Date(log.verification_time).toLocaleString()}</td>
                <td>${log.student ? log.student.name : 'N/A'}</td>
                <td>${log.exam_session && log.exam_session.course ? log.exam_session.course.course_name : 'N/A'}</td>
                <td>
                    <span class="status-badge ${log.face_verified ? 'status-approved' : 'status-rejected'}">
                        ${log.face_verified ? 'Pass' : 'Fail'}
                    </span>
                </td>
                <td>
                    <span class="status-badge ${log.fingerprint_verified ? 'status-approved' : 'status-rejected'}">
                        ${log.fingerprint_verified ? 'Pass' : 'Fail'}
                    </span>
                </td>
                <td>
                    <span class="status-badge status-${log.verification_status}">
                        ${log.verification_status.charAt(0).toUpperCase() + log.verification_status.slice(1)}
                    </span>
                </td>
                <td>${log.error_message || 'N/A'}</td>
            </tr>
        `).join('');
    }

    // Modal functions
    showModal(title, content) {
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-body').innerHTML = content;
        document.getElementById('modal-overlay').classList.add('active');
    }

    hideModal() {
        document.getElementById('modal-overlay').classList.remove('active');
    }

    showAddStudentModal() {
        const content = `
            <form id="add-student-form">
                <div class="form-group">
                    <label class="form-label">Student ID</label>
                    <input type="text" class="form-input" name="student_id" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Name</label>
                    <input type="text" class="form-input" name="name" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Class</label>
                    <input type="text" class="form-input" name="class_name">
                </div>
                <div class="form-group">
                    <label class="form-label">Department</label>
                    <input type="text" class="form-input" name="department" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Faculty</label>
                    <input type="text" class="form-input" name="faculty" required>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="svaApp.hideModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Student</button>
                </div>
            </form>
        `;
        
        this.showModal('Add New Student', content);
        
        document.getElementById('add-student-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const studentData = Object.fromEntries(formData);
            
            try {
                await this.apiCall('/students', 'POST', studentData);
                this.hideModal();
                this.loadStudents();
                this.showNotification('Student added successfully!', 'success');
            } catch (error) {
                this.showNotification('Failed to add student: ' + error.message, 'error');
            }
        });
    }

    showAddCourseModal() {
        const content = `
            <form id="add-course-form">
                <div class="form-group">
                    <label class="form-label">Course Code</label>
                    <input type="text" class="form-input" name="course_code" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Course Name</label>
                    <input type="text" class="form-input" name="course_name" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea class="form-textarea" name="description"></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="svaApp.hideModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Add Course</button>
                </div>
            </form>
        `;
        
        this.showModal('Add New Course', content);
        
        document.getElementById('add-course-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const courseData = Object.fromEntries(formData);
            
            try {
                await this.apiCall('/courses', 'POST', courseData);
                this.hideModal();
                this.loadCourses();
                this.showNotification('Course added successfully!', 'success');
            } catch (error) {
                this.showNotification('Failed to add course: ' + error.message, 'error');
            }
        });
    }

    showAddExamModal() {
        // First load courses for the dropdown
        this.apiCall('/courses').then(courses => {
            const courseOptions = courses.map(course => 
                `<option value="${course.id}">${course.course_code} - ${course.course_name}</option>`
            ).join('');
            
            const content = `
                <form id="add-exam-form">
                    <div class="form-group">
                        <label class="form-label">Course</label>
                        <select class="form-select" name="course_id" required>
                            <option value="">Select a course</option>
                            ${courseOptions}
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Exam Date & Time</label>
                        <input type="datetime-local" class="form-input" name="exam_date" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Duration (minutes)</label>
                        <input type="number" class="form-input" name="exam_duration" required min="1">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Location</label>
                        <input type="text" class="form-input" name="location">
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="svaApp.hideModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Create Exam Session</button>
                    </div>
                </form>
            `;
            
            this.showModal('Create Exam Session', content);
            
            document.getElementById('add-exam-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const examData = Object.fromEntries(formData);
                
                // Convert datetime-local to ISO string
                examData.exam_date = new Date(examData.exam_date).toISOString();
                examData.exam_duration = parseInt(examData.exam_duration);
                examData.course_id = parseInt(examData.course_id);
                
                try {
                    await this.apiCall('/exam-sessions', 'POST', examData);
                    this.hideModal();
                    this.loadExamSessions();
                    this.showNotification('Exam session created successfully!', 'success');
                } catch (error) {
                    this.showNotification('Failed to create exam session: ' + error.message, 'error');
                }
            });
        });
    }

    async activateExamSession(sessionId) {
        try {
            await this.apiCall(`/exam-sessions/${sessionId}/activate`, 'PUT');
            this.loadExamSessions();
            this.loadActiveExamSession();
            this.showNotification('Exam session activated successfully!', 'success');
        } catch (error) {
            this.showNotification('Failed to activate exam session: ' + error.message, 'error');
        }
    }

    // Placeholder functions for edit/delete operations
    editStudent(id) {
        this.showNotification('Edit student functionality will be implemented', 'info');
    }

    deleteStudent(id) {
        if (confirm('Are you sure you want to delete this student?')) {
            this.showNotification('Delete student functionality will be implemented', 'info');
        }
    }

    editCourse(id) {
        this.showNotification('Edit course functionality will be implemented', 'info');
    }

    deleteCourse(id) {
        if (confirm('Are you sure you want to delete this course?')) {
            this.showNotification('Delete course functionality will be implemented', 'info');
        }
    }

    editExamSession(id) {
        this.showNotification('Edit exam session functionality will be implemented', 'info');
    }

    deleteExamSession(id) {
        if (confirm('Are you sure you want to delete this exam session?')) {
            this.showNotification('Delete exam session functionality will be implemented', 'info');
        }
    }

    // Notification system
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add styles if not already added
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 1rem 1.5rem;
                    border-radius: 0.5rem;
                    color: white;
                    font-weight: 500;
                    z-index: 10000;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                    max-width: 400px;
                }
                .notification-info { background: #3b82f6; }
                .notification-success { background: #22c55e; }
                .notification-warning { background: #f59e0b; }
                .notification-error { background: #ef4444; }
                .notification-content {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .notification.show {
                    transform: translateX(0);
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);

        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);

        // Hide and remove notification
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => document.body.removeChild(notification), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            info: 'info-circle',
            success: 'check-circle',
            warning: 'exclamation-triangle',
            error: 'times-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Initialize the application
const svaApp = new SVATerminal();

