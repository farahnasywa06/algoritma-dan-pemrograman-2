import json
import random

first_names = [
    "Aditya", "Farah", "Rizky", "Dinda", "Andi",
    "Budi", "Siti", "Nabila", "Fajar", "Putri",
    "Rafi", "Aulia", "Yoga", "Intan", "Dimas",
    "Nanda", "Rahma", "Arif", "Kevin", "Rina"
]

last_names = [
    "Saputra", "Pratama", "Wijaya", "Ramadhan",
    "Permata", "Putra", "Sari", "Lestari",
    "Nugroho", "Hidayat", "Kusuma",
    "Maulana", "Ananda", "Purnama"
]

majors = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Komputer",
    "Ilmu Komputer",
    "Teknologi Informasi"
]

students = []

TOTAL_DATA = 1000

for i in range(TOTAL_DATA):

    nim = f"23{i:05d}"

    first = random.choice(first_names)
    last = random.choice(last_names)

    full_name = f"{first} {last}"

    email = (
        full_name
        .lower()
        .replace(" ", ".")
        + "@gmail.com"
    )

    student = {
        "nim": nim,
        "full_name": full_name,
        "major": random.choice(majors),
        "year": random.randint(2020, 2025),
        "gpa": round(random.uniform(2.50, 4.00), 2),
        "email": email,
        "phone": f"08{random.randint(1000000000,9999999999)}"
    }

    students.append(student)

with open(
    "data/students.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        students,
        file,
        indent=4,
        ensure_ascii=False
    )

print(
    f"{TOTAL_DATA} data mahasiswa berhasil dibuat."
)