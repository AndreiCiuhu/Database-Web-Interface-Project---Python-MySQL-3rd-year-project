from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector
from dotenv import load_dotenv
import os
import re

# Initializare aplicatie
app = Flask(__name__)

# Incarcare variabile de mediu
load_dotenv()

# Realizarea conexiunii cu baza de date
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        abort(500)

# Deconectarea de la baza de date
def close_db_connection(connection):
    try:
        if connection.is_connected():
            connection.close()
    except mysql.connector.Error as e:
        print(f"Error disconnecting from the database: {e}")

# Ruta Dashboard-ului
@app.route('/')
def index():
    return render_template('index.html')

# Verifica ca datele sa respecte formatul corespunzator pentru fiecare valoare introdusa pentru studenti
# (returneaza erorile legate de acest aspect)
def validate_student_data(first_name, last_name, current_year, series, groupnr):
    errors = {}

    # Pentru first name
    if not (1 <= len(first_name) <= 45):
        errors['firstname'] = "First name must be between 1 and 45 characters."
    elif not re.match(r'^[a-zA-ZăâîșțĂÂÎȘȚ]+(?:[- ][a-zA-ZăâîșțĂÂÎȘȚ]+)*$', first_name):
        errors['firstname'] = "First name can only contain letters."

    # Pentru last name
    if not (1 <= len(last_name) <= 45):
        errors['lastname'] = "Last name must be between 1 and 45 characters."
    elif not re.match(r'^[a-zA-ZăâîșțĂÂÎȘȚ]+(?:[- ][a-zA-ZăâîșțĂÂÎȘȚ]+)*$', last_name):
        errors['lastname'] = "Last name can only contain letters."

    # Pentru current year
    if not current_year.isdigit() or not (1 <= int(current_year) <= 4):
        errors['currentyear'] = "Current year must be a number between 1 and 4."

    # Pentru series
    if not (series.isalpha() and len(series) == 1 and series.isupper()):
        errors['series'] = "Series must be an upper single letter."

    # Pentru groupnr
    if not groupnr.isdigit() or int(groupnr) <= 0:
        errors['groupnr'] = "Group number must be a positive integer."

    return errors

# Verifica ca datele sa respecte formatul corespunzator pentru fiecare valoare introdusa pentru cursuri
# (returneaza erorile legate de acest aspect)
def validate_course(coursename, credits, coursetype):
    errors = {}

    # Pentru course name
    if not (1 <= len(coursename) <= 100):
        errors['coursename'] = "Course name must be between 1 and 100 characters."
    elif not re.match(r'^[a-zA-Z0-9ăâîșțĂÂÎȘȚ]+(?:[- ][a-zA-Z0-9ăâîșțĂÂÎȘȚ]+)*$', coursename):
        errors['coursename'] = "Course name can only contain letters, numbers."

    # Pentru credits
    if not credits.isdigit() or not (1 <= int(credits) <= 10):
        errors['credits'] = "Credits must be a positive integer between 1 and 10."

    # Pentru tipul cursrului
    if coursetype not in ['mandatory', 'optional']:
        errors['coursetype'] = "Course type must be either 'mandatory' or 'optional'."

    return errors

# Verifica ca datele sa respecte formatul corespunzator pentru fiecare valoare introdusa pentru inrolari
# (returneaza erorile legate de acest aspect)
def validate_enrollment(studentid, courseid, enrollmentdate, grade, editflag):
    errors = {}
    connection = get_db_connection()

    try:
        cursor = connection.cursor()
        # Pentru inrolare deja existenta
        cursor.execute(
            "SELECT COUNT(*) FROM Enrollments WHERE studentid = %s AND courseid = %s",
            (studentid, courseid)
        )
        enrollment_exists = cursor.fetchone()[0] > 0
        if enrollment_exists and editflag==False:
            errors['general'] = "This enrollment already exists (student and course are already linked)."

    except Exception as e:
        print(f"Error validating enrollment IDs: {e}")
        errors['general'] = "An error occurred during validation."
    finally:
        close_db_connection(connection)

    # Pentru enrollmentdate
    try:
        from datetime import datetime
        datetime.strptime(enrollmentdate, '%Y-%m-%d')
    except ValueError:
        errors['enrollmentdate'] = "Enrollment date must be in the format YYYY-MM-DD."

    # Pentru grade
    try:
        grade_value = float(grade)
        if grade_value < 0.0 or grade_value > 10.0:
            errors['grade'] = "Grade must be a float between 0.0 and 10.0."
    except ValueError:
        errors['grade'] = "Grade must be a valid float."
    return errors

# Adauga un student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Extrage datele din form
        first_name = request.form['firstname'].strip()
        last_name = request.form['lastname'].strip()
        current_year = request.form['currentyear']
        series = request.form['series'].strip()
        groupnr = request.form['groupnr']

        # Valideaza si preia erorile
        errors = validate_student_data(first_name, last_name, current_year, series, groupnr)

        if not errors:  # Daca nu au fost gasite erori
            connection = get_db_connection()
            # Se incearca adaugarea datelor studentului in tabela
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Students (firstname, lastname, currentyear, series, groupnr)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (first_name, last_name, current_year, series, groupnr)
                )
                connection.commit()
                return redirect(url_for('manage_students'))
            except Exception as e:
                print(f"Database error while adding student: {e}")
            finally:
                close_db_connection(connection)

        # Mai incarca o data formul cu erorile aparute si datele deja introduse
        return render_template(
            'add_student.html',
            errors=errors,
            form_data={'firstname': first_name, 'lastname': last_name, 'currentyear': current_year,
                       'series': series, 'groupnr': groupnr}
        )

    # Incarca interfata necompletata utilizatorului(pentru metoda GET)
    return render_template('add_student.html', errors={}, form_data={})

# Adauga un curs
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        # Extrage datele din form
        coursename = request.form['coursename'].strip()
        credite = request.form['credits'].strip()
        coursetype = request.form['coursetype'].strip()

        # Valideaza si preia erorile
        errors = validate_course(coursename, credite, coursetype)

        if not errors:  # Daca nu au fost gasite erori
            connection = get_db_connection()
            # Se incearca adaugarea datelor cursului in tabela
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Courses (coursename, credits, coursetype) VALUES (%s, %s, %s)",
                    (coursename, credite, coursetype)
                )
                connection.commit()
                return redirect(url_for('manage_courses'))
            except Exception as e:
                print(f"Error adding course: {e}")
            finally:
                close_db_connection(connection)

        # Mai incarca o data formul cu erorile aparute si datele deja introduse
        return render_template('add_course.html', errors=errors, form_data=request.form)

    # Incarca interfata necompletata utilizatorului(pentru metoda GET)
    return render_template('add_course.html', errors={}, form_data={})

# Adauga o inrolare
@app.route('/add_enrollment', methods=['GET', 'POST'])
def add_enrollment():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Extrage date din studenti si cursuri pentru dropdown-uri
    cursor.execute("SELECT studentid, firstname, lastname FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT courseid, coursename FROM courses")
    courses = cursor.fetchall()

    if request.method == 'POST':
        # Extrage datele din form
        studentid = request.form['studentid'].strip()
        courseid = request.form['courseid'].strip()
        enrollmentdate = request.form['enrollmentdate'].strip()
        grade = request.form['grade'].strip()

        # Valideaza si preia erorile
        errors = validate_enrollment(studentid, courseid, enrollmentdate, grade, False)

        if not errors:  # Daca nu au fost gasite erori
            try:
                cursor.execute(
                    """
                    INSERT INTO enrollments (studentid, courseid, enrollmentdate, grade)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (studentid, courseid, enrollmentdate, grade)
                )
                connection.commit()
                return redirect(url_for('manage_enrollments'))
            except Exception as e:
                print(f"Database error while adding enrollment: {e}")
            finally:
                close_db_connection(connection)

        # Mai incarca o data formul cu erorile aparute si datele deja introduse
        return render_template(
            'add_enrollment.html',
            errors=errors,
            form_data=request.form,
            students=students,
            courses=courses
        )

    # Incarca interfata necompletata utilizatorului(pentru metoda GET)
    return render_template(
        'add_enrollment.html',
        errors={},
        form_data={},
        students=students,
        courses=courses
    )

# Editeaza datele unui student ales
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        connection = get_db_connection()
        try:
            # Extrage datele din form
            first_name = request.form['firstname'].strip()
            last_name = request.form['lastname'].strip()
            current_year = request.form['currentyear']
            series = request.form['series'].strip()
            groupnr = request.form['groupnr']

            # Valideaza si preia erorile
            errors = validate_student_data(first_name, last_name, current_year, series, groupnr)

            if not errors:  # Daca nu au fost gasite erori
                # Se incearca modificarea datelor studentului ales din tabela
                try:
                    cursor = connection.cursor()
                    cursor.execute(
                        """
                        UPDATE Students
                        SET firstname = %s, lastname = %s, currentyear = %s, series = %s, groupnr = %s
                        WHERE studentid = %s
                        """,
                        (first_name, last_name, current_year, series, groupnr, student_id)
                    )
                    connection.commit()
                    return redirect(url_for('manage_students'))
                except Exception as e:
                    print(f"Database error while updating student: {e}")

            # Mai incarca o data formul cu erorile aparute si datele deja introduse
            return render_template(
                'edit_student.html',
                errors=errors,
                student={'studentid': student_id, 'firstname': first_name, 'lastname': last_name,
                         'currentyear': current_year, 'series': series, 'groupnr': groupnr}
            )

        except Exception as e:
            print(f"Error processing the student edit form: {e}")
        finally:
            close_db_connection(connection)

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Students WHERE studentid = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            abort(404)  # Studentul nu a fost gasit
    finally:
        close_db_connection(connection)

    # Incarca interfata utilizatorului(pentru metoda GET)
    return render_template('edit_student.html', errors={}, student=student)

# Editeaza datele unui curs ales
@app.route('/edit_course/<int:courseid>', methods=['GET', 'POST'])
def edit_course(courseid):
    if request.method == 'POST':
        connection = get_db_connection()
        try:
            # Extrage datele din form
            coursename = request.form['coursename'].strip()
            credite = request.form['credits']
            coursetype = request.form['coursetype'].strip()
        
            # Valideaza si preia erorile
            errors = validate_course(coursename, credite, coursetype)
            if not errors: # Daca nu au fost gasite erori
            # Se incearca modificarea datelor studentului ales din tabela
                try:
                    cursor = connection.cursor()
                    cursor.execute(
                    "UPDATE courses SET coursename = %s, credits = %s, coursetype = %s WHERE courseid = %s",
                    (coursename, credite, coursetype, courseid)
                    )
                    connection.commit()
                    return redirect(url_for('manage_courses'))
                except Exception as e:
                    print(f"Database error while updating course: {e}")

            # Mai incarca o data formul cu erorile aparute si datele deja introduse
            return render_template(
                'edit_course.html',
                course={'courseid': courseid,'coursename': coursename, 'credits': credite, 'coursetype': coursetype},
                errors=errors,
                form_data=request.form
            )

                
        except Exception as e:
            print(f"Error processing the course edit form: {e}")
        finally:
            close_db_connection(connection)

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses WHERE courseid = %s", (courseid,))
        course = cursor.fetchone()
        if not course:
            print("Course not found.")
            abort(404)  # Cursul nu a fost gasit
    finally:
        close_db_connection(connection)

    # Incarca interfata utilizatorului(pentru metoda GET)
    return render_template('edit_course.html', course=course, errors={}, form_data={})

# Editeaza datele unui enrollment ales
@app.route('/edit_enrollment/<int:studentid>/<int:courseid>', methods=['GET', 'POST'])
def edit_enrollment(studentid, courseid):
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            # Extrage datele din form
            enrollmentdate = request.form['enrollmentdate'].strip()
            grade = request.form['grade'].strip()

            # Valideaza si preia erorile
            errors = validate_enrollment(str(studentid), str(courseid), enrollmentdate, grade, True)
            if not errors:  # Daca nu au fost gasite erori
            # Se incearca modificarea datelor studentului ales din tabela
                try:
                    cursor = connection.cursor()
                    cursor.execute(
                        """
                        UPDATE Enrollments
                        SET enrollmentdate = %s, grade = %s
                        WHERE studentid = %s AND courseid = %s
                        """,
                        (enrollmentdate, grade, studentid, courseid)
                    )
                    connection.commit()
                    return redirect(url_for('manage_enrollments'))
                except Exception as e:
                    print(f"Database error while updating enrollment: {e}")
                finally:
                    close_db_connection(connection)

            # Mai incarca o data formul cu erorile aparute si datele deja introduse
            return render_template(
                'edit_enrollment.html',
                errors=errors,
                form_data=request.form,
                enrollment={
                    'studentid': studentid,
                    'courseid': courseid,
                    'enrollmentdate': enrollmentdate,
                    'grade': grade,
                    'student_name': request.form.get('student_name', ''),
                    'course_name': request.form.get('course_name', ''),
                }
            )

        # Incarca interfata utilizatorului(pentru metoda GET)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT e.studentid, e.courseid, e.enrollmentdate, e.grade,
                   CONCAT(s.firstname, ' ', s.lastname) AS student_name,
                   c.coursename AS course_name
            FROM Enrollments e
            INNER JOIN Students s ON e.studentid = s.studentid
            INNER JOIN Courses c ON e.courseid = c.courseid
            WHERE e.studentid = %s AND e.courseid = %s
            """,
            (studentid, courseid)
        )
        enrollment = cursor.fetchone()
        if not enrollment:
            abort(404)  # Inrolarea nu a fost gasita
        return render_template('edit_enrollment.html', errors={}, form_data={}, enrollment=enrollment)
    except Exception as e:
        print(f"Error fetching enrollment: {e}")
        abort(500)
    finally:
        close_db_connection(connection)

# Sterge studentii alesi
@app.route('/delete_students', methods=['POST'])
def delete_students():
    student_ids = request.form.getlist('student_ids')
    if student_ids:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            for currentid in student_ids:
                cursor.execute("DELETE FROM Students WHERE studentid = %s", (currentid,))
                connection.commit()
        except Exception as e:
            print(f"Error deleting students: {e}")
            return "An error occurred while deleting students", 500
        finally:
            close_db_connection(connection)
    return redirect(url_for('manage_students'))

# Sterge cursurile alese
@app.route('/delete_courses', methods=['POST'])
def delete_courses():
    course_ids = request.form.getlist('course_ids')
    if course_ids:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            for currentid in course_ids:
                cursor.execute("DELETE FROM Courses WHERE courseid = %s", (currentid,))
                connection.commit()
        finally:
            close_db_connection(connection)
    return redirect(url_for('manage_courses'))

# Sterge inscrierile alese
@app.route('/delete_enrollments', methods=['POST'])
def delete_enrollment():
    enrollment_ids = request.form.getlist('enrollment_ids')
    if enrollment_ids:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            # Imparte lista obtinuta ['studentid'-'courseid'] in studentid and courseid
            ids = [id_.split('-') for id_ in enrollment_ids]
            values = [(int(studentid), int(courseid)) for studentid, courseid in ids]
            for val in values:
                cursor.execute("DELETE FROM Enrollments WHERE studentid =%s AND courseid=%s",(val[0],val[1],))
                connection.commit()

        except Exception as e:
            print(f"Error deleting enrollments: {e}")
            return "An error occurred while deleting enrollments", 500
        finally:
            close_db_connection(connection)

    return redirect(url_for('manage_enrollments'))

# Afiseaza lista cu studenti
@app.route('/manage_students', methods=['GET'])
def manage_students():
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving students: {e}")
        students = []
    finally:
        close_db_connection(connection)
    return render_template('students.html', students=students)

# Afiseaza lista cu cursuri
@app.route('/manage_courses', methods=['GET'])
def manage_courses():
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Courses")
        courses = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving courses: {e}")
        courses = []
    finally:
        close_db_connection(connection)
    return render_template('courses.html', courses=courses)

#Afiseaza lista cu inscrieri
@app.route('/manage_enrollments', methods=['GET'])
def manage_enrollments():
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            e.studentid,
            e.courseid,
            e.enrollmentdate,
            e.grade,
            s.firstname AS student_firstname,
            s.lastname AS student_lastname,
            c.coursename AS course_name
        FROM 
            Enrollments e
        INNER JOIN 
            Students s ON e.studentid = s.studentid
        INNER JOIN 
            Courses c ON e.courseid = c.courseid
        ORDER BY e.enrollmentdate DESC
        """
        cursor.execute(query)
        enrollments = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving enrollments: {e}")
        enrollments = []
    finally:
        close_db_connection(connection)

    return render_template('enrollments.html', enrollments=enrollments)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
