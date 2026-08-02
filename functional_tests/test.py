from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
import time

### PREPARE SERVER AND DATABESES ###
class StartTests(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class CreateUSerInDataBase(StartTests):
    def setUp(self):
        super().setUp()
        self.test_user = User.objects.create_user(
            username = 'Tester',
            password = 'test'
        )

class FoundPageItem:
    def __init__(self, browser):
        self.browser = browser

    @property
    def username_input(self):
        return self.browser.find_element(By.ID, "id_username")

    @property
    def password_input(self):
        return self.browser.find_element(By.ID, "id_password")

    @property
    def password_inputs(self):
        password1 = self.browser.find_element(By.ID, "id_password1")
        password2 = self.browser.find_element(By.ID, "id_password2")
        return password1, password2

    @property
    def login_button(self):
        return self.browser.find_element(By.ID, "login_button")

    @property
    def logout_button(self):
        return self.browser.find_element(By.ID, "logout_button")

    @property
    def registration_button(self):
        return self.browser.find_element(By.ID, "registration_button")

    @property
    def body_text(self):
        return self.browser.find_element(By.TAG_NAME, "body").text

    def find_tag(self, tag):
        return self.browser.find_element(By.TAG_NAME, tag).text

### TESTS ###

class NewVisitorTest(StartTests):
    def test_visit_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Horse Owner", self.browser.title)

        header_h1 = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Horse Owner", header_h1)

class LoginTest(CreateUSerInDataBase):
    def test_can_login_with_valid_credentials(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        time.sleep(1)
        elements = FoundPageItem(self.browser)
        
        elements.username_input.send_keys('Tester')
        elements.password_input.send_keys('test')
        elements.login_button.click()

        self.assertIn('Witaj Tester', elements.body_text)
        self.assertIn("Dashboard", elements.find_tag('h1'))
        self.assertNotIn("Zaloguj się", elements.body_text)
        time.sleep(1)

        elements.logout_button.click()
        time.sleep(1)

        self.assertIn("Horse Owner", elements.find_tag('h1'))
        self.assertIn("Zaloguj się", elements.body_text)

        self.browser.get(self.live_server_url + '/dashboard/')
        self.assertNotIn('Witaj Tester', elements.body_text)
        self.assertNotIn("Dashboard", elements.body_text)

class RegisterTest(StartTests):
    def test_signup(self):
        self.browser.get(self.live_server_url + '/accounts/registration/')
        time.sleep(1)
        elements = FoundPageItem(self.browser)
        
        self.assertIn('Zarejestruj się w systemie', elements.find_tag('h2'))

        elements.username_input.send_keys('Tester')
        elements.password_inputs[0].send_keys('haslo')
        elements.password_inputs[1].send_keys('haslo')
        elements.registration_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/accounts/login/')

        elements.username_input.send_keys('Tester')
        elements.password_input.send_keys('haslo')
        elements.login_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + '/dashboard/')

        self.assertIn('Witaj Tester', elements.body_text)

        