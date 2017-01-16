from datetime import datetime

from django.contrib.auth.models import User
from django.utils.formats import date_format
from django.test import TestCase, Client
from molo.core.models import SiteLanguage
from molo.core.tests.base import MoloTestCaseMixin
from molo.polls.models import Choice, Question, FreeTextQuestion,\
    FreeTextVote, PollsIndexPage, ChoiceVote


class TestQuestionResultsAdminView(TestCase, MoloTestCaseMixin):
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

    def test_question_appears_in_wagtail_admin(self):
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)

        response = self.client.get(
            '/admin/polls/question/'
        )

        self.assertContains(response, question.title)

    def test_question_results_view(self):
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)

        choice1 = Choice(title='yes')
        question.add_child(instance=choice1)
        choice2 = Choice(title='no')
        question.add_child(instance=choice2)
        question.save_revision().publish()

        choice_vote = ChoiceVote(user=self.superuser, question=question)
        choice_vote.save()
        choice_vote.choice.add(choice1)
        choice1.choice_votes.add(choice_vote)

        response = self.client.get(
            '/admin/polls/question/{0}/results/'.format(question.id)
        )

        expected_headings_html = '<tr><th>Submission Date</th><th>Answer</th>'\
                                 '<th>User</th></tr>'

        expected_data_html = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'\
            .format(
                # this depends on settings.DATE_FORMAT assuming default
                date_format(datetime.today(), 'N j, Y'),
                choice1.title,
                self.superuser.username)

        self.assertContains(response, expected_headings_html, html=True)
        self.assertContains(response, expected_data_html, html=True)

        # test CSV download
        response = self.client.get(
            '/admin/polls/question/{0}/results/?action=download'.format(
                question.id)
        )

        expected_output = (
            'Submission Date,Answer,User\r\n'
            '%s,yes,superuser\r\n' % datetime.today().strftime('%Y-%m-%d')
        )

        self.assertContains(response, expected_output)

    def test_freetextquestion_results_view(self):
        question = FreeTextQuestion(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        free_text_vote = FreeTextVote(user=self.superuser, question=question,
                                      answer='yeah probably')
        free_text_vote.save()

        response = self.client.get(
            '/admin/polls/question/{0}/results/'.format(question.id)
        )

        expected_headings_html = '<tr><th>Submission Date</th><th>Answer</th>'\
                                 '<th>User</th></tr>'

        expected_data_html = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>' \
            .format(
                # this depends on settings.DATE_FORMAT assuming default
                date_format(datetime.today(), 'N j, Y'),
                free_text_vote.answer,
                self.superuser.username)

        self.assertContains(response, expected_headings_html, html=True)
        self.assertContains(response, expected_data_html, html=True)

        # test CSV download
        response = self.client.get(
            '/admin/polls/question/{0}/results/?action=download'.format(
                question.id)
        )

        expected_output = (
            'Submission Date,Answer,User\r\n'
            '%s,yeah probably,superuser\r\n'
            % datetime.today().strftime('%Y-%m-%d')
        )

        self.assertContains(response, expected_output)
