from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from quiz_bim.models.quiz_bim import QuizBim
from quiz_bim.forms.quiz_bim_form import QuizBimForm


class QuizBimListView(ListView):
    model = QuizBim
    template_name = 'quiz_bim/quiz_bim/quiz_bim_list.html'
    context_object_name = 'tests'


class QuizBimDetailView(DetailView):
    queryset = QuizBim.objects.all()
    template_name = "quiz_bim/quiz_bim/quiz_bim_detail.html"
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        questions = self.object.question_bim.all()
        kwargs['questions'] = questions
        return super().get_context_data(**kwargs)


class QuizBimCreateView(CreateView):
    form_class = QuizBimForm
    template_name = "quiz_bim/quiz_bim/quiz_bim_create.html"

    def get_success_url(self):
        return reverse("quiz_bim:test_detail", kwargs={"pk": self.object.pk})


class QuizBimUpdateView(UpdateView):
    model = QuizBim
    form_class = QuizBimForm
    template_name = 'quiz_bim/quiz_bim/quiz_bim_update.html'
    success_url = reverse_lazy('quiz_bim:tests_list')
    context_object_name = 'test'


class QuizBimDeleteView(DeleteView):
    model = QuizBim
    context_object_name = 'test'
    template_name = 'quiz_bim/quiz_bim/quiz_bim_delete.html'
    success_url = reverse_lazy('quiz_bim:tests_list')


