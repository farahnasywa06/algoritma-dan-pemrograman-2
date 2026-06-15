import time
import csv
import json
import os
import re
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
)

from services.auth_service import login
from services.activity_service import write_log
from services.import_export_service import (
    load_students,
    save_students,
    import_csv,
    import_json,
)
from services.search_service import LinearSearch, SequentialSearch, BinarySearch
from services.sort_service import BubbleSort, SelectionSort, MergeSort
from services.email_service import send_student_profile
from models.student import Student

app = Flask(__name__)

app.secret_key = "semester3-secret-key"

# =========================

# LOGIN REQUIRED

# =========================


def login_required():
    return "username" in session


# =========================

# HOME

# =========================


@app.route("/")
def home():
    if login_required():
        return redirect(url_for("dashboard"))

    return redirect(url_for("login_page"))


# =========================

# LOGIN

# =========================


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login(username, password):
            session["username"] = username

            write_log(username, "LOGIN", "Berhasil login")

            return redirect(url_for("dashboard"))

        flash("Username atau Password salah")

    return render_template("login.html")


# =========================

# LOGOUT

# =========================


@app.route("/logout")
def logout():
    if "username" in session:
        write_log(session["username"], "LOGOUT", "Logout sistem")

    session.clear()

    return redirect(url_for("login_page"))


# =========================

# DASHBOARD

# =========================


@app.route("/dashboard")
def dashboard():

    students = load_students()

    total_students = len(students)

    majors = set()

    total_gpa = 0

    year_data = {}
    major_data = {}

    for student in students:

        majors.add(student.major)

        total_gpa += student.gpa

        year_data[student.year] = year_data.get(student.year, 0) + 1

        major_data[student.major] = major_data.get(student.major, 0) + 1

    average_gpa = 0

    if total_students > 0:

        average_gpa = round(total_gpa / total_students, 2)
    try:

        with open("data/activity_log.json", "r", encoding="utf-8") as file:

            logs = json.load(file)

        logs.reverse()

        recent_logs = logs[:5]

    except:

        recent_logs = []
    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_majors=len(majors),
        average_gpa=average_gpa,
        students=[student.to_dict() for student in students],
        year_data=year_data,
        major_data=major_data,
        recent_logs=recent_logs,
    )


# =========================

# STUDENTS PAGE

# =========================


@app.route("/students")
def students_page():

    if not login_required():
        return redirect(url_for("login_page"))

    students = load_students()

    # =========================
    # PARAMETER FILTER
    # =========================

    keyword = request.args.get("keyword", "").strip()

    search_method = request.args.get("search", "linear")

    sort_method = request.args.get("sort", "merge")

    search_field = request.args.get("field", "full_name")

    sort_field = request.args.get("sort_field", "nim")

    order = request.args.get("order", "asc")

    execution_time = 0
    complexity = "-"

    # =========================
    # MULAI HITUNG WAKTU
    # =========================

    start = time.perf_counter()

    # =========================
    # SEARCHING
    # =========================

    if keyword:

        if search_method == "linear":

            students = LinearSearch.search(students, keyword, search_field)

            complexity = "O(n)"

        elif search_method == "sequential":
            students = SequentialSearch.search(students, keyword, search_field)

            complexity = "O(n)"

        elif search_method == "binary":

            # Binary Search wajib data terurut

            students = MergeSort.sort(students, search_field)

            students = BinarySearch.search(students, keyword, search_field)

            complexity = "O(log n)"

    # =========================
    # SORTING
    # =========================

    if sort_method == "bubble":

        students = BubbleSort.sort(students, sort_field)

    elif sort_method == "selection":

        students = SelectionSort.sort(students, sort_field)

    elif sort_method == "merge":

        students = MergeSort.sort(students, sort_field)

    # =========================
    # DESCENDING
    # =========================

    if order == "desc":

        students.reverse()

    # =========================
    # EXECUTION TIME
    # =========================

    execution_time = round((time.perf_counter() - start) * 1000, 4)

    return render_template(
        "students.html",
        students=students,
        execution_time=execution_time,
        complexity=complexity,
        keyword=keyword,
        search_method=search_method,
        sort_method=sort_method,
        search_field=search_field,
        sort_field=sort_field,
        order=order,
    )


@app.route("/export/csv")
def export_csv():

    students = load_students()

    csv_file = "data/export_students.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["nim", "full_name", "major", "year", "gpa", "email", "phone"])

        for student in students:

            writer.writerow(
                [
                    student.nim,
                    student.full_name,
                    student.major,
                    student.year,
                    student.gpa,
                    student.email,
                    student.phone,
                ]
            )

    return send_file(csv_file, as_attachment=True)


@app.route("/export/json")
def export_json():

    students = load_students()

    export_file = "data/export_students.json"

    with open(export_file, "w", encoding="utf-8") as file:

        json.dump([student.to_dict() for student in students], file, indent=4)

    return send_file(export_file, as_attachment=True)


@app.route("/import/csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]

    if file.filename == "":

        flash("Pilih file CSV terlebih dahulu")

        return redirect(url_for("students_page"))

    upload_path = "data/temp_import.csv"

    file.save(upload_path)

    import_csv(upload_path)

    flash("Import CSV berhasil")

    return redirect(url_for("students_page"))


@app.route("/import/json", methods=["POST"])
def upload_json():

    file = request.files["file"]

    if file.filename == "":

        flash("Pilih file JSON terlebih dahulu")

        return redirect(url_for("students_page"))

    upload_path = "data/temp_import.json"

    file.save(upload_path)

    import_json(upload_path)

    flash("Import JSON berhasil")

    return redirect(url_for("students_page"))


# =========================

# ADD STUDENT

# =========================


@app.route("/students/add", methods=["POST"])
def add_student():

    nim = request.form["nim"].strip()
    full_name = request.form["full_name"].strip()
    major = request.form["major"].strip()
    year = request.form["year"]
    gpa = request.form["gpa"]
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    # Validasi NIM
    if not re.match(r"^\d{12}$", nim):

        flash("NIM harus terdiri dari 12 digit angka")

        return redirect(url_for("students_page"))

    # Validasi Nama
    if not re.match(r"^[A-Za-z\s]+$", full_name):

        flash("Nama hanya boleh huruf dan spasi")

        return redirect(url_for("students_page"))

    # Validasi Email
    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):

        flash("Format email tidak valid")

        return redirect(url_for("students_page"))

    # Validasi Nomor HP
    if not re.match(r"^08\d{8,12}$", phone):

        flash("Nomor HP tidak valid")

        return redirect(url_for("students_page"))

    students = load_students()

    # Cek NIM Duplikat
    for student in students:

        if student.nim == nim:

            flash("NIM sudah terdaftar")

            return redirect(url_for("students_page"))

    try:

        new_student = Student(
            nim=nim,
            full_name=full_name,
            major=major,
            year=int(year),
            gpa=float(gpa),
            email=email,
            phone=phone,
        )

        students.append(new_student)

        save_students(students)

        write_log(session["username"], "ADD", f"Tambah mahasiswa {nim}")

        flash("Mahasiswa berhasil ditambahkan")

    except Exception as error:

        flash(f"Terjadi kesalahan: {error}")

    return redirect(url_for("students_page"))


@app.route("/students/update/<nim>", methods=["POST"])
def update_student(nim):

    full_name = request.form["full_name"].strip()
    major = request.form["major"].strip()
    year = request.form["year"]
    gpa = request.form["gpa"]
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    if not re.match(r"^[A-Za-z\s]+$", full_name):

        flash("Nama hanya boleh huruf dan spasi")

        return redirect(url_for("students_page"))

    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):

        flash("Format email tidak valid")

        return redirect(url_for("students_page"))

    if not re.match(r"^08\d{8,12}$", phone):

        flash("Nomor HP tidak valid")

        return redirect(url_for("students_page"))

    students = load_students()

    try:

        for student in students:

            if student.nim == nim:

                student.full_name = full_name
                student.major = major
                student.year = int(year)
                student.gpa = float(gpa)
                student.email = email
                student.phone = phone

                break

        save_students(students)

        write_log(session["username"], "UPDATE", f"Update mahasiswa {nim}")

        flash("Data mahasiswa berhasil diperbarui")

    except Exception as error:

        flash(f"Terjadi kesalahan: {error}")

    return redirect(url_for("students_page"))


# =========================

# DELETE STUDENT

# =========================


@app.route("/students/delete/<nim>")
def delete_student(nim):

    students = load_students()

    students = [student for student in students if student.nim != nim]

    save_students(students)

    write_log(session["username"], "DELETE", f"Hapus mahasiswa {nim}")

    flash("Mahasiswa berhasil dihapus")

    return redirect(url_for("students_page"))


@app.route("/students/delete-all")
def delete_all_students():

    if not login_required():

        return redirect(url_for("login_page"))

    save_students([])

    write_log(
        session["username"],
        "DELETE",
        f"Menghapus seluruh data mahasiswa",
    )

    flash("Semua data mahasiswa berhasil dihapus.")

    return redirect(url_for("students_page"))


# =========================

# SEND EMAIL

# =========================


@app.route("/send-email/<nim>")
def send_email_student(nim):

    students = load_students()

    student = None

    for item in students:

        if item.nim == nim:

            student = item

            break

    if student is None:

        flash("Mahasiswa tidak ditemukan")

        return redirect(url_for("students_page"))

    send_student_profile(student)

    write_log(session["username"], "EMAIL", f"Kirim profil mahasiswa {student.nim}")

    flash(f"Data mahasiswa berhasil dikirim ke {student.email}")

    return redirect(url_for("students_page"))


# =========================

# SETTINGS

# =========================


@app.route("/settings")
def settings():

    students = load_students()

    try:

        with open("data/activity_log.json", "r", encoding="utf-8") as file:

            logs = json.load(file)

    except:

        logs = []

    return render_template(
        "settings.html", total_students=len(students), total_logs=len(logs)
    )


# =========================

# ACTIVITY LOG


# =========================
@app.route("/activity-log")
def activity_log_page():

    try:

        with open("data/activity_log.json", "r", encoding="utf-8") as file:

            logs = json.load(file)

        # Aktivitas terbaru di atas
        logs.reverse()

    except Exception:

        logs = []

    return render_template("activity_log.html", logs=logs)


# =========================

# RUN APP

# =========================

if __name__ == "__main__":

    app.run()
