import json
import csv

from pathlib import Path

from models.student import Student

BASE_DIR = Path(__file__).resolve().parent.parent

STUDENTS_FILE = BASE_DIR / "data" / "students.json"


def load_students():

    if not STUDENTS_FILE.exists():

        return []

    with open(STUDENTS_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return [Student.from_dict(item) for item in data]


def save_students(students):

    with open(STUDENTS_FILE, "w", encoding="utf-8") as file:

        json.dump([student.to_dict() for student in students], file, indent=4)


def export_json(output_file):

    students = load_students()

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump([student.to_dict() for student in students], file, indent=4)


def import_json(input_file):

    with open(input_file, "r", encoding="utf-8") as file:

        data = json.load(file)

    students = [Student.from_dict(item) for item in data]

    save_students(students)


def export_csv(output_file):

    students = load_students()

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["nim", "full_name", "major", "year", "gpa", "email", "phone"],
        )

        writer.writeheader()

        for student in students:

            writer.writerow(student.to_dict())


def import_csv(input_file):

    students = []

    with open(input_file, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            students.append(Student.from_dict(row))

    save_students(students)
