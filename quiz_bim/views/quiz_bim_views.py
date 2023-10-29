from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from view_breadcrumbs import ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin

from quiz_bim.forms.answer_bim_form import AnswerBimForm
from quiz_bim.forms.question_bim_form import QuestionBimForm
from quiz_bim.models import QuestionBim, AnswerBim
from quiz_bim.models.quiz_bim import QuizBim
from quiz_bim.forms.quiz_bim_form import QuizBimForm

from quiz_bim.validators import validate_answer


class QuizBimListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = QuizBim
    template_name = 'quiz_bim/quiz_bim/quiz_bim_list.html'
    context_object_name = 'tests'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuizBimDetailView(PermissionRequiredMixin, DetailView, FormMixin):
    model = QuizBim
    queryset = QuizBim.objects.all()
    template_name = "quiz_bim/quiz_bim/quiz_bim_detail.html"
    context_object_name = 'test'
    question = None

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        questions = self.object.question_bim.all()
        self.object.questions_qty = questions.count()
        kwargs['answers'] = AnswerBim.objects.all()
        kwargs['questions'] = questions
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.GET.get('question_pk'):
            htmx_form = form.save(commit=False)
            htmx_form.question_bim = get_object_or_404(QuestionBim, pk=self.question)
            error_messages = validate_answer(htmx_form.question_bim, htmx_form.answer, htmx_form.is_correct)
            if error_messages:
                return render(self.request, "quiz_bim/answer_bim/answer_bim_form.html", context={
                    "forms": form,
                    "error_messages": error_messages,
                    "question": htmx_form.question_bim
                })
            htmx_form.save()
            return redirect("quiz_bim:answerbim_htmx_detail", qpk=self.question, apk=htmx_form.id)
        else:
            htmx_form = form.save(commit=False)
            htmx_form.test_bim = self.object
            quiz = self.object
            questions_quantity =  0 if quiz.questions_qty == None else quiz.questions_qty
            questions_quantity += 1
            quiz.questions_qty = questions_quantity
            quiz.save()
            htmx_form.save()
            return redirect("quiz_bim:questionbim_htmx_detail", tpk=self.object.pk, qpk=htmx_form.id)

    def form_invalid(self, form):
        forms = [form]
        if self.question:
            return render(self.request, "quiz_bim/answer_bim/answer_bim_form.html", context={
                "forms": forms,
            })
        else:
            return render(self.request, "quiz_bim/question_bim/question_bim_form.html", context={
                "forms": forms
            })

    def get_form_class(self):
        self.question = self.request.GET.get('question_pk')
        if self.question:
            return AnswerBimForm
        else:
            return QuestionBimForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class QuizBimCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = QuizBim
    form_class = QuizBimForm
    template_name = "quiz_bim/quiz_bim/quiz_bim_create.html"
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("quiz_bim:quizbim_list")

    def form_valid(self, form):
        test = form.save()
        return redirect("quiz_bim:quizbim_detail", test.pk)


class QuizBimUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = QuizBim
    form_class = QuizBimForm
    template_name = 'quiz_bim/quiz_bim/quiz_bim_update.html'
    success_url = reverse_lazy('quiz_bim:quizbim_list')
    context_object_name = 'test'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuizBimDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = QuizBim
    context_object_name = 'test'
    template_name = 'quiz_bim/quiz_bim/quiz_bim_delete.html'
    success_url = reverse_lazy('quiz_bim:quizbim_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser
