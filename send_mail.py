import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

# Загрузка переменных окружения из файла .env
load_dotenv()

def send_mail(message):
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    destination_mail = "nikataqtaqishvili72@gmail.com"
    if not sender or not password:
        return "Sender email or password not set in environment variables."
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Booking at a beauty salon 💅"
        server.sendmail(sender, destination_mail, msg.as_string())
        #server.sendmail(sender, destination_mail,f"Subject: Booking at a beauty salon\n{message}")

        return "The message was sent successfully!!!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password!"
def main():
    message = "We remind you that in an hour you have a service booked in our salon❤️"
    print(send_mail(message=message))

if __name__ == "__main__":
    main()
