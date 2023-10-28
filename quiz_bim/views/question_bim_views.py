from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import FormMixin

from quiz_bim.forms.question_bim_form import QuestionBimForm
from quiz_bim.models import QuestionBim, AnswerBim, QuizBim


class QuestionBimFormCreateView(PermissionRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        forms = QuestionBimForm()
        # Пока не реализовано (идея такова что приходит pk и данное кол-во форм создается)
        # if not pk:
        #    forms = QuestionBimForm()
        # else:
        #    forms = []
        #    for i in range(0, int(pk)):
        #        forms.append(QuestionBimForm())
        context = {
            'forms': forms
        }
        return render(request, "quiz_bim/question_bim/question_bim_form.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuestionBimFormDetailView(PermissionRequiredMixin, View):
    def get(self, request, tpk, qpk, *args, **kwargs):
        question = get_object_or_404(QuestionBim, id=qpk)
        answers = AnswerBim.objects.all()
        context = {
            'question': question,
            'answers': answers
        }
        return render(request, "quiz_bim/question_bim/question_bim_detail.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuestionBimFormUpdateView(PermissionRequiredMixin, View, FormMixin):
    form = None

    def get(self, request, tpk, qpk, *args, **kwargs):
        question = get_object_or_404(QuestionBim, id=qpk)
        form = QuestionBimForm(request.POST or None, instance=question)
        context = {
            "forms": form,
            "question": question
        }
        return render(request, "quiz_bim/question_bim/question_bim_form.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def post(self, request, *args, **kwargs):
        question = QuestionBim.objects.get(id=kwargs['qpk'])
        form = QuestionBimForm(request.POST or None, instance=question)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if form.is_valid():
            form.save()
            return redirect("quiz_bim:questionbim_htmx_detail", tpk=kwargs['tpk'], qpk=kwargs['qpk'])
        else:
            context = {
                "forms": form,
                "question": question
            }
            return render(request, "quiz_bim/question_bim/question_bim_form.html", context)


class QuestionBimFormDeleteView(View):
    def post(self, request, *args, **kwargs):
        question = get_object_or_404(QuestionBim, id=kwargs['qpk'])
        quiz = get_object_or_404(QuizBim, id=kwargs['tpk'])
        questions_quantity = 0 if quiz.questions_qty == None else quiz.questions_qty
        questions_quantity -= 1
        quiz.questions_qty = questions_quantity
        quiz.save()
        question.delete()
        return HttpResponse("")
