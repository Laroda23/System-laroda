# ===== PROBLEMA =====
# Nahihirapan at natatagalan ang mga guro o department heads sa pag-compute
# ng General Weighted Average (GWA) at pagtukoy sa Class Top Performers
# (Dean's List / Honors).
#
# ===== SOLUSYON =====
# Gumagamit ng SQL: SUM(grade * units) / SUM(units) para makuha ang eksaktong GWA.
# Nagpapamalas ng ranking ng Top 10 students bawat section/course.

import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "school_grades_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM students LIMIT 1")
            cursor.fetchone()
            return True, "Koneksyon sa Student Grade Processing database ay OK na."
        return False, "Hindi makakonekta sa database."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# STUDENTS
def add_student(student_id, name, section):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (student_id, name, section) VALUES (%s,%s,%s)",
            (student_id, name, section),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_student(student_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_students():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY section, name")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# SUBJECTS
def add_subject(subject_code, subject_name, units):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO subjects (subject_code, subject_name, units) VALUES (%s,%s,%s)",
            (subject_code, subject_name, units),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_subject(subject_code):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subjects WHERE subject_code = %s", (subject_code,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_subjects():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subjects ORDER BY subject_code")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# GRADES
def add_grade(student_id, subject_code, numeric_grade, semester):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO grades (student_id, subject_code, numeric_grade, semester)
            VALUES (%s,%s,%s,%s)
            """,
            (student_id, subject_code, numeric_grade, semester),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_student_grades(student_id, semester=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        if semester:
            cursor.execute(
                """
                SELECT g.grade_id, g.student_id, g.subject_code, s.subject_name, s.units,
                       g.numeric_grade, g.semester, g.date_encoded
                FROM grades g
                JOIN subjects s ON s.subject_code = g.subject_code
                WHERE g.student_id = %s AND g.semester = %s
                ORDER BY s.subject_code
                """,
                (student_id, semester),
            )
        else:
            cursor.execute(
                """
                SELECT g.grade_id, g.student_id, g.subject_code, s.subject_name, s.units,
                       g.numeric_grade, g.semester, g.date_encoded
                FROM grades g
                JOIN subjects s ON s.subject_code = g.subject_code
                WHERE g.student_id = %s
                ORDER BY g.semester, s.subject_code
                """,
                (student_id,),
            )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_student_gwa(student_id, semester):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT s.student_id, s.name, s.section,
                   SUM(g.numeric_grade * sub.units) / SUM(sub.units) AS gwa,
                   SUM(sub.units) AS total_units,
                   COUNT(g.grade_id) AS total_subjects
            FROM students s
            JOIN grades g ON g.student_id = s.student_id
            JOIN subjects sub ON sub.subject_code = g.subject_code
            WHERE s.student_id = %s AND g.semester = %s
            GROUP BY s.student_id, s.name, s.section
            """,
            (student_id, semester),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_class_ranking(section, semester, limit=10):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT s.student_id, s.name, s.section,
                   SUM(g.numeric_grade * sub.units) / SUM(sub.units) AS gwa,
                   SUM(sub.units) AS total_units,
                   COUNT(g.grade_id) AS total_subjects
            FROM students s
            JOIN grades g ON g.student_id = s.student_id
            JOIN subjects sub ON sub.subject_code = g.subject_code
            WHERE s.section = %s AND g.semester = %s
            GROUP BY s.student_id, s.name, s.section
            ORDER BY gwa ASC
            LIMIT %s
            """,
            (section, semester, limit),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
