import csv

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from molo.polls.models import (
    Choice, Question, FreeTextVote, ChoiceVote, FreeTextQuestion)
from django .db.models import F
from django.views.generic.edit import FormView
from molo.polls.forms import TextVoteForm, VoteForm, NumericalTextVoteForm
from django.utils.translation import get_language_from_request
from molo.core.utils import get_locale_code


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def poll_results(request, poll_id):
    question = get_object_or_404(Question, pk=poll_id)
    page = question.get_main_language_page()
    qs = Choice.objects.live().child_of(page).filter(
        languages__language__is_main_language=True)
    locale = get_locale_code(get_language_from_request(request))
    choices = [(a.get_translation_for(locale) or a, a) for a in qs]
    total_votes = sum(c.votes for c in qs)
    choice_color = ['orange', 'purple', 'turq']
    index = 0
    for choice, main_choice in choices:
        vote_percentage = 0
        if index >= len(choice_color):
            index = 0
        if main_choice.votes > 0:
            vote_percentage = int(main_choice.votes * 100.0 / total_votes)
        choice.percentage = vote_percentage
        choice.color = choice_color[index]
        index += 1

    context = {
        'question': question,
        'total': total_votes,
        'choices': sorted(
            [c for c, m in choices], key=lambda x: x.percentage, reverse=True)
    }
    return render(request, 'polls/results.html', context,)


class VoteView(FormView):
    form_class = VoteForm
    template_name = 'polls/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            VoteView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')

        question = get_object_or_404(Question, pk=question_id)
        context.update({'question': question})
        return context

    def form_valid(self, form, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        question = question.get_main_language_page().specific
        obj, created = ChoiceVote.objects.get_or_create(
            user=self.request.user,
            question=question,)

        if created:
            selected_choice = form.cleaned_data['choice']
            for choice_pk in selected_choice:
                Choice.objects.filter(
                    pk=choice_pk).update(votes=F('votes') + 1)
                choice = Choice.objects.get(pk=choice_pk)
                obj.choice.add(choice)
                choice.choice_votes.add(obj)
                choice.save()
        return HttpResponseRedirect(
            reverse('molo.polls:results', args=(question_id,)))


class FreeTextVoteView(FormView):
    template_name = 'polls/free_text_detail.html'

    def dispatch(self, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        if question.numerical:
            self.form_class = NumericalTextVoteForm
        else:
            self.form_class = TextVoteForm
        return super(FreeTextVoteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            FreeTextVoteView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        context.update({'question': question})
        return context

    def form_valid(self, form, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        question = question.get_main_language_page().specific
        FreeTextVote.objects.get_or_create(
            user=self.request.user,
            question=question,
            defaults={
                'answer': form.cleaned_data['answer']
            })
        return HttpResponseRedirect(reverse('molo.polls:results',
                                            args=(question.id,)))


class PollResultView(FormView):
    def get_context_data(self, **kwargs):
        kwargs = super(PollResultView, self).get_context_data()
        kwargs['parent'] = self.kwargs['parent']
        return kwargs

    def get(self, request, *args, **kwargs):
        parent = kwargs['parent']
        question = get_object_or_404(Question, pk=parent)
        page = question.get_main_language_page()

        choice_vote = Choice.objects.live().child_of(page).filter(
            languages__language__is_main_language=True)

        free_text_votes = FreeTextVote.objects.filter(question_id=parent)

        results = choice_vote if choice_vote else free_text_votes

        data_rows = []
        data_headings = []

        def to_dict(instance, include=None):
            opts = instance._meta
            data = {}
            for f in opts.get_fields():
                if f.name in include:
                    data[f.name] = f.value_from_object(instance)
                    if 'user' in data:
                        data['user'] = instance.user.username
                    if 'question' in data:
                        data['question'] = instance.question

            return data

        for result in results:
            model_data = to_dict(result, include=['question', 'answer',
                                                  'user', 'submission_date',
                                                  'title', 'votes'])

            data_rows.append({
                "fields": model_data.values()
            })

            data_headings = model_data.keys()

            data_headings = [field.replace('_', ' ') for field
                             in data_headings]

        context = {
            'page_title': page.title,
            'data_headings': data_headings,
            'data_rows': data_rows
        }

        if 'CSV' in request.GET:
            response = HttpResponse(content_type='text/csv')
            response[
                'Content-Disposition'] = 'attachment; ' \
                                         'filename="{0} results.csv"' \
                .format(page.title)

            writer = csv.writer(response)
            writer.writerow(data_headings)
            for item in data_rows:
                data_row = []
                form_data = item['fields']
                for value in form_data:
                    data_row.append(value)
                writer.writerow(data_row)

            return response

        return render(request, 'admin/model_admin_results_view.html', context)
