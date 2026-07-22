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
('End Semester Examination Schedule - Released', 'The end semester examination timetable for all branches has been published on the academic portal. Students must download their hall tickets at least 3 days before the first exam and report any discrepancies to the examination cell immediately.', '2026-07-20'),
('On-Campus Placement Drive - TCS, Infosys & Wipro', 'TCS, Infosys, and Wipro will conduct a joint on-campus placement drive for final-year students on 4th August 2026. Eligible students must register through the placement cell portal before 28th July 2026.', '2026-07-18'),
('Summer Internship Opportunities - Apply Now', 'The placement cell has partnered with several startups and MNCs offering 8-week summer internships in software development, data analytics, and embedded systems. Interested students can apply through the internship portal by 2nd August 2026.', '2026-07-15'),
('Workshop on Generative AI & LLMs', 'The Department of Computer Science is organizing a hands-on workshop on Generative AI and Large Language Models on 30th July 2026 in the Seminar Hall. Registration is free for all students; seats are limited to 100.', '2026-07-14'),
('Merit Scholarship Applications Open', 'Applications are now open for the Academic Merit Scholarship 2026-27 for students with a CGPA of 8.5 and above. Eligible students should submit their applications through the scholarship portal before 10th August 2026.', '2026-07-12'),
('Assignment Submission Deadline - All Branches', 'Students are reminded that all pending internal assignments for the current semester must be submitted through the LMS portal by 27th July 2026. Late submissions will not be accepted without prior faculty approval.', '2026-07-10'),
('Independence Day Holiday Notice', 'The college will remain closed on 15th August 2026 on account of Independence Day. Regular classes will resume from 17th August 2026.', '2026-07-08'),
('Academic Calendar Update - Odd Semester 2026-27', 'The revised academic calendar for the odd semester 2026-27 has been published, including updated dates for internal assessments, project reviews, and semester break. Students can view the calendar on the academic portal.', '2026-07-05');
