import json
import random
import smtplib

from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

OTP_FILE = BASE_DIR / "data" / "otp.json"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def ensure_otp_file():

    if not OTP_FILE.exists():

        with open(OTP_FILE, "w", encoding="utf-8") as file:

            json.dump({}, file)


def generate_otp():

    return str(random.randint(100000, 999999))


def save_otp(email, otp):

    ensure_otp_file()

    with open(OTP_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    data[email] = otp

    with open(OTP_FILE, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)


def verify_otp(email, otp):

    ensure_otp_file()

    with open(OTP_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return email in data and data[email] == otp


def send_email(recipient, subject, message):

    msg = MIMEMultipart()

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.send_message(msg)

    server.quit()


def send_otp(email):

    otp = generate_otp()

    save_otp(email, otp)

    send_email(
        email,
        "Kode OTP Verifikasi",
        f"""


    Kode OTP Anda :

    {otp}

    Jangan berikan kode ini
    kepada siapapun.


        """,
    )

    return otp


def send_student_profile(student):

    subject = "Data Mahasiswa"

    body = f"""
Halo {student.full_name},

Berikut data mahasiswa Anda:

NIM       : {student.nim}
Nama      : {student.full_name}
Program   : {student.major}
Angkatan  : {student.year}
IPK       : {student.gpa}
Email     : {student.email}
Telepon   : {student.phone}

Terima kasih.

Student Management System
"""

    send_email(student.email, subject, body)
