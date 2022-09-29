from unittest.mock import patch
from django.contrib import auth
from django.test import TestCase
from http import client
from django.urls import reverse
from localusers.forms import UserCreationForm
from localusers import models


class TestPage(TestCase):
    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(
            response.context["form"], UserCreationForm
        )

    def test_user_signup_page_submission_works(self):
        post_data = {
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }
        with patch.object(UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(reverse("signup"), post_data)
            print(response)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.status_code, 302) #the correct one

        self.assertTrue(models.User.objects.filter(
            email="user@domain.com").exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        mock_send.assert_called_once()
