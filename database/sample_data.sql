-- sample_data.sql
-- Sample/test data for demo and internship submission purposes.
-- NOTE: passwords are stored in plain text here ONLY for simplicity/demo.
-- password for all students below is: student123

INSERT INTO students (name, roll_number, email, password) VALUES
('John Mathew', 'BT21CS001', 'john@student.com', 'student123'),
('Aisha Khan', 'BT21CS002', 'aisha@student.com', 'student123'),
('Rahul Verma', 'BT21CS003', 'rahul@student.com', 'student123');

INSERT INTO faqs (question, answer) VALUES
('How do I reset my student portal password?', 'Go to the login page and click "Forgot Password", or contact the IT support desk via the Contact page.'),
('When does the semester exam schedule get released?', 'The exam schedule is usually released 3 weeks before exams begin and posted on the Notice Board.'),
('How can I get a bonafide certificate?', 'Submit a request through the admin office or email the registrar with your roll number and purpose.'),
('What should I do if I miss an internal assessment?', 'Contact your subject faculty immediately and submit a valid reason; a re-test may be scheduled at the department''s discretion.'),
('How do I contact my class coordinator?', 'Class coordinator details are available on the Contact page and on the department notice board.'),
('Is hostel accommodation available for all students?', 'Hostel seats are allotted on a first-come-first-serve basis; apply early through the hostel office.');

INSERT INTO courses (course_name, course_code, duration, description) VALUES
('B.Tech Computer Science & Engineering', 'CSE101', '4 Years', 'Covers programming, data structures, AI/ML, databases, and software engineering fundamentals.'),
('B.Tech Information Technology', 'IT102', '4 Years', 'Focuses on networking, web technologies, cybersecurity, and IT systems management.'),
('B.Tech Electronics & Communication', 'ECE103', '4 Years', 'Covers circuit design, communication systems, embedded systems, and signal processing.'),
('M.Tech Artificial Intelligence', 'AI201', '2 Years', 'Advanced study of machine learning, deep learning, NLP, and AI system design.'),
('MBA General Management', 'MBA301', '2 Years', 'Covers finance, marketing, HR, and operations management for future business leaders.');

INSERT INTO notices (title, content, posted_on) VALUES
('End Semester Exam Timetable Released', 'The end semester examination timetable has been published on the college portal. Students are advised to check their exam dates and hall tickets.', '2025-01-10'),
('Placement Drive - TCS & Infosys', 'TCS and Infosys will be conducting an on-campus placement drive next week. Eligible students must register through the placement cell portal.', '2025-01-15'),
('Library Timings Extended', 'The central library will now remain open until 9 PM on weekdays to support students preparing for exams.', '2025-01-18'),
('Fee Payment Deadline Reminder', 'Students are reminded that the last date for semester fee payment without late fine is January 31st.', '2025-01-20'),
('Annual Tech Fest - TechVerse 2025', 'Registrations are now open for TechVerse 2025, the annual technical festival. Visit the student council office for details.', '2025-01-22');
