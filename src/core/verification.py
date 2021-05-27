from datetime import timedelta
import logging
import random
import string

import emails
from src.core.config import settings
from src.core.security import generate_token
from src.core.db.session import redis_email, redis_pw


smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
if settings.SMTP_TLS:
    smtp_options["tls"] = True
if settings.SMTP_USER:
    smtp_options["user"] = settings.SMTP_USER
if settings.SMTP_PASSWORD:
    smtp_options["password"] = settings.SMTP_PASSWORD


def send_mail(subject: str, to: str, text: str, mail_from: str = settings.SMTP_USER):
    message = emails.Message(subject=subject, mail_from=mail_from, text=text)

    response = message.send(to=to, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_email_verificaton_token(to: str):
    valid_token = False
    while not valid_token:
        token = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
        if redis_email.get(token):
            valid_token = False
        else:
            valid_token = True

    redis_email.set(token, to)
    redis_email.expire(token, timedelta(days=7))
    subj = "Verify your email address."
    msg = f"Please use the following code in the application to verify your account: {token}"
    send_mail(subject=subj, to=to, text=msg)


def send_password_reset_token(to: str):
    valid_token = False
    while not valid_token:
        token = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
        if redis_pw.get(token):
            valid_token = False
        else:
            valid_token = True

    redis_pw.set(token, to)
    redis_pw.expire(token, timedelta(days=1))
    subj = "Pictureapp password reset request"
    msg = f"Please use the following code in the application to reset your password: {token}"
    send_mail(subject=subj, to=to, text=msg)