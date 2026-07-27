from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class Home_Page_Test(TestCase):
    def test_home_page_status_code(self):
        url = reverse('home')
        response =self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Horse Owner')
