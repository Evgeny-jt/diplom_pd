# import os
import smtplib

from celery import shared_task
from .models import User, MailConfirmationCode
from email.message import EmailMessage
from time import sleep

# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


@shared_task()
def send_email_task(send_email, content):
    '''
    Функция отправки почты
    Принемает на вход электронную почту на котоую отправить сообщение и текст сообщения
    '''
    msg = EmailMessage()
    msg['Subject'] = "API shop"
    msg['From'] = 'bym001jt@yandex.ru'
    msg['To'] = send_email
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login('bym001jt@yandex.ru', 'bbwwrfghysnbntah')
        smtp.send_message(msg)
    return


@shared_task()
def code_email_delete_task(code_id, sec_sleep=0):
    '''
    Функция удаления кода подтветждения электронной почты с базы данных
    Принемает на вход id удаляемого сообщения и в секундах время задержки(время жизни кода активации электроннойпочты),
    если задержка не указанна то код удаляется немедленно
    '''
    if sec_sleep > 0:
        sleep(sec_sleep)
    if MailConfirmationCode.objects.filter(id=code_id).exists():
        MailConfirmationCode.objects.filter(id=code_id).delete()
    return
