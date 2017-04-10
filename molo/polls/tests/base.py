from django.test import TestCase, Client
from django.contrib.auth.models import User

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import (
    SiteLanguageRelation,
    Languages
)
from molo.polls.models import PollsIndexPage


class BasePollsTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)
        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)
        self.french = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='fr',
            is_active=True)
        self.user = self.login()

        # Get the polls index page
        self.polls_index = PollsIndexPage.objects.child_of(
            self.main).first()

        self.superuser_name = 'test_superuser'
        self.superuser_password = 'password'
        self.superuser = User.objects.create_superuser(
            username=self.superuser_name,
            email='admin@example.com',
            password=self.superuser_password,
            is_staff=True)
        self.client = Client()
