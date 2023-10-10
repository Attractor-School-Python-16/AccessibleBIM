from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from view_breadcrumbs import ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin

from quiz_bim.forms.question_bim_form import QuestionBimForm
from quiz_bim.models import QuestionBim
from quiz_bim.models.quiz_bim import QuizBim
from quiz_bim.forms.quiz_bim_form import QuizBimForm


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
    form_class = QuestionBimForm
    queryset = QuizBim.objects.all()
    template_name = "quiz_bim/quiz_bim/quiz_bim_detail.html"
    context_object_name = 'test'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        questions = self.object.question_bim.all()
        kwargs['questions'] = questions
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        question = form.save(commit=False)
        question.test_bim = self.object
        question.save()
        return redirect("quiz_bim:questionbim_htmx_detail", tpk=self.object.pk, qpk=question.id)

    def form_invalid(self, form):
        forms = [form]
        return render(self.request, "partials/question_form.html", context={
            "forms": forms
        })

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


class QuestionBimFormCreateView(PermissionRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            forms = QuestionBimForm()
        else:
            forms = []
            for i in range(0, int(pk)):
                forms.append(QuestionBimForm())
        context = {
            'forms': forms
        }
        return render(request, "partials/question_form.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuestionBimFormDetailView(PermissionRequiredMixin, View):
    def get(self, request, tpk, qpk, *args, **kwargs):
        question = get_object_or_404(QuestionBim, id=qpk)
        context = {
            'question': question
        }
        return render(request, "partials/question_detail.html", context)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class QuestionBimFormUpdateView(PermissionRequiredMixin, View, FormMixin):
    form = None

    def get(self, request, tpk, qpk, *args, **kwargs):
        question = QuestionBim.objects.get(id=qpk)
        form = QuestionBimForm(request.POST or None, instance=question)
        context = {
            "forms": form,
            "question": question
        }
        return render(request, "partials/question_form.html", context)

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
            return render(request, "partials/question_form.html", context)


class QuestionBimFormDeleteView(View):
    def post(self, request, *args, **kwargs):
        question = QuestionBim.objects.get(id=kwargs['qpk'])
        if request.method == "POST":
            question.delete()
            return HttpResponse("")

        return HttpResponseNotAllowed(
            [
                "POST",
            ]
        )

# def delete_book(request, pk):
# book = get_object_or_404(Book, id=pk)
#
# if request.method == "POST":
#     book.delete()
#     return HttpResponse("")
#
# return HttpResponseNotAllowed(
#     [
#         "POST",
#     ]
# )
