from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
import time

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_visit_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Horse Owner", self.browser.title)

        header_h1 = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Horse Owner", header_h1)

class BaseLiveServerTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()

        self.test_user = User.objects.create_user(
            username = 'Tester',
            password = 'test'
        )

        options = webdriver.FirefoxOptions()
        # options.add_argument('_headless')
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LoginTest(BaseLiveServerTestCase):
    def test_can_login_with_valid_credentials(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        user_name_input = self.browser.find_element(By.ID, "id_username")
        user_password_input = self.browser.find_element(By.ID, "id_password")
        login_button = self.browser.find_element(By.ID, "login_button")

        user_name_input.send_keys('Tester')
        user_password_input.send_keys('test')
        login_button.click()

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        header_h1 = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn('Witaj Tester', body_text)
        self.assertIn("Dashboard", header_h1)
        self.assertNotIn("Zaloguj się", body_text)
        time.sleep(1)

        logout_button = self.browser.find_element(By.ID, "logout_button")
        logout_button.click()
        time.sleep(1)
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        header_h1 = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Horse Owner", header_h1)
        self.assertIn("Zaloguj się", body_text)
        self.browser.get(self.live_server_url + '/dashboard/')
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn('Witaj Tester', body_text)
        self.assertNotIn("Dashboard", body_text)

class RegisterTest(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_signup(self):
        self.browser.get(self.live_server_url + '/accounts/registration/')
        time.sleep(1)

        welcome_text = self.browser.find_element(By.TAG_NAME, "h2").text
        user_name_input = self.browser.find_element(By.ID, "id_username")
        user_password1_input = self.browser.find_element(By.ID, "id_password1")
        user_password2_input = self.browser.find_element(By.ID, "id_password2")
        registration_button = self.browser.find_element(By.ID, "registration_button")

        self.assertIn('Zarejestruj się w systemie', welcome_text)

        user_name_input.send_keys('Tester')
        user_password1_input.send_keys('haslo')
        user_password2_input.send_keys('haslo')
        registration_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/accounts/login/')

        user_name_input = self.browser.find_element(By.ID, "id_username")
        user_password_input = self.browser.find_element(By.ID, "id_password")
        login_button = self.browser.find_element(By.ID, "login_button")

        user_name_input.send_keys('Tester')
        user_password_input.send_keys('haslo')
        login_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/dashboard/')

        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Witaj Tester', body_text)

        