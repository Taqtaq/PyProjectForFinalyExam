import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import sqlite3

# Загрузка переменных окружения из файла .env
load_dotenv()


def send_mail(to_email, subject, message):
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    if not sender or not password:
        print("Sender email or password not set in environment variables.")
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as _ex:
        print(f"Failed to send email to {to_email}: {_ex}")


def get_upcoming_appointments():
    conn = sqlite3.connect("beauty.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    one_hour_from_now = datetime.now() + timedelta(hours=1)
    one_hour_from_now_str = one_hour_from_now.strftime("%Y-%m-%d %H:%M:%S")

    query = """
        SELECT a.AppointmentID, a.StartTime, c.Email, c.FirstName, c.LastName, s.ServiceName 
        FROM Appointments a
        JOIN Clients c ON a.ClientID = c.Client_id
        JOIN Services s ON a.ServiceID = s.ServiceID
        WHERE a.StartTime BETWEEN datetime('now') AND ?
    """
    c.execute(query, (one_hour_from_now_str,))
    appointments = c.fetchall()
    conn.close()
    return appointments


def main():
    appointments = get_upcoming_appointments()
    for appointment in appointments:
        email = appointment["Email"]
        first_name = appointment["FirstName"]
        last_name = appointment["LastName"]
        service_name = appointment["ServiceName"]
        start_time = appointment["StartTime"]

        subject = "Reminder: Upcoming Appointment"
        message = f"""
        <p>Dear {first_name} {last_name},</p>
        <p>This is a reminder for your upcoming appointment for <strong>{service_name}</strong> at <strong>{start_time}</strong>.</p>
        <p>Thank you for choosing our beauty salon!</p>
        """

        send_mail(email, subject, message)


if __name__ == "__main__":
    main()