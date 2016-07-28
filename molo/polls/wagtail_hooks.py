from django.conf.urls import url
from django.core.urlresolvers import reverse
from molo.polls.admin import QuestionAdmin
from molo.polls.models import Question
from molo.polls.views import PollResultView
from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register
from wagtail.wagtailcore import hooks


@hooks.register('register_admin_urls')
def register_admin_reply_url():
    return [
        url(r'poll/(?P<parent>\d+)/results/$',
            PollResultView.as_view(),
            name='wagtail-polls-results'),
    ]


class QuestionsModelAdmin(ModelAdmin, QuestionAdmin):
    model = Question
    menu_label = 'Polls'
    menu_icon = 'doc-full'
    add_to_settings_menu = False
    list_display = ('entries', 'live')

    def entries(self, obj, *args, **kwargs):
        url = reverse('wagtail-polls-results', args=(obj.id,))
        return '<a href="%s">%s</a>' % (url, obj)

    entries.allow_tags = True
    entries.short_description = 'Title'


wagtailmodeladmin_register(QuestionsModelAdmin)
