from django.core.mail import send_mail
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def send_email_task(user_id, password):
    """
    Рассылает письма пользователям с приветствием при регистрации.
    """
    user = User.objects.get(id=user_id)
    print(f'Приветственное письмо отправлено - {user.email}')
    subject = f'Приветственное письмо!'
    message = f'Привет! \n' \
              f'Добро пожаловать на нашу платформу!\n' \
              f'Твой пароль для входа: {password}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)


@shared_task
def send_password_reset_email(user_id):
    user = User.objects.get(id=user_id)
    print(f'Письмо для сброса пароля отправлено - {user.email}')
    subject = 'Cброс пароля'
    message = f'Перейдите по ссылке для сброса пароля: http://127.0.0.1:8000/recovery/{user.password}/'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
