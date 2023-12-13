from django.core.mail import send_mail
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def send_email_task(user_id):
    """
    Рассылает письма пользователям с приветствием при регистрации.
    """
    user = User.objects.get(id=user_id)
    print(f'Письмо отправлено - {user.email}')
    subject = f'Приветственное письмо!'
    message = f'Привет! \n' \
              f'Добро пожаловать на нашу платформу!\n' \
              f'Твой пароль для входа: {user.password}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
