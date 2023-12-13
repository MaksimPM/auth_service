from django.core.management import BaseCommand
from config import settings
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=settings.SUPERUSER_EMAIL,
            first_name=settings.SUPERUSER_FIRST_NAME,
            last_name=settings.SUPERUSER_LAST_NAME,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )

        user.set_password(settings.SUPERUSER_PASSWORD)
        user.save()
        print(f'Администратор {user.first_name} {user.last_name} создан.')
