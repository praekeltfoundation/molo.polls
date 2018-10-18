from django.core.urlresolvers import reverse

from molo.polls.tests.base import BasePollsTestCase
from molo.polls.models import (
    Choice,
    Question,
    FreeTextQuestion,
    FreeTextVote,
    ChoiceVote,
)


class TranslationTestCase(BasePollsTestCase):

    def test_translated_question_exists(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        question = Question(title='is this a test', language=self.english)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))
        page = Question.objects.get(
            slug='french-translation-of-is-this-a-test')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[self.polls_index.id]))
        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_translated_choice_exists(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        question = Question(title='is this a test', language=self.english)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        choice1 = self.make_choice(parent=question, language=self.english)
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[question.id]))
        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_votes_stored_against_main_language_question(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        question = Question(title='is this a test', language=self.english)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        choice1 = self.make_choice(parent=question, language=self.english)
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        self.client.post(reverse('molo.polls:vote',
                                 kwargs={'question_id': question.id}),
                         {'choice': choice1.id})

        vote = ChoiceVote.objects.all().first()
        self.assertEqual(vote.choice.all().first().id, choice1.id)

    def test_user_not_allow_to_vote_in_other_languages_once_voted(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        question = Question(title='is this a test', language=self.english)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        choice1 = self.make_choice(parent=question, language=self.english)
        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        page = Choice.objects.get(
            slug='french-translation-of-yes')
        page.save_revision().publish()

        self.client.post(reverse('molo.polls:vote',
                                 kwargs={'question_id': question.id}),
                         {'choice': choice1.id})

        response = self.client.get('/')
        self.assertContains(response, 'Show Results')

        response = self.client.get('/locale/fr/')
        response = self.client.get('/')
        self.assertContains(response, 'Show Results')

    def test_translated_free_text_question_exists(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )
        question = FreeTextQuestion(title='what is this')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))

        page = FreeTextQuestion.objects.get(
            slug='french-translation-of-what-is-this')
        page.save_revision().publish()

        response = self.client.get(reverse(
            'wagtailadmin_explore', args=[self.polls_index.id]))

        self.assertContains(response,
                            '<a href="/admin/pages/%s/edit/"'
                            % page.id)

    def test_free_text_question_reply_stored_against_main_language(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )
        question = FreeTextQuestion(title='what is this')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))

        page = FreeTextQuestion.objects.get(
            slug='french-translation-of-what-is-this')
        page.save_revision().publish()

        self.client.post(
            reverse(
                'molo.polls:free_text_vote',
                kwargs={'question_id': page.id}),
            {'answer': 'A test free text question '})
        answer = FreeTextVote.objects.all().first()
        self.assertEquals(answer.question.id, question.id)
