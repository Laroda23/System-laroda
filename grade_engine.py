# ===== PROBLEMA =====
# Nahihirapan at natatagalan ang mga guro o department heads sa pag-compute
# ng General Weighted Average (GWA) at pagtukoy sa Class Top Performers
# (Dean's List / Honors).
#
# ===== SOLUSYON =====
# CLI na nag-i-input ng marka (numeric_grade) at units bawat subject.
# GWA = SUM(grade * units) / SUM(units) gamit ang SQL computation.
# May Class Ranking (Top 10) bawat section/course.

import re

import mysql.connector

import gwa_db


def ask_required(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        return v


def ask_score(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        try:
            val = float(v)
            if val < 50 or val > 100:
                print("  * Dapat nasa 50 - 100 ang marka.")
                continue
            return val
        except ValueError:
            print("  * Numero lang dapat.")
            continue


def ask_whole_number(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        try:
            val = int(v)
            if val < 1:
                print("  * Dapat mas malaki sa 0 ang units.")
                continue
            return val
        except ValueError:
            print("  * Numero lang dapat.")
            continue


def print_learner_card(s):
    print("\n" + "="*44)
    print(f"  STUDENT ID : {s['student_id']}")
    print("="*44)
    print(f"  Buong Pangalan : {s['name']}")
    print(f"  Seksyon        : {s['section']}")
    if s.get('date_added'):
        print(f"  Idinagdag noong: {s['date_added']}")
    print("="*44)


def print_subject_card(su):
    print("\n" + "="*44)
    print(f"  SUBJECT CODE : {su['subject_code']}")
    print("="*44)
    print(f"  Pangalan ng Subject : {su['subject_name']}")
    print(f"  Units               : {su['units']}")
    if su.get('date_added'):
        print(f"  Idinagdag noong     : {su['date_added']}")
    print("="*44)


def register_learner():
    print("\n--- MAGDAGDAG NG ESTUDYANTE ---")
    sid = ask_required("  Student ID: ").upper()
    try:
        exist = gwa_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if exist:
        print("  [PAALALA] Mayroon nang estudyante na may ganitong Student ID.")
        print_learner_card(exist)
        return
    name = ask_required("  Buong Pangalan (Apelyido, Pangalan): ")
    sec = ask_required("  Seksyon: ")
    try:
        gwa_db.add_student(sid, name, sec)
        print("\n  [TAPOS NA] Naidagdag na ang estudyante.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def register_subject():
    print("\n--- MAGDAGDAG NG SUBJECT ---")
    scode = ask_required("  Subject Code: ").upper()
    try:
        exist = gwa_db.find_subject(scode)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if exist:
        print("  [PAALALA] Mayroon nang subject na may ganitong Subject Code.")
        print_subject_card(exist)
        return
    sname = ask_required("  Pangalan ng Subject: ")
    units = ask_whole_number("  Units: ")
    try:
        gwa_db.add_subject(scode, sname, units)
        print("\n  [TAPOS NA] Naidagdag na ang subject.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def show_learner_list():
    try:
        mark_rows = gwa_db.list_students()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not mark_rows:
        print("\n  Wala pang naitalang estudyante.")
        return
    print("\n--- LISTAHAN NG MGA ESTUDYANTE ---")
    for r in mark_rows:
        print(f"  [{r['student_id']}] {r['name']} | Seksyon: {r['section']}")


def show_subject_list():
    try:
        mark_rows = gwa_db.list_subjects()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not mark_rows:
        print("\n  Wala pang naitalang subject.")
        return
    print("\n--- LISTAHAN NG MGA SUBJECT ---")
    for r in mark_rows:
        print(f"  [{r['subject_code']}] {r['subject_name']} | Units: {r['units']}")


def post_mark():
    print("\n--- I-ENCODE ANG MARKA ---")
    sid = ask_required("  Student ID: ").upper()
    try:
        s = gwa_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi pa naka-register ang estudyante.")
        return
    print_learner_card(s)
    scode = ask_required("  Subject Code: ").upper()
    try:
        sub = gwa_db.find_subject(scode)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not sub:
        print("  [WALA] Hindi pa naka-register ang subject.")
        return
    print_subject_card(sub)
    sem = ask_required("  Semestre (hal. 1st Semester / 2nd Semester): ")
    grade = ask_score("  Numeric Grade (50-100): ")
    try:
        gwa_db.add_grade(sid, scode, grade, sem)
        print("\n  [TAPOS NA] Na-encode na ang marka.")
    except mysql.connector.Error as e:
        if "Duplicate entry" in str(e) or "uniq_student_subject_sem" in str(e):
            print("  [PAALALA] Naka-encode na ang marka ng estudyante sa subject na ito sa nasabing semestre.")
        else:
            print(f"  [MALI] {e}")


def show_mark_sheet():
    print("\n--- TINGNAN ANG MGA MARKA NG ESTUDYANTE ---")
    sid = ask_required("  Student ID: ").upper()
    try:
        s = gwa_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi matagpuan ang estudyante.")
        return
    print_learner_card(s)
    sem = ask_required("  Semestre (Enter para sa LAHAT): ").strip()
    try:
        if sem == "":
            mark_rows = gwa_db.get_student_grades(sid)
        else:
            mark_rows = gwa_db.get_student_grades(sid, sem)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not mark_rows:
        print("\n  Wala pang naka-encode na marka para sa estudyante na ito.")
        return
    print("\n--- MGA MARKA ---")
    for r in mark_rows:
        print(f"  [{r['subject_code']}] {r['subject_name']} | Units:{r['units']} | Grade:{r['numeric_grade']} | Sem:{r['semester']}")
    try:
        if sem != "":
            gwa_res = gwa_db.get_student_gwa(sid, sem)
            if gwa_res and gwa_res['gwa'] is not None:
                gwa_rounded = round(float(gwa_res['gwa']), 2)
                print("\n" + "="*44)
                print(f"  GWA ({sem}): {gwa_rounded}")
                print(f"  Kabuuang Units: {gwa_res['total_units']} | Bilang ng Subjects: {gwa_res['total_subjects']}")
                print("="*44)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def show_general_average():
    print("\n--- TINGNAN ANG GWA NG ESTUDYANTE ---")
    sid = ask_required("  Student ID: ").upper()
    try:
        s = gwa_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi matagpuan ang estudyante.")
        return
    print_learner_card(s)
    sem = ask_required("  Semestre: ")
    try:
        gwa_res = gwa_db.get_student_gwa(sid, sem)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not gwa_res or gwa_res['gwa'] is None:
        print("\n  Wala pang marka na naka-encode para sa semestreng ito.")
        return
    gwa_rounded = round(float(gwa_res['gwa']), 2)
    print("\n" + "="*44)
    print(f"  GWA ({sem}): {gwa_rounded}")
    print(f"  Kabuuang Units: {gwa_res['total_units']}")
    print(f"  Bilang ng Subjects: {gwa_res['total_subjects']}")
    print("="*44)


def rank_section():
    print("\n--- CLASS RANKING (TOP 10) BAWAT SEKSYON ---")
    sec = ask_required("  Seksyon: ")
    sem = ask_required("  Semestre: ")
    try:
        mark_rows = gwa_db.get_class_ranking(sec, sem, 10)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not mark_rows:
        print("\n  Wala pang marka na naka-encode para sa seksyon at semestreng ito.")
        return
    print(f"\n--- TOP 10 | Seksyon: {sec} | {sem} ---")
    rank = 0
    for r in mark_rows:
        rank += 1
        gwa_rounded = round(float(r['gwa']), 2)
        print(f"  #{rank} | [{r['student_id']}] {r['name']} | GWA: {gwa_rounded} | Units: {r['total_units']} | Subjects: {r['total_subjects']}")
