# tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Message

class MessageSendingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_send_message_view(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('send_message', kwargs={'client_id': self.user2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send_message.html')

        # Test sending a message
        response = self.client.post(reverse('send_message', kwargs={'client_id': self.user2.pk}), {
            'content': 'Test message content',
            'file': '',  # File field can be empty for this test
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Message sent successfully')

        # Verify that the message is saved in the database
        self.assertTrue(Message.objects.filter(sender=self.user1, recipient=self.user2, content='Test message content').exists())
        self.client.logout()