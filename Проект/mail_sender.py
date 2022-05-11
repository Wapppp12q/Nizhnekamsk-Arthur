import os

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(email, code):
    addr_from = os.getenv("FROM")
    password = os.getenv('PASSWORD')

    body = f"Здравствуйте! Код подтверждения регистрации {email} - {code}."
    msg = MIMEText(body)
    msg['Subject'] = 'Код активации'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(addr_from, password)
    server.sendmail(addr_from, email, msg.as_string())