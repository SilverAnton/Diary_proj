from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="mock_user@test.com",
            first_name="New",
            last_name="User",
        )
        user.set_password("password123_mock_user")
        user.save()
