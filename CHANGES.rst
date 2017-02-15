CHANGE LOG
==========

3.1.0
-----
- Removed ability to delete Polls IndexPage in the Admin UI

3.0.1
-----
- Updated templates in order to reflect styling changes in modeladmin

3.0.0
-----
- Removed dependency on wagtailmodeladmin

Backwards incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Removed use of ``wagtailmodeladmin``: use ``wagtail.contrib.modeladmin`` instead
- ``{% load wagtailmodeladmin_tags %}`` has been replaced by ``{% load modeladmin_tags %}``

NOTE: This release is not compatible with molo versions that are less than 4.0

2.2.1
-----
- Add polls permissions to groups

2.2.1
-----
- Return None if there is no question

2.2.0
-----
- Add support for hiding untranslated content

2.1.0
-----
- Added Polls view to Wagtail Admin

2.0.3
-----

- pinned molo.core to version 3

2.0.2
-----

- Changed molo.core version to 3.0rc8

2.0.1
-----

- Restructured polls to introduce index page

NOTE: This release is not compatible with molo versions that are less than 3.0

2.0.0
-----

- Added multi-language support

Backwards incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- deprecated use of ``LanguagePage``: all pages are now direct children of ``Main`` (use ``SiteLanguage`` for multilanguage support)
- deprecated use of ``question.choices``: use the template tag ``{% load_choices_for_poll_page question as choices %}``


NOTE: This release is not compatible with molo versions that are less than 3.0

1.0.1
-----
- Fixed the issue with not previewing a question page in wagtail

1.0.0
-----
- Initial commit, migrated from `praekelt/molo-tuneme`_


.. _`praekelt/molo-tuneme`: https://github.com/praekelt/molo-tuneme
