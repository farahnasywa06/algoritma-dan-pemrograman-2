import json
import csv
import os
<<<<<<< HEAD
=======
import shutil
>>>>>>> bbf3ee3 (update filesystem)

from pathlib import Path
from models.student import Student

BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< HEAD
STUDENTS_FILE = BASE_DIR / "data" / "students.json"
=======
DEFAULT_STUDENTS_FILE = BASE_DIR / "data" / "students.json"
VERCEL_STUDENTS_FILE = Path("/tmp") / "students.json"
>>>>>>> bbf3ee3 (update filesystem)

IS_VERCEL = os.getenv("VERCEL") == "1"


<<<<<<< HEAD
def load_students():

    if not STUDENTS_FILE.exists():
        return []

    with open(STUDENTS_FILE, "r", encoding="utf-8") as file:
=======
def get_students_file():
    if not IS_VERCEL:
        return DEFAULT_STUDENTS_FILE

    if not VERCEL_STUDENTS_FILE.exists():
        VERCEL_STUDENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if DEFAULT_STUDENTS_FILE.exists():
            shutil.copyfile(DEFAULT_STUDENTS_FILE, VERCEL_STUDENTS_FILE)
        else:
            VERCEL_STUDENTS_FILE.write_text("[]", encoding="utf-8")

    return VERCEL_STUDENTS_FILE


def load_students():
    students_file = get_students_file()

    if not students_file.exists():
        return []

    with open(students_file, "r", encoding="utf-8") as file:
>>>>>>> bbf3ee3 (update filesystem)
        data = json.load(file)

    return [Student.from_dict(item) for item in data]


def save_students(students):
<<<<<<< HEAD

    # Vercel tidak mengizinkan write file
    if IS_VERCEL:
        print("VERCEL MODE -> save_students skipped")
        return

    with open(STUDENTS_FILE, "w", encoding="utf-8") as file:
=======
    students_file = get_students_file()

    with open(students_file, "w", encoding="utf-8") as file:
>>>>>>> bbf3ee3 (update filesystem)

        json.dump(
            [student.to_dict() for student in students],
            file,
            indent=4,
            ensure_ascii=False
        )

<<<<<<< HEAD
=======
    return True

>>>>>>> bbf3ee3 (update filesystem)

def export_json(output_file):

    students = load_students()

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            [student.to_dict() for student in students],
            file,
            indent=4,
            ensure_ascii=False
        )


def import_json(input_file):

<<<<<<< HEAD
    if IS_VERCEL:
        return

=======
>>>>>>> bbf3ee3 (update filesystem)
    with open(input_file, "r", encoding="utf-8") as file:

        data = json.load(file)

    students = [
        Student.from_dict(item)
        for item in data
    ]

    save_students(students)


def export_csv(output_file):

    students = load_students()

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "nim",
                "full_name",
                "major",
                "year",
                "gpa",
                "email",
                "phone",
            ],
        )

        writer.writeheader()

        for student in students:

            writer.writerow(student.to_dict())


def import_csv(input_file):

<<<<<<< HEAD
    if IS_VERCEL:
        return

=======
>>>>>>> bbf3ee3 (update filesystem)
    students = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            students.append(
                Student.from_dict(row)
            )

<<<<<<< HEAD
    save_students(students)
=======
    save_students(students)
>>>>>>> bbf3ee3 (update filesystem)
