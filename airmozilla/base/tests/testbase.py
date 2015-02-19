import os
import shutil

from nose.plugins.skip import SkipTest
from selenium import webdriver

from django.test import TestCase, LiveServerTestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File


class DjangoTestCase(TestCase):

    def shortDescription(self):
        return None

    def tearDown(self):
        assert os.path.basename(settings.MEDIA_ROOT).startswith('testmedia')
        if os.path.isdir(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

        super(DjangoTestCase, self).tearDown()

    def _login(self, username='mary', email='mary@mozilla.com', pwd='secret'):
        user = User.objects.create_user(
            username, email, pwd
        )
        assert self.client.login(username=username, password=pwd)
        return user

    def _attach_file(self, event, image):
        with open(image, 'rb') as f:
            img = File(f)
            event.placeholder_img.save(os.path.basename(image), img)
            assert os.path.isfile(event.placeholder_img.path)

    def _upload_media(self, image_path):
        # make sure the main_image is actually accessible
        if not os.path.isdir(settings.MEDIA_ROOT):
            os.mkdir(settings.MEDIA_ROOT)
        shutil.copy(
            image_path,
            settings.MEDIA_ROOT
        )


class DjangoLiveServerTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if settings.RUN_SELENIUM_TESTS:
            cls.driver = webdriver.Firefox()
            cls.driver.implicitly_wait(30)
            cls.base_url = cls.live_server_url
            cls.driver.set_window_size(1120, 550)
        super(DjangoLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if settings.RUN_SELENIUM_TESTS:
            cls.driver.quit()
        super(DjangoLiveServerTestCase, cls).tearDownClass()

    def setUp(self):
        if not settings.RUN_SELENIUM_TESTS:
            raise SkipTest("settings.RUN_SELENIUM_TESTS is set to False")
        super(DjangoLiveServerTestCase, self).setUp()
