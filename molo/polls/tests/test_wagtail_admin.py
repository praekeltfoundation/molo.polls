import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import SiteLanguage

from molo.polls.models import (Choice, Question, FreeTextQuestion,
                               FreeTextVote, PollsIndexPage)


class TestAdminUserView(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='admin@example.com',
            password='0000',
            is_staff=True)

        self.mk_main()
        # Create Main language
        self.english = SiteLanguage.objects.create(locale='en')
        # Create polls index page
        self.polls_index = PollsIndexPage(title='Polls', slug='polls')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

        self.client = Client()
        self.client.login(username='superuser', password='0000')

    def test_wagtail_admin_poll_view(self):
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)

        response = self.client.get(
            '/admin/modeladmin/polls/question/'
        )

        self.assertContains(response, question.title)

    def test_wagtail_admin_choice_view(self):
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)

        choice1 = Choice(title='yes')
        question.add_child(instance=choice1)
        question.save_revision().publish()

        response = self.client.get(
            '/admin/poll/{0}/results/'.format(question.id)
        )

        self.assertContains(response, choice1.title)

        # test CSV export
        response = self.client.get(
            '/admin/poll/{0}/results/?CSV'.format(question.id)
        )

        expected_output = (
            'votes,title\r\n'
            '0,yes'
        )

        self.assertContains(response, expected_output)

    def test_wagtail_admin_freetext_view(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        vote = FreeTextVote(user=self.superuser,
                            question=question,
                            answer='Test')
        vote.save()

        response = self.client.get(
            '/admin/poll/{0}/results/'.format(question.id)
        )

        self.assertContains(response, vote.answer)

        # test CSV export
        response = self.client.get(
            '/admin/poll/{0}/results/?CSV'.format(question.id)
        )

        date = str(datetime.datetime.now().date())

        expected_output = (
            'answer,submission date,question,user\r\n'
            'Test,{0},is this a test,superuser'.format(date)
        )

        self.assertContains(response, expected_output)
