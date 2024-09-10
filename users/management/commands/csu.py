from users.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="Admin@user.com",
            first_name="Admin",
            last_name="User",
            is_staff=True,
            is_superuser=True,
        )
        user.set_password("admin-user123")
        user.save()
