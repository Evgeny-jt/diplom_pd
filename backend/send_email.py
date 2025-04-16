import smtplib
from email.message import EmailMessage

from time import sleep


def send_email_registration(send_email, content):
    msg = EmailMessage()
    msg['Subject'] = "Email test"
    msg['From'] = "bym001jt@yandex.ru"
    msg['To'] = send_email
    msg.set_content(content)
    sleep(20)

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login('bym001jt@yandex.ru', 'bbwwrfghysnbntah')
        smtp.send_message(msg)

