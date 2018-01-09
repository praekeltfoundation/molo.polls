from datetime import datetime

from django.utils.formats import date_format

from molo.polls.tests.base import BasePollsTestCase
from molo.polls.models import (
    Choice,
    Question,
    FreeTextQuestion,
    FreeTextVote,
    ChoiceVote,
)


class TestQuestionResultsAdminView(BasePollsTestCase):

    def test_question_appears_in_wagtail_admin(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)

        response = self.client.get(
            '/admin/polls/question/'
        )

        self.assertContains(response, question.title)

    def test_question_results_view(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

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
            '{0},yes,{1}\r\n'
        ).format(
            datetime.today().strftime('%Y-%m-%d'),
            self.superuser_name)

        self.assertContains(response, expected_output)

    def test_freetextquestion_results_view(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

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
            '{0},yeah probably,{1}\r\n'
        ).format(
            datetime.today().strftime('%Y-%m-%d'),
            self.superuser_name)

        self.assertContains(response, expected_output)

    def test_multisite_wagtail_admin(self):

        question = Question(
            title='poll for main1',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)

        question_main2 = Question(
            title='poll for main2',
            allow_multiple_choice=True, show_results=False)
        self.polls_index_main2.add_child(instance=question_main2)

        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        response = self.client.get(
            '/admin/polls/question/'
        )

        self.assertContains(response, question.title)
        self.assertNotContains(response, question_main2.title)

        self.client2.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        response = self.client2.get(
            '/admin/polls/question/'
        )

        self.assertContains(response, question_main2.title)
        self.assertNotContains(response, question.title)
