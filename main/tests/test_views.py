from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestPage(TestCase):
    """ 
    We want to make sure that
        • The HTTP status code for this page is 200.
        • The template home.html has been used.
        • The response contains the name of our shop.
    """

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')

    def test_aboutpage(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertContains(response, 'BookTime')
