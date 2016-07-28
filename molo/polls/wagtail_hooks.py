from django.conf.urls import url
from molo.polls.admin import QuestionsModelAdmin
from molo.polls.admin_views import QuestionResultsAdminView
from wagtail.wagtailcore import hooks
from wagtailmodeladmin.options import wagtailmodeladmin_register


@hooks.register('register_admin_urls')
def register_question_results_admin_view_url():
    return [
        url(r'polls/question/(?P<parent>\d+)/results/$',
            QuestionResultsAdminView.as_view(),
            name='question-results-admin'),
    ]

wagtailmodeladmin_register(QuestionsModelAdmin)
