from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        url = reverse('home')
        response =self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Horse Owner')


class LoginAndLogoutTest(TestCase):
    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(
            username = 'Test',
            password = 'test'
        )

    def test_login_redirect_to_user_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': "Test",
            'password': "test"
        })

        self.assertRedirects(response, '/dashboard/')

    def test_logout_post_redirects_to_home(self):
        self.client.login(username='Test', password='test')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_user_is_logged_out_after_redirection(self):
        self.client.login(username='Test', password='test')
        self.client.post(reverse('logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class LoggedInTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user(
            username = 'Test',
            password = 'test'
        )

        self.client.force_login(self.user)


class DashboardTest(LoggedInTestCase):
    def test_dashboard_view_display_user_name(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertContains(response, self.user.username)