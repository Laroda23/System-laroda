# ===== PROBLEMA =====
# Nahihirapan at natatagalan ang mga guro o department heads sa pag-compute
# ng General Weighted Average (GWA) at pagtukoy sa Class Top Performers
# (Dean's List / Honors). 
#
# ===== SOLUSYON =====
# CLI system na nag-i-input ng marka at units bawat subject ng estudyante.
# Gumagamit ng SQL formula: SUM(grade * units) / SUM(units) para sa eksaktong GWA.
# Nagpapamalas ng ranking ng Top 10 students bawat section/course sa terminal.
import gwa_db
import grade_engine


def gwa_menu():
    print("\n" + "="*52)
    print("     STUDENT GRADE PROCESSING & GWA CALCULATOR")
    print("="*52)
    print("  [1] Magdagdag ng Estudyante")
    print("  [2] Magdagdag ng Subject")
    print("  [3] I-encode ang Marka (Grades)")
    print("  [4] Tingnan ang GWA ng Estudyante")
    print("  [5] Tingnan ang mga Marka ng Estudyante")
    print("  [6] Class Ranking (Top 10) Bawat Seksyon")
    print("  [7] Tingnan ang Listahan ng mga Estudyante")
    print("  [8] Tingnan ang Listahan ng mga Subject")
    print("  [0] Lumabas")
    print("="*52)


def gwa_cli():
    ok, msg = gwa_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_gwa.sql' sa XAMPP/MySQL.")
        return
    while True:
        gwa_menu()
        ch = input("\n  Ano'ng aksyon ang gagawin? : ").strip()
        if ch == "1":
            grade_engine.register_learner()
        elif ch == "2":
            grade_engine.register_subject()
        elif ch == "3":
            grade_engine.post_mark()
        elif ch == "4":
            grade_engine.show_general_average()
        elif ch == "5":
            grade_engine.show_mark_sheet()
        elif ch == "6":
            grade_engine.rank_section()
        elif ch == "7":
            grade_engine.show_learner_list()
        elif ch == "8":
            grade_engine.show_subject_list()
        elif ch == "0":
            print("\n  Sige, paalam!")
            break
        else:
            print("\n  * Hindi tamang pagpili.")


if __name__ == "__main__":
    gwa_cli()
