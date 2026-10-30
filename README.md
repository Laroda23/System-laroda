# Student Grade Processing & GWA Calculator

Kini nga sistema motabang sa mga magtutudlo ug department head sa pag-compute
sa **General Weighted Average (GWA)** ug sa pag-ila sa top performers sa klase.
Ang GWA gikompyut sa SQL mismo:

```sql
SUM(numeric_grade * units) / SUM(units)
```

Busa dili na kinahanglan magkalkulo sa kamot.

## Unsa ang kinahanglan

- **Python 3.8 o mas bag-o**
- **XAMPP** (MySQL/MariaDB)
- **mysql-connector-python**

## 1) I-install ang MySQL connector

```powershell
pip install mysql-connector-python
```

## 2) Sugdi ang XAMPP

1. Ablihi ang **XAMPP Control Panel**.
2. Pindota ang **Start** tapad sa **MySQL**.
3. Siguroha nga **green** ang kolor sa MySQL.

## 3) I-import ang database

1. Ablihi ang `http://localhost/phpmyadmin`.
2. Pindota ang **Import** tab.
3. Pilia ang `schema_gwa.sql` (naa sa sama nga folder).
4. Pindota ang **Go** o **Import**.
5. Siguroha nga makita ang `school_grades_db` sa lista sa wala.

## 4) Koneksyon sa database

| Variable | Default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | *(walay password)* |
| `DB_NAME` | `school_grades_db` |

Kung lahi ang setup:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_NAME = "school_grades_db"
```

## 5) Padagana ang sistema

```powershell
cd "C:\Users\suete\Documents\system for sale\laroda=grade_gwa_system"
python main_gwa.py
```

> Kung ibalhin ang folder sa lain nga computer, ilisi ang `cd` path sa
> aktwal nga lokasyon sa folder.


Dapat makita nimo ang **"Koneksyon sa Student Grade Processing database ay OK na."**

## Mga file

| File | Tumong |
| --- | --- |
| `schema_gwa.sql` | Naghimo sa `students`, `subjects`, `grades` |
| `gwa_db.py` | SQL para sa estudyante, subject, marka, GWA, ug ranking |
| `grade_engine.py` | Flow sa menu ug validation sa input |
| `main_gwa.py` | Ang CLI menu |
| `test_compile.py` | Pagsusi kung walay syntax error |

## Menu

| Numero | Aksyon |
| --- | --- |
| `1` | Pagdugang og estudyante |
| `2` | Pagdugang og subject (subject code, pangalan, units) |
| `3` | Pag-encode sa marka |
| `4` | Tan-awa ang GWA sa estudyante |
| `5` | Tan-awa ang mga marka sa estudyante |
| `6` | Ranking sa klase (Top 10) matag seksyon |
| `7` | Listahan sa mga estudyante |
| `8` | Listahan sa mga subject |
| `0` | Gula |

## Importante nga lagda sa input

- Ang **marka** dapat naa sa **50 hangtod 100**.
- Ang **units** dapat **1 o mas daghan**.
- Ang GWA gikompyut base sa tanan nga na-encode nga marka sa estudyante.
- Ang ranking gigrupo matag **seksyon**.

## Giunsa pagtipig ang datos

Ang tanan naa sa MySQL: `school_grades_db.students`, `subjects`, ug `grades`.
Ang GWA dili gitipig; gikompyut kini sa matag query aron laging updated.

## Troubleshooting

| Sayop / Mensahe | Solusyon |
| --- | --- |
| `Can't connect to MySQL server on 'localhost:3306'` | Wala nagdagan ang MySQL. Pindota ang **Start** sa XAMPP. |
| `Unknown database 'school_grades_db'` | Wala pa na-import ang `schema_gwa.sql`. |
| `Table 'school_grades_db.students' doesn't exist` | I-import pag-usab ang schema. |
| `Access denied for user 'root'@'localhost'` | I-set ang `DB_PASSWORD` kung naay password. |
| `ModuleNotFoundError: No module named 'mysql'` | `pip install mysql-connector-python` |
| `Duplicate entry` sa subject o marka | Naa na ang subject code, o naa nay marka sa parehas nga subject ug semester. |

## Backup sa datos

1. Adto sa phpMyAdmin.
2. Pilia ang `school_grades_db`.
3. **Export** → **Go**.
4. Tipigi ang `.sql` file.

## Sulayi ang code

```powershell
python test_compile.py
```

Dapat `OK` ang mogawas.
