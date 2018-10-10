from django.test import TestCase, Client
from django.contrib.auth.models import User

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import (
    Main,
    SiteLanguageRelation,
    Languages
)
from molo.polls.models import Choice, PollsIndexPage


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

        self.mk_main2()
        self.main2 = Main.objects.all().last()
        self.language_setting2 = Languages.objects.create(
            site_id=self.main2.get_site().pk)
        self.english2 = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting2,
            locale='en',
            is_active=True)
        self.french2 = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting2,
            locale='fr',
            is_active=True)

        self.polls_index_main2 = PollsIndexPage.objects.child_of(
            self.main2).first()

        self.mk_main2(title='main3', slug='main3', path='4099')
        self.client2 = Client(HTTP_HOST=self.main2.get_site().hostname)

    def make_choice(self, parent, title='yes', language=None):
        choice = Choice(title=title, language=language)
        parent.add_child(instance=choice)
        choice.save_revision().publish()
        return choice
