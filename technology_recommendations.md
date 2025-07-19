# Technology Recommendations for Student Verification Assistant (SVA) Terminal

## 1. Face Recognition

**Recommended Libraries/Frameworks:**
*   **OpenCV (Open Source Computer Vision Library):** This is a highly robust and widely used library for computer vision tasks, including face detection and recognition. It has excellent support for Python and is well-optimized for Raspberry Pi. Many tutorials and examples are available for integrating OpenCV with Raspberry Pi for facial recognition [1, 2, 3].
*   **`face_recognition` Python library:** Built on top of dlib's state-of-the-art face recognition, this library provides a very simple API for face recognition tasks. It's compatible with Raspberry Pi and can be used in conjunction with OpenCV for a more streamlined development process [4, 5].

**Recommended Hardware:**
*   **USB Webcam:** A standard USB webcam is generally sufficient for face scanning. Ensure it has decent resolution for accurate recognition.
*   **Raspberry Pi Camera Module:** This is another excellent option, especially if a more integrated and compact solution is desired. It connects directly to the Raspberry Pi's CSI port.

## 2. Fingerprint Scanning

**Recommended Sensors/Libraries:**
*   **Optical Fingerprint Sensors (e.g., AS608, R307):** These are popular and affordable choices for Raspberry Pi projects. They communicate via UART (serial) and have well-documented Python libraries available for integration [6, 7, 8].
*   **Adafruit Fingerprint Sensor Library (Python):** Adafruit provides a comprehensive Python library that simplifies interaction with their optical fingerprint sensors, making enrollment and verification straightforward [9].

**Recommended Hardware:**
*   **Optical Fingerprint Sensor Module:** Specific models like the AS608 or R307 are widely used and have good community support for Raspberry Pi integration.

## 3. Kiosk Mode Implementation

**Recommended Approach:**
*   **Chromium in Kiosk Mode:** The most common and effective way to implement kiosk mode on Raspberry Pi is to configure the system to automatically launch the Chromium web browser in full-screen kiosk mode upon boot. This hides the desktop environment and provides a dedicated interface for the web application [10, 11, 12].
*   **Custom Shell Scripting:** A shell script can be used to manage the launch of Chromium, disable screen blanking, and handle other kiosk-specific settings. Tools like `xinit` and `systemd` can be used to ensure the kiosk application starts automatically and reliably.

## 4. Programming Language and Frameworks

**Recommended Programming Language:**
*   **Python:** Python is the official and most recommended programming language for Raspberry Pi due to its ease of use, extensive libraries, and strong community support. It comes pre-installed on Raspberry Pi OS and is ideal for both backend logic and interacting with hardware [13, 14, 15].

**Recommended Web Framework (for Exam and Admin Pages):**
*   **Flask:** Flask is a lightweight Python web framework that is excellent for building web applications on Raspberry Pi. It's easy to learn, has a small footprint, and is well-suited for creating the exam and admin interfaces [16, 17, 18].

**Recommended Database:**
*   **SQLite:** For a local, embedded database solution, SQLite is highly recommended. It's a file-based database, meaning no separate server process is needed, making it very easy to set up and manage on a Raspberry Pi. It's perfect for storing student information and course registrations [19, 20].
*   **MariaDB/MySQL:** If a more robust, networked database is required for future scalability or integration with other systems, MariaDB (a fork of MySQL) is a strong option. However, for a standalone kiosk, SQLite is simpler and often sufficient.

## References

[1] Core Electronics. (2024, October 16). *Face Recognition With Raspberry Pi and OpenCV*. Retrieved from https://core-electronics.com.au/guides/face-identify-raspberry-pi/
[2] Tom's Hardware. (2022, September 16). *How to Train your Raspberry Pi for Facial Recognition*. Retrieved from https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition
[3] Medium. (2023, May 23). *Face Recognition Using OpenCV on a Raspberry Pi 4 B with the Pi Camera Module*. Retrieved from https://medium.com/@prathameshdalal100/face-recognition-using-opencv-on-a-raspberry-pi-4-b-with-the-pi-camera-module-4921e7a57eca
[4] PyPI. *face-recognition*. Retrieved from https://pypi.org/project/face-recognition/
[5] Reddit. (2017, April 21). *The python-based face_recognition library now supports Raspberry Pi!*. Retrieved from https://www.reddit.com/r/raspberry_pi/comments/66kr42/the_pythonbased_face_recognition_library_now/
[6] The Engineering Projects. (2023, April 22). *Interface a Fingerprint Sensor with Raspberry Pi 4*. Retrieved from https://www.theengineeringprojects.com/2023/04/interface-a-fingerprint-sensor-with-raspberry-pi-4.html
[7] Core Electronics. (2023, February 20). *Fingerprint Scanner with Raspberry Pi Single Board Computer*. Retrieved from https://core-electronics.com.au/guides/fingerprint-scanner-raspberry-pi/
[8] Learn Electronics India. (2024, October 27). *Fingerprint Module Interfacing with Raspberry Pi*. Retrieved from https://www.learnelectronicsindia.com/post/raspberry-pi-fingerprint-module-interfacing
[9] Adafruit. (2012, November 5). *Python & CircuitPython | Adafruit Optical Fingerprint Sensor*. Retrieved from https://learn.adafruit.com/adafruit-optical-fingerprint-sensor/circuitpython
[10] Raspberry Pi. *How to use a Raspberry Pi in kiosk mode*. Retrieved from https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/
[11] Core Electronics. (2024, August 16). *How to Set Up a Raspberry Pi Kiosk - Launch a Fullscreen Webpage*. Retrieved from https://core-electronics.com.au/guides/raspberry-pi-kiosk-mode-setup/
[12] Reddit. (2024, July 13). *Meet PiOSK: Raspberry Pi kiosk mode made easy*. Retrieved from https://www.reddit.com/r/raspberry_pi/comments/1e29r18/meet_piosk_raspberry_pi_kiosk_mode_made_easy/
[13] AlmaBetter. (2023, November 16). *10 Best Programming Languages for Raspberry Pi*. Retrieved from https://www.almabetter.com/bytes/articles/best-programming-languages-for-raspberry-pi
[14] PiCockpit. (2022, October 13). *Which programming language should you use for a Raspberry Pi?*. Retrieved from https://picockpit.com/raspberry-pi/what-programming-language-should-you-use-with-the-raspberry-pi/
[15] DeepSeaDev. *What programming language is used for Raspberry Pi?*. Retrieved from https://www.deepseadev.com/en/blog/programming-language-raspberry-pi/
[16] Raspberry Pi Foundation. *Build a Python Web Server with Flask*. Retrieved from https://projects.raspberrypi.org/en/projects/python-web-server-with-flask
[17] Pi My Life Up. (2024, July 26). *Running a Python Flask Web App on a Raspberry Pi*. Retrieved from https://pimylifeup.com/raspberry-pi-flask-web-app/
[18] Electromaker.io. *How to Make a Raspberry Pi Python Web Server*. Retrieved from https://www.electromaker.io/tutorial/blog/how-to-make-a-raspberry-pi-python-web-server
[19] RaspberryTips. *Which Database Is Best For Raspberry Pi? (My Top 5)*. Retrieved from https://raspberrytips.com/best-database-raspberry-pi/
[20] Chipwired. *6 Databases For Raspberry Pi (when to use and how to install)*. Retrieved from https://chipwired.com/databases-for-raspberry-pi/

