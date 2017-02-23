from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import SiteLanguage

from molo.polls.models import (Choice, Question, PollsIndexPage)


class ModelsTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.user = self.login()
        self.mk_main()
        # Create Main language
        self.english = SiteLanguage.objects.create(locale='en')
        self.french = SiteLanguage.objects.create(locale='fr')
        # Create polls index page
        self.polls_index = PollsIndexPage(title='Polls', slug='polls')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

    def test_load_polls_in_footer_page(self):
        client = Client()
        client.login(username='superuser', password='pass')

        choice1 = Choice(title='yes')
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()

        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))
        question_fr = Question.objects.get(
            slug='french-translation-of-is-this-a-test')
        question_fr.save_revision().publish()

        response = client.get('/')
        self.assertContains(
            response, '<a href="/polls/7/polls_details/" '
            'class="footer-link">is this a test</a>', html=True)

        response = client.get('/polls/%s/' % question.id)
        self.assertContains(response, "yes")

        self.client.get('/locale/fr/')
        response = self.client.get('/')
        self.assertContains(
            response, '<a href="/polls/%s/polls_details/" '
            'class="footer-link">'
            'French translation of is this a test</a>' % question_fr.id,
            html=True)
