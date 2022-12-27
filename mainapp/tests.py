from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from mainapp.models import News, Course
from authapp.models import User
from mainapp.tasks import send_feedback_to_email
from braniaclms.settings import SELENIUM_DRIVER_PATH_FF

import pickle
from unittest import mock
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail as django_mail
from django.test import Client, TestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestMainPage(TestCase):
    def test_page_open(self):
        path = reverse("mainapp:index")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestNewsPage(TestCase):

    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixutes/001_news.json",
    )

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse("authapp:login")
        self.client_with_auth.post(
            path_auth, data={"username": "superuser", "password": "Superuser"}
        )

    def test_page_open_list(self):
        path = reverse("mainapp:news")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_crete_deny_access(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_crete_by_admin(self):
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = News.objects.count()
        path = reverse("mainapp:news_create")
        self.client_with_auth.post(
            path,
            data={
                "title": "NewTestNews001",
                "preambule": "NewTestNews001",
                "body": "NewTestNews001",
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):

        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data={
                "title": new_title,
                "preambule": news_obj.preamble,
                "body": news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestCoursesWithMock(TestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixutes/002_courses.json",
        "mainapp/fixutes/003_lessons.json",
        "mainapp/fixutes/004_teachers.json",
    )

    def test_page_open_detail(self):
        course_obj = Course.objects.get(pk=2)
        path = reverse("mainapp:courses_detail", args=[course_obj.pk])
        with open(
            "mainapp/fixutes/006_feedback_list_2.bin", "rb"
        ) as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestTaskMailSend(TestCase):
    fixtures = ("authapp/fixtures/001_user_admin.json",)

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = User.objects.first()
        send_feedback_to_email(
            {"user_id": user_obj.id, "message": message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)


class TestCoursesWithMock(TestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixutes/002_courses.json",
        "mainapp/fixutes/003_lessons.json",
        "mainapp/fixutes/004_teachers.json",
    )

    def test_page_open_detail(self):
        course_obj = Course.objects.get(pk=2)
        path = reverse("mainapp:courses_detail", args=[course_obj.pk])
        with open(
            "mainapp/fixutes/006_feedback_list_2.bin", "rb"
        ) as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixutes/001_news.json",
    )

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(
            executable_path=settings.SELENIUM_DRIVER_PATH_FF
        )
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element_by_id("id_username").send_keys("admin")
        self.selenium.find_element_by_id("id_password").send_keys("admin")
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto"))
        )

    def test_create_button_clickable(self):
        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'[href="{path_add}"]')
            )
        )
        print("Trying to click button ...")
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.ID, "id_title"))
        )
        print("Button clickable!")
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 5).until(
        # EC.visibility_of_element_located((By.ID, "id_title111"))
        # )

    def test_pick_color(self):
        path = f"{self.live_server_url}{reverse('mainapp:main_page')}"
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "navbar"))
        )
        try:
            self.assertEqual(
                navbar_el.value_of_css_property("background-color"),
                "rgb(255, 255, 155)",
            )
        except AssertionError:
            with open(
                "var/screenshots/001_navbar_el_scrnsht.png", "wb"
            ) as outf:
                outf.write(navbar_el.screenshot_as_png)
            raise

    def tearDown(self):
        # Close browser
        self.selenium.quit()
        super().tearDown()
