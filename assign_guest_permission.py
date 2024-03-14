from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Assigns the permission to log in as a guest to all users'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Get the content type for the User model
        content_type = ContentType.objects.get_for_model(User)

        # Create the custom permission if it doesn't exist
        permission, created = Permission.objects.get_or_create(
            codename='can_login_as_guest',
            name='Can log in as guest',
            content_type=content_type,
        )

        # Assign the permission to all users who don't already have it
        users_without_permission = User.objects.exclude(user_permissions=permission)
        for user in users_without_permission:
            user.user_permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully assigned the permission to all users'))
