import datetime

from django.core.urlresolvers import reverse

from molo.polls.admin import QuestionAdmin, download_as_csv
from molo.polls.models import (
    Choice,
    Question,
    FreeTextQuestion,
)
from molo.polls.tests.base import BasePollsTestCase


class AdminTestCase(BasePollsTestCase):

    def test_download_csv_question(self):
        # make choices
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        self.client.post(
            reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
            {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = (('title,date_submitted,user,answer'
                            '\r\nis this a test,{0},{1},'
                            '"yes,no"\r\n').format(
                                date,
                                self.superuser_name))

        self.assertContains(response, expected_output)

    def test_choice_short_name(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        choice2 = Choice(title='no', short_name='n')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        self.client.post(
            reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
            {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = (('title,date_submitted,user,answer'
                            '\r\nis this a test,{0},{1},'
                            '"y,n"\r\n').format(
                                date,
                                self.superuser_name))
        self.assertContains(response, expected_output)

    def test_choice_short_name_single_choice(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        # make a vote
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        self.client.post(
            reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
            {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = (('title,date_submitted,user,answer'
                            '\r\nis this a test,{0},{1},'
                            'y\r\n').format(
                                date,
                                self.superuser_name))
        self.assertContains(response, expected_output)

    def test_download_csv_free_text_question(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )
        response = self.client.get('/')
        self.assertContains(response, 'is this a test')

        self.client.post(
            reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
            {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = (('title,date_submitted,user,answer'
                            '\r\nis this a test,{0},{1},'
                            'this is an answer\r\n').format(
                                date,
                                self.superuser_name))
        self.assertContains(response, expected_output)

    def test_download_csv_free_text_question_short_name(self):
        question = FreeTextQuestion(
            title='is this a test', short_name='short')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )
        response = self.client.get('/')
        self.assertContains(response, 'is this a test')

        self.client.post(
            reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
            {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = (('title,date_submitted,user,answer'
                            '\r\nshort,{0},{1},'
                            'this is an answer\r\n').format(
                                date,
                                self.superuser_name))
        self.assertContains(response, expected_output)

    def test_multisite_download_csv_question(self):
        # make choices
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        # make a question
        question = Question(
            title='poll for main1',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        self.client.post(
            reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
            {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = self.client.get(
            ('/admin/polls/question/{0}/'
             'results/?action=download').format(question.pk))

        date = str(datetime.datetime.now().date())
        expected_output = (
            'Submission Date,Answer,User\r\n{0},"yes,no",{1}\r\n').format(
                date,
                self.superuser_name)
        self.assertContains(response, expected_output)

        # test seperation on multi-site

        # make choices
        choice1_main2 = Choice(title='yes')
        # make a question
        question_main2 = Question(
            title='poll for main2',
            allow_multiple_choice=True, show_results=False)
        self.polls_index_main2.add_child(instance=question_main2)
        question_main2.add_child(instance=choice1_main2)
        question_main2.save_revision().publish()

        self.client2.login(
            username=self.superuser_name,
            password=self.superuser_password
        )
        self.client2.post(
            reverse('molo.polls:vote',
                    kwargs={'question_id': question_main2.id}),
            {'choice': [choice1_main2.id]})

        expected_output = (
            'Submission Date,Answer,User\r\n{0},yes,{1}\r\n').format(
                date,
                self.superuser_name)

        response = self.client2.get(
            ('/admin/polls/question/{0}/'
             'results/?action=download').format(question_main2.pk))
        self.assertContains(response, expected_output)
