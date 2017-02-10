from django.test import TestCase

from molo.polls.models import PollsIndexPage

from molo.core.models import SiteLanguage, Main
from molo.core.tests.base import MoloTestCaseMixin

from bs4 import BeautifulSoup


class TestDeleteButtonRemoved(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.english = SiteLanguage.objects.create(locale='en')

        self.login()

        # Create polls index page
        self.polls_index = PollsIndexPage(
            title='Security Questions',
            slug='security-questions')
        self.main.add_child(instance=self.polls_index)
        self.polls_index.save_revision().publish()

    def test_delete_btn_removed_for_polls_index_page_in_main(self):

        main_page = Main.objects.first()
        response = self.client.get('/admin/pages/{0}/'
                                   .format(str(main_page.pk)))
        self.assertEquals(response.status_code, 200)

        polls_index_page_title = (
            PollsIndexPage.objects.first().title)

        soup = BeautifulSoup(response.content, 'html.parser')
        index_page_rows = soup.find_all('tbody')[0].find_all('tr')

        for row in index_page_rows:
            if row.h2.a.string == polls_index_page_title:
                self.assertTrue(row.find('a', string='Edit'))
                self.assertFalse(row.find('a', string='Delete'))

    def test_delete_button_removed_from_dropdown_menu(self):
        polls_index_page = PollsIndexPage.objects.first()

        response = self.client.get('/admin/pages/{0}/'
                                   .format(str(polls_index_page.pk)))
        self.assertEquals(response.status_code, 200)

        delete_link = ('<a href="/admin/pages/{0}/delete/" '
                       'title="Delete this page" class="u-link '
                       'is-live ">Delete</a>'
                       .format(str(polls_index_page.pk)))
        self.assertNotContains(response, delete_link, html=True)

    def test_delete_button_removed_in_edit_menu(self):
        polls_index_page = PollsIndexPage.objects.first()

        response = self.client.get('/admin/pages/{0}/edit/'
                                   .format(str(polls_index_page.pk)))
        self.assertEquals(response.status_code, 200)

        delete_button = ('<li><a href="/admin/pages/{0}/delete/" '
                         'class="shortcut">Delete</a></li>'
                         .format(str(polls_index_page.pk)))
        self.assertNotContains(response, delete_button, html=True)
