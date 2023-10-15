from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import FormMixin

from quiz_bim.forms.answer_bim_form import AnswerBimForm
from quiz_bim.models import AnswerBim, QuestionBim


class AnswerBimFormCreateView(PermissionRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        question = get_object_or_404(QuestionBim, pk=pk)
        forms = AnswerBimForm()
        # Пока не реализовано (идея такова что приходит pk и данное кол-во форм создается)
        # if not pk:
        #     forms = AnswerBimForm()
        #
        # else:
        #     forms = []
        #     for i in range(0, int(pk)):
        #         forms.append(AnswerBimForm())
        context = {
            'forms': forms,
            'question': question
        }

        return render(request, "quiz_bim/answer_bim/answer_bim_form.html", context)



    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class AnswerBimFormDetailView(PermissionRequiredMixin, View):
    def get(self, request, qpk, apk, *args, **kwargs):
        answer = get_object_or_404(AnswerBim, id=apk)
        context = {
            'answer': answer
        }
        return render(request, "quiz_bim/answer_bim/answer_bim_detail.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class AnswerBimFormUpdateView(PermissionRequiredMixin, View, FormMixin):
    form = None

    def get(self, request, qpk, apk, *args, **kwargs):
        answer = AnswerBim.objects.get(id=apk)
        form = AnswerBimForm(request.POST or None, instance=answer)
        context = {
            "forms": form,
            "answer": answer
        }
        return render(request, "quiz_bim/answer_bim/answer_bim_form.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def post(self, request, *args, **kwargs):
        print(kwargs)
        answer = AnswerBim.objects.get(id=kwargs['apk'])
        form = AnswerBimForm(request.POST or None, instance=answer)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if form.is_valid():
            form.save()
            return redirect("quiz_bim:answerbim_htmx_detail", qpk=kwargs['qpk'], apk=kwargs['apk'])
        else:
            context = {
                "forms": form,
                "answer": answer
            }
            return render(request, "quiz_bim/answer_bim/answer_bim_form.html", context)


class AnswerBimFormDeleteView(View):
    def post(self, request, *args, **kwargs):
        answer = AnswerBim.objects.get(id=kwargs['apk'])
        if request.method == "POST":
            answer.delete()
            return HttpResponse("")

        return HttpResponseNotAllowed(
            [
                "POST",
            ]
        )
