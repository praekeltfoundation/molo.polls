import csv
from collections import OrderedDict

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView
from molo.polls.models import Question


class QuestionResultsAdminView(FormView):
    def get(self, request, *args, **kwargs):
        parent = kwargs['parent']
        question = get_object_or_404(Question, pk=parent)

        data_headings = ['Submission Date', 'Answer', 'User']
        data_rows = []

        if hasattr(question, 'freetextquestion'):
            votes = question.freetextquestion.freetextvote_set.all()
        else:
            votes = question.choicevote_set.all()

        for vote in votes:
            data_rows.append(OrderedDict({
                'submission_date': vote.submission_date,
                'answer': vote.answer,
                'user': vote.user
            }))

        action = request.GET.get('action', None)
        if action == 'download':
            return self.send_csv(question.title, data_headings, data_rows)

        context = {
            'page_title': question.title,
            'data_headings': ['Submission Date', 'Answer', 'User'],
            'data_rows': data_rows
        }

        return render(request, 'admin/question_results.html', context)

    def send_csv(self, question_title, data_headings, data_rows):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment;filename="question-{0}-results.csv"'.format(
                question_title)

        writer = csv.writer(response)
        writer.writerow(data_headings)

        for item in data_rows:
            writer.writerow(item.values())

        return response
