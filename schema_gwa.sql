-- PROBLEMA:
-- Nahihirapan at natatagalan ang mga guro o department heads sa pag-compute
-- ng General Weighted Average (GWA) at pagtukoy sa Class Top Performers
-- (Dean's List / Honors).
--
-- SOLUSYON:
-- CLI system na nag-i-input ng mga marka (grades) at units bawat subject ng estudyante.
-- Gumagamit ang terminal ng SQL SUM(grade * units) / SUM(units) para makuha ang eksaktong GWA.
-- Nagpapamalas ng ranking ng top 10 students bawat section/course sa terminal interface.

CREATE DATABASE IF NOT EXISTS school_grades_db;
USE school_grades_db;

CREATE TABLE IF NOT EXISTS students (
  student_id VARCHAR(20) PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  section VARCHAR(50) NOT NULL,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
  subject_code VARCHAR(20) PRIMARY KEY,
  subject_name VARCHAR(150) NOT NULL,
  units INT NOT NULL DEFAULT 1,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grades (
  grade_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  subject_code VARCHAR(20) NOT NULL,
  numeric_grade DECIMAL(4,2) NOT NULL,
  semester VARCHAR(30) NOT NULL,
  date_encoded DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_g_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_g_subject FOREIGN KEY (subject_code) REFERENCES subjects(subject_code) ON DELETE RESTRICT ON UPDATE CASCADE,
  UNIQUE KEY uniq_student_subject_sem (student_id, subject_code, semester)
);
