CHANGE LOG
==========

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
