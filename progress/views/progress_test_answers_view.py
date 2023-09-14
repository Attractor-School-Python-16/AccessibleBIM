from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from progress.models import ProgressTestAnswers


#функцию нужно вызвать во вьюшке, которая создает возможность прохождения теста для юзера, чтобы функция
#вызывалась после клика на кнопку Далее после ответа на первый вопрос
def create_progress_tests_answers(progress_test, question, answer):
    # Функция создает и сохраняет объект ProgressTestAnswers
    progress_test_answer = ProgressTestAnswers.objects.create(
        progress_test=progress_test,
        question=question,
        answer=answer
    )
    progress_test_answer.save()


# закомментировала создание ProgressTestAnswers, т.к. нам нужно,
# чтобы в БД эти данные появлялись авто-ки после начала теста. Но возможно для статистики это понадобится,
# поэтому пока не удаляю.
# class ProgressTestAnswersCreateView(CreateView):
#     model = ProgressTestAnswers
#     fields = ['progress_test', 'question', 'answer']
#     template_name = "progress_test_answers_create.html"


class ProgressTestAnswersDeleteView(DeleteView):
    model = ProgressTestAnswers
    success_url = reverse_lazy('index.html')       #как будет главная админки, нужно поменять путь
    template_name = 'progress_test_answers_delete.html'    #использовала шаблон от удаления Step



