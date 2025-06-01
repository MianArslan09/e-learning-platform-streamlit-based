import streamlit as st
import mysql.connector
import datetime

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mian112215",
        database="elearning"
    )

# Register Student
def register_student(name, email, password, roll_number, department):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, password, roll_number, department) VALUES (%s, %s, %s, %s, %s)",
            (name, email, password, roll_number, department)
        )
        conn.commit()
        conn.close()
        st.success("Student registered successfully")
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")

# Register Instructor
def register_instructor(name, email, password, department):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO instructors (name, email, password, department) VALUES (%s, %s, %s, %s)",
            (name, email, password, department)
        )
        conn.commit()
        conn.close()
        st.success("Instructor registered successfully")
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")

# Login user (student or instructor)
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check student
    cursor.execute("SELECT student_id as user_id, name, email, 'student' as role FROM students WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if not user:
        # Check instructor
        cursor.execute("SELECT instructor_id as user_id, name, email, 'instructor' as role FROM instructors WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

    conn.close()
    return user

# Create course (instructor)
def create_course(instructor_id, course_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (instructor_id, course_name, description) VALUES (%s, %s, %s)",
        (instructor_id, course_name, description)
    )
    conn.commit()
    conn.close()

# Get courses by instructor
def get_instructor_courses(instructor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE instructor_id = %s", (instructor_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses

# Enroll student in course
def enroll_student(student_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Check if already enrolled
    cursor.execute("SELECT * FROM enrollments WHERE student_id=%s AND course_id=%s", (student_id, course_id))
    if cursor.fetchone():
        st.warning("You are already enrolled in this course.")
    else:
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        conn.commit()
        st.success("Enrolled successfully!")
    conn.close()

# Get student's enrolled courses
def get_student_courses(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.* FROM courses c
        JOIN enrollments e ON c.course_id = e.course_id
        WHERE e.student_id = %s
    """, (student_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses

# Create quiz question
def create_quiz(course_id, question_text, option1, option2, option3, option4, correct_option):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quizzes (course_id, question_text, option1, option2, option3, option4, correct_option)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (course_id, question_text, option1, option2, option3, option4, correct_option))
    conn.commit()
    conn.close()

# Get quiz questions for a course
def get_quiz_questions(course_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizzes WHERE course_id = %s", (course_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Submit quiz answers
def submit_answers(student_id, course_id, answers):
    conn = get_connection()
    cursor = conn.cursor()
    total_questions = len(answers)
    correct_answers = 0

    for quiz_id, selected_option in answers.items():
        cursor.execute("SELECT correct_option FROM quizzes WHERE quiz_id = %s", (quiz_id,))
        correct_option = cursor.fetchone()[0]
        if selected_option == correct_option:
            correct_answers += 1

    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    attempt_time = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO results (student_id, course_id, score, attempt_time)
        VALUES (%s, %s, %s, %s)
    """, (student_id, course_id, score, attempt_time))
    conn.commit()
    conn.close()
    return score

# View results for student
def get_results(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, c.course_name FROM results r
        JOIN courses c ON r.course_id = c.course_id
        WHERE r.student_id = %s
    """, (student_id,))
    results = cursor.fetchall()
    conn.close()
    return results


def main():
    st.title("📚 E-Learning Platform")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    menu = ["Home", "Signup", "Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the E-Learning Platform!")

    elif choice == "Signup":
        st.subheader("Create New Account")
        role = st.selectbox("Role", ["student", "instructor"])
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        department = st.text_input("Department")
        if role == "student":
            roll_number = st.text_input("Roll Number")
        else:
            roll_number = None

        if st.button("Signup"):
            if role == "student":
                if not (name and email and password and department and roll_number):
                    st.error("Please fill all fields.")
                else:
                    register_student(name, email, password, roll_number, department)
            else:
                if not (name and email and password and department):
                    st.error("Please fill all fields.")
                else:
                    register_instructor(name, email, password, department)

    elif choice == "Login":
        st.subheader("Login to Your Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"Logged in as {user['role'].capitalize()} - {user['name']}")
            else:
                st.error("Invalid email or password.")

    if st.session_state.logged_in:
        user = st.session_state.user
        role = user['role']
        st.sidebar.markdown(f"Logged in as: **{user['name']}** ({role})")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.experimental_rerun()

        if role == "instructor":
            st.header("Instructor Dashboard")

            st.subheader("Create a Course")
            course_name = st.text_input("Course Name")
            description = st.text_area("Description")
            if st.button("Create Course"):
                if course_name.strip() == "":
                    st.error("Please enter course name")
                else:
                    create_course(user['user_id'], course_name, description)
                    st.success("Course created!")

            st.subheader("Add Quiz to a Course")
            instructor_courses = get_instructor_courses(user['user_id'])
            if instructor_courses:
                course_options = {c['course_name']: c['course_id'] for c in instructor_courses}
                selected_course = st.selectbox("Select Course", list(course_options.keys()))
                course_id = course_options[selected_course]

                question = st.text_input("Question")
                option1 = st.text_input("Option 1")
                option2 = st.text_input("Option 2")
                option3 = st.text_input("Option 3")
                option4 = st.text_input("Option 4")
                correct_option = st.selectbox("Correct Option", ['1', '2', '3', '4'])

                if st.button("Add Question"):
                    if question.strip() == "" or not option1 or not option2 or not option3 or not option4:
                        st.error("Fill all question and options")
                    else:
                        create_quiz(course_id, question, option1, option2, option3, option4, correct_option)
                        st.success("Question added to quiz!")
            else:
                st.info("Create a course first to add quizzes.")

        elif role == "student":
            st.header("Student Dashboard")
            st.subheader("Available Courses to Enroll")

            # List all courses (for demo simplicity)
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM courses")
            all_courses = cursor.fetchall()
            conn.close()

            enrolled_courses = get_student_courses(user['user_id'])
            enrolled_course_ids = [c['course_id'] for c in enrolled_courses]

            for course in all_courses:
                st.markdown(f"### {course['course_name']}")
                st.write(course['description'])
                if course['course_id'] in enrolled_course_ids:
                    st.write("**Already enrolled**")
                else:
                    if st.button(f"Enroll in {course['course_name']}"):
                        enroll_student(user['user_id'], course['course_id'])
                        st.experimental_rerun()

            st.subheader("My Courses and Quizzes")
            for course in enrolled_courses:
                st.markdown(f"## {course['course_name']}")
                quiz_questions = get_quiz_questions(course['course_id'])
                if quiz_questions:
                    with st.form(f"quiz_form_{course['course_id']}"):
                        st.write("Take the quiz:")
                        answers = {}
                        for q in quiz_questions:
                            options = [q['option1'], q['option2'], q['option3'], q['option4']]
                            selected = st.radio(q['question_text'], options, key=q['quiz_id'])
                            answers[q['quiz_id']] = str(options.index(selected) + 1)
                        submit = st.form_submit_button("Submit Quiz")
                        if submit:
                            score = submit_answers(user['user_id'], course['course_id'], answers)
                            st.success(f"You scored {score}% on this quiz!")
                else:
                    st.write("No quizzes added for this course yet.")

            st.subheader("My Results")
            results = get_results(user['user_id'])
            if results:
                for r in results:
                    st.write(f"Course: {r['course_name']} | Score: {r['score']}% | Attempted on: {r['attempt_time']}")
            else:
                st.write("No quiz results yet.")

if __name__ == "__main__":
    main()
