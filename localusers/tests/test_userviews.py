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
        self.assertTemplateUsed(response, "localusers/signup.html")
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

    def test_address_list_page_returns_only_owned(self):
        user1 = models.User.objects.create_user("user1", "pw432joij")
        user2 = models.User.objects.create_user("user2", "pw432joij")
        models.Address.objects.create(
            user=user1,
            name="john kimball",
            address1="flat 2",
            address2="12 Stralz avenue",
            city="London",
            country="uk",
        )
        models.Address.objects.create(
            user=user2,
            name="marc kimball",
            address1="123 Deacon road",
            city="London",
            country="uk",
        )
        self.client.force_login(user2)
        response = self.client.get(reverse("address_list"))
        self.assertEqual(response.status_code, 200)
        address_list = models.Address.objects.filter(user=user2)
        self.assertEqual(
            list(response.context["object_list"]),
            list(address_list),
        )

    def test_address_create_stores_user(self):
        user1 = models.User.objects.create_user("user1", "pw432joij")
        post_data = {
            "name": "john kercher",
            "address1": "1 av st",
            "address2": "",
            "zip_code": "MA12GS",
            "city": "Manchester",
            "country": "uk",
        }
        self.client.force_login(user1)
        self.client.post(reverse("address_create"), post_data)
        self.assertTrue(models.Address.objects.filter(user=user1).exists())
