from django.test import TestCase
from django.core import mail
from localusers.forms import UserCreationForm


class TestUserForm(TestCase):
    def test_valid_signup_form_sends_email(self):
        form = UserCreationForm(
            {
                'email': 'user@domain.com',
                'password1': 'abcdefabcdef',
                'password2': 'abcdefabcdef'
            }
        )
        self.assertTrue(form.is_valid())
        with self.assertLogs("localusers.forms", level="INFO") as cm:
            form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Welcome to BookTime"
        )
        self.assertGreaterEqual(len(cm.output), 1)
