from celery import shared_task

from .models import User, MailConfirmationCode

import smtplib
from email.message import EmailMessage

from time import sleep


@shared_task()
def send_email_task(send_email, content):
    '''
    Функция отправки почты
    Принемает на вход электронную почту на котоую отправить сообщение и текст сообщения
    '''
    msg = EmailMessage()
    msg['Subject'] = "Email test"
    msg['From'] = "bym001jt@yandex.ru"
    msg['To'] = send_email
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login('bym001jt@yandex.ru', 'bbwwrfghysnbntah')
        smtp.send_message(msg)


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




