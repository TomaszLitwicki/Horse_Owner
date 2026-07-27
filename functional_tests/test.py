from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    