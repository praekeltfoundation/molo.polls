
from copy import copy

from django import template

from molo.polls.models import Question

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None, page=None):
    context = copy(context)
    context.update({
        'questions': Question.objects.live().child_of(page)
        if page else Question.objects.none()
    })
    return context


@register.inclusion_tag('polls/poll_page_in_section.html',
                        takes_context=True)
def poll_page_in_section(context, pk=None, page=None):
    context = copy(context)
    context.update({
        'questions': Question.objects.live().child_of(page)
        if page else Question.objects.none()
    })
    return context


@register.assignment_tag(takes_context=True)
def has_questions(context, page):
    return Question.objects.live().child_of(page).exists()


@register.assignment_tag(takes_context=True)
def can_vote(context, question):
    request = context['request']
    if hasattr(question, 'freetextquestion'):
        return question.freetextquestion.can_vote(request.user)
    return question.can_vote(request.user)


@register.assignment_tag(takes_context=True)
def user_choice(context, question):
    request = context['request']
    choice = question.user_choice(request.user)
    if choice.all().count() == 1:
        return choice
    else:
        choice_titles = [c.title for c in choice.all()]

        return ", ".join(choice_titles)
