from django.conf.urls import url
from django.core.urlresolvers import reverse
from molo.polls.admin import QuestionAdmin
from molo.polls.admin_views import QuestionResultsAdminView
from molo.polls.models import Question
from wagtail.wagtailcore import hooks
from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register


@hooks.register('register_admin_urls')
def register_question_results_admin_view_url():
    return [
        url(r'polls/question/(?P<parent>\d+)/results/$',
            QuestionResultsAdminView.as_view(),
            name='question-results-admin'),
    ]


class QuestionsModelAdmin(ModelAdmin, QuestionAdmin):
    model = Question
    menu_label = 'Polls'
    menu_icon = 'doc-full'
    add_to_settings_menu = False
    list_display = ('entries', 'live')

    def entries(self, obj, *args, **kwargs):
        url = reverse('question-results-admin', args=(obj.id,))
        return '<a href="%s">%s</a>' % (url, obj)

    entries.allow_tags = True
    entries.short_description = 'Title'


wagtailmodeladmin_register(QuestionsModelAdmin)
