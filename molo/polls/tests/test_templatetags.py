from django.core.urlresolvers import reverse

from molo.polls.tests.base import BasePollsTestCase
from molo.polls.models import (
    Choice,
    Question
)


class TemplateTagTestCase(BasePollsTestCase):

    def test_load_polls_in_footer_page(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        choice1 = Choice(title='yes')
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.add_child(instance=choice1)
        question.save_revision().publish()
        choice1.save_revision().publish()

        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))
        question_fr = Question.objects.get(
            slug='french-translation-of-is-this-a-test')
        question_fr.save_revision().publish()

        response = self.client.get('/')
        self.assertContains(
            response,
            '<a href="/polls/%s/polls_details/" '
            'class="footer-link">is this a test</a>' % question.id,
            html=True)

        response = self.client.get('/polls/%s/' % question.id)
        self.assertContains(response, "yes")

        self.client.get('/locale/fr/')
        response = self.client.get('/')
        self.assertContains(
            response, '<a href="/polls/%s/polls_details/" '
            'class="footer-link">'
            'French translation of is this a test</a>' % question_fr.id,
            html=True)
