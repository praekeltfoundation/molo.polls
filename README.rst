Molo polls
=============

.. image:: https://travis-ci.org/praekelt/molo.polls.svg?branch=develop
    :target: https://travis-ci.org/praekelt/molo.polls
    :alt: Continuous Integration

.. image:: https://coveralls.io/repos/praekelt/molo.polls/badge.png?branch=develop
    :target: https://coveralls.io/r/praekelt/molo.polls?branch=develop
    :alt: Code Coverage

.. image:: https://badge.fury.io/py/molo.polls.svg
    :target: http://badge.fury.io/py/molo.polls
    :alt: Pypi Package


A molo module that provides the ability to run polls and surveys.

Installation::

   pip install molo.polls


Django setup::

   INSTALLED_APPS = (
      'molo.polls',
   )

In your urls.py::

   urlpatterns += patterns('',
        url(r'^polls/', include('molo.polls.urls', namespace='molo.polls', app_name='molo.polls')),
   )

In your main.html::

   {% load poll_votings %}

   {% block content %}
      {% poll_page page=language_page %}
   {% endblock %}

In your section page or article page::

   {% load poll_votings %}

   {% block content %}
    {% has_questions self as questions %}
    {% if questions %}
      {% poll_page_in_section page=self %}
    {% endif %}
   {% endblock %}
