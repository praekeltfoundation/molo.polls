# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 12:29
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


class Migration(migrations.Migration):
    def add_polls_permissions_to_groups(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        try:
            # Django 1.9
            emit_post_migrate_signal(2, False, db_alias)
        except TypeError:
            # Django < 1.9
            try:
                # Django 1.8
                emit_post_migrate_signal(2, False, 'default', db_alias)
            except TypeError:  # Django < 1.8
                emit_post_migrate_signal([], 2, False, 'default', db_alias)

        Group = apps.get_model('auth.Group')
        GroupPagePermission = apps.get_model('wagtailcore.GroupPagePermission')
        PollsIndexPage = apps.get_model('polls.PollsIndexPage')

        # Create groups

        # <- Editors ->
        editor_group = Group.objects.get(name='Editors')

        polls = PollsIndexPage.objects.first()
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=polls,
            permission_type='add',
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=polls,
            permission_type='edit',
        )

        # <- Moderator ->
        moderator_group = Group.objects.get(name='Moderators')

        polls = PollsIndexPage.objects.first()
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=polls,
            permission_type='add',
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=polls,
            permission_type='edit',
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=polls,
            permission_type='publish',
        )


    dependencies = [
        ('polls', '0003_create_polls_index_pages'),
        ('core', '0047_add_core_permissions_to_groups'),
        ('contenttypes', '__latest__'),
        ('sites', '__latest__'),
    ]

    operations = [
        migrations.RunPython(add_polls_permissions_to_groups),
    ]
