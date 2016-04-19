# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_polls_index(apps, schema_editor):
    from molo.core.models import Main
    from molo.polls.models import Question, FreeTextQuestion, PollsIndexPage
    main = Main.objects.all().first()

    if main:
        polls_index = PollsIndexPage(title='Polls', slug='polls')
        main.add_child(instance=polls_index)
        polls_index.save_revision().publish()

        # Move existing Questions
        for page in Question.objects.all().child_of(main):
            page.move(polls_index, pos='last-child')

        # Move existing FreeTextQuestion
        for page in FreeTextQuestion.objects.all().child_of(main):
            page.move(polls_index, pos='last-child')


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_pollsindexpage'),
    ]

    operations = [
        migrations.RunPython(create_polls_index),
    ]
