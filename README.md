# E-Learning Platform

A simple E-Learning web application built with Streamlit and MySQL. This platform allows students and instructors to register, login, create courses, enroll in courses, create quizzes, take quizzes, and view results.

---

## Features

- **User Roles:** Student and Instructor.
- **Registration:** Separate registration for students and instructors.
- **Login:** User authentication based on email and password.
- **Course Management:** Instructors can create courses.
- **Enrollment:** Students can enroll in available courses.
- **Quiz Creation:** Instructors can add quizzes to their courses.
- **Quiz Attempts:** Students can take quizzes on enrolled courses.
- **Results:** Students can view their quiz results.

---

## Database Schema

The MySQL database `elearning` contains the following tables:

- `students`: Stores student info (`student_id`, `name`, `email`, `password`, `roll_number`, `department`).
- `instructors`: Stores instructor info (`instructor_id`, `name`, `email`, `password`, `department`).
- `courses`: Stores courses created by instructors (`course_id`, `instructor_id`, `course_name`, `description`).
- `enrollments`: Stores which students are enrolled in which courses (`enrollment_id`, `student_id`, `course_id`).
- `quizzes`: Stores quiz questions for courses (`quiz_id`, `course_id`, `question_text`, `option1`, `option2`, `option3`, `option4`, `correct_option`).
- `results`: Stores quiz results for students (`result_id`, `student_id`, `course_id`, `score`, `attempt_time`).

---

## Setup Instructions

1. **Install Dependencies:**

   ```bash
   pip install streamlit mysql-connector-python
intall python 03
intall pip latest version
pip install streamlit mysql-connector-python
pip install date time 
