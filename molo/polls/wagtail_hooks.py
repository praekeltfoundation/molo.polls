from django.conf.urls import url
from molo.polls.admin import QuestionsModelAdmin
from molo.polls.admin_views import QuestionResultsAdminView
from wagtail.wagtailcore import hooks
from wagtail.contrib.modeladmin.options import modeladmin_register
from django.contrib.auth.models import User


@hooks.register('register_admin_urls')
def register_question_results_admin_view_url():
    return [
        url(r'polls/question/(?P<parent>\d+)/results/$',
            QuestionResultsAdminView.as_view(),
            name='question-results-admin'),
    ]


modeladmin_register(QuestionsModelAdmin)


@hooks.register('construct_main_menu')
def show_polls_entries_for_users_have_access(request, menu_items):
    if not request.user.is_superuser and not User.objects.filter(
            pk=request.user.pk, groups__name='Moderators').exists():
        menu_items[:] = [
            item for item in menu_items if item.name != 'polls']
