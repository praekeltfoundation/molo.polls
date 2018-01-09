from bs4 import BeautifulSoup

from molo.core.models import Main

from molo.polls.tests.base import BasePollsTestCase
from molo.polls.models import (
    PollsIndexPage,
    Question,
)


class TestMultiSitePolls(BasePollsTestCase):

    def test_multi_site_different_polls(self):
        # create poll on site 1
        first_site_poll_text = 'site 1 poll'
        second_site_poll_text = 'site 2 poll'
        question_site1 = Question(title=first_site_poll_text)
        self.polls_index.add_child(instance=question_site1)
        question_site1.save_revision().publish()

        # create poll on site 2
        question_site2 = Question(title=second_site_poll_text)
        self.polls_index_main2.add_child(instance=question_site2)
        question_site2.save_revision().publish()

        # request site 1
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        # check title is there
        self.assertContains(response, first_site_poll_text)
        self.assertNotContains(response, second_site_poll_text)

        # request site 2
        response = self.client2.get('/')
        self.assertEquals(response.status_code, 200)
        # check that site 2 poll is there
        self.assertNotContains(response, first_site_poll_text)
        self.assertContains(response, second_site_poll_text)


class TestDeleteButtonRemoved(BasePollsTestCase):

    def test_delete_btn_removed_for_polls_index_page_in_main(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

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
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

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
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        polls_index_page = PollsIndexPage.objects.first()

        response = self.client.get('/admin/pages/{0}/edit/'
                                   .format(str(polls_index_page.pk)))
        self.assertEquals(response.status_code, 200)

        delete_button = ('<li><a href="/admin/pages/{0}/delete/" '
                         'class="shortcut">Delete</a></li>'
                         .format(str(polls_index_page.pk)))
        self.assertNotContains(response, delete_button, html=True)
