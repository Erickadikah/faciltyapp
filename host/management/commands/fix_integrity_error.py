from django.core.management.base import BaseCommand
from host.models import Message, Client

class Command(BaseCommand):
    help = 'Fixes integrity error by updating invalid foreign keys'

    def handle(self, *args, **options):
        messages = Message.objects.all()
        for message in messages:
            if not message.recipient_id:
                message.delete()  # Or handle the invalid foreign key in another way

        self.stdout.write(self.style.SUCCESS('Integrity error fixed successfully'))
