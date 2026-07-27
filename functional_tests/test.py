from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

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
        self.browser.quit
        super().tearDown()

class LoginTest(BaseLiveServerTestCase):
    def test_can_login_with_valid_credentials(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        user_name_input = self.browser.find_element(By.NAME, "username")
        user_password_input = self.browser.find_element(By.NAME, "password")
        subbmit_button = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        user_name_input.send_keys('Tester')
        user_password_input.send_keys('test')
        subbmit_button.click()

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        header_h1 = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn('Witaj Tester', body_text)
        self.assertIn("Horse Owner", header_h1)
        self.assertNotIn("Zaloguj się", body_text)

