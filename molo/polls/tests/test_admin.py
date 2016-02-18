from molo.polls.models import (Choice, Question, FreeTextQuestion)
from django.test import TestCase
from django.contrib.auth.models import User
from molo.core.models import LanguagePage, Main
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailcore.models import Site, Page
from django.test.client import Client
from django.core.urlresolvers import reverse
from molo.polls.admin import QuestionAdmin, download_as_csv

import datetime


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')
        # Create page content type
        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Create root page
        Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )

        main_content_type, created = ContentType.objects.get_or_create(
            model='main', app_label='core')

        # Create a new homepage
        main = Main.objects.create(
            title="Main",
            slug='main',
            content_type=main_content_type,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )
        main.save_revision().publish()

        self.english = LanguagePage(
            title='English',
            code='en',
            slug='english')
        main.add_child(instance=self.english)
        self.english.save_revision().publish()

        # Create a site with the new homepage set as the root
        Site.objects.all().delete()
        self.site = Site.objects.create(
            hostname='localhost', root_page=main, is_default_site=True)

    def test_download_csv_question(self):
        # make choices
        choice1 = Choice(title='yes')
        choice2 = Choice(title='no')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='tester', password='tester')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',tester,'
                           '"yes,no"\r\n')
        self.assertEquals(str(response), expected_output)

    def test_choice_short_name(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        choice2 = Choice(title='no', short_name='n')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        question.add_child(instance=choice2)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='tester', password='tester')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',tester,'
                           '"y,n"\r\n')
        self.assertEquals(str(response), expected_output)

    def test_choice_short_name_single_choice(self):
        # make choices
        choice1 = Choice(title='yes', short_name='y')
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.english.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        # make a vote
        client = Client()
        client.login(username='tester', password='tester')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',tester,'
                           'y\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_csv_free_text_question(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.english.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='tester', password='tester')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nis this a test,' + date + ',tester,'
                           'this is an answer\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_csv_free_text_question_short_name(self):
        question = FreeTextQuestion(
            title='is this a test', short_name='short')
        self.english.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='tester', password='tester')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = download_as_csv(QuestionAdmin(Question, self.site),
                                   None,
                                   Question.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=questions-' + date +
                           '.csv\r\n\r\n'
                           'title,date_submitted,user,answer'
                           '\r\nshort,' + date + ',tester,'
                           'this is an answer\r\n')
        self.assertEquals(str(response), expected_output)
