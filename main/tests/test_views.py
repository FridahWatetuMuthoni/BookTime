from http import client
from django.test import TestCase
from django.urls import reverse
from main.forms import ContactForm
from decimal import Decimal
from main import models
from django.contrib import auth

# Create your tests here.
""" 
    We want to make sure that
        • The HTTP status code for this page is 200.
        • The template home.html has been used.
        • The response contains the name of our shop.
    """


class TestPage(TestCase):

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertContains(response, 'BookTime')

    def test_aboutpage(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'BookTime')

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(
            response.context["form"], ContactForm
        )

    # without tags as fillter
    def test_products_page_returns_active(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )

        models.Product.objects.create(
            name="A Tale of Two Cities",
            slug="tale-two-cities",
            price=Decimal("2.00"),
            active=False,
        )

        response = self.client.get(
            reverse("products", kwargs={"tag": "all"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")
        product_list = models.Product.objects.active().order_by('name')
        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    # with tags as fillter
    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        cb.tags.create(name="Open source", slug="opensource")
        models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )
        response = self.client.get(
            reverse("products", kwargs={"tag": "opensource"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = (
            models.Product.objects.active()
            .filter(tags__slug="opensource")
            .order_by("name")
        )

        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_add_to_basket_loggedin_works(self):
        user1 = models.User.objects.create_user("user1@a.com", "pw432joij")
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        w = models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )
        self.client.force_login(user1)
        response = self.client.get(
            reverse("add_to_basket"), {"product_id": cb.id}
        )
        response = self.client.get(
            reverse("add_to_basket"), {"product_id": cb.id}
        )
        self.assertTrue(models.Basket.objects.filter(user=user1).exists())
        self.assertEquals(models.BasketLine.objects.filter(
            basket__user=user1).count(), 1)
        response = self.client.get(
            reverse("add_to_basket"), {"product_id": w.id})
        self.assertEquals(models.BasketLine.objects.filter(
            basket__user=user1).count(), 2)

    def test_add_to_basket_login_merge_works(self):
        user1 = models.User.objects.create_user("user1@a.com", "pw432joij")
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar", slug="cathedral-bazaar", price=Decimal("10.00"),)
        w = models.Product.objects.create(
            name="Microsoft Windows guide", slug="microsoft-windows-guide", price=Decimal("12.00"),)
        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(basket=basket, product=cb, quantity=2)
        response = self.client.get(
            reverse("add_to_basket"), {"product_id": w.id})
        response = self.client.post(
            reverse("login"), {"email": "user1@a.com", "password": "pw432joij"},)
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        self.assertTrue(models.Basket.objects.filter(user=user1).exists())
        basket = models.Basket.objects.get(user=user1)
        self.assertEquals(basket.count(), 3)
