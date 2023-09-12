from django.urls import reverse_lazy
from django.views.generic import DeleteView

from progress.models import ProgressTest, ProgressTestAnswers
from django.utils import timezone


#функцию нужно вызвать во вьюшке, которая создает возможность прохождения теста для юзера, чтобы функция
#вызывалась после клика на кнопку Начать тест
def create_progress_test(user, test):
    progress_test = ProgressTest.objects.create(user=user, test=test)
    progress_test.save()

    # Большинство тестов рассчитано на 20 минут, поэтому перед проверкой пройден ли тест, подождем 20 минут
    twenty_minutes_later = progress_test.start_time + timezone.timedelta(minutes=20)

    # Только после прошествия 20 минут начинаем проверку "пройден ли тест"
    if timezone.now() > twenty_minutes_later:
        correct_answers_count = ProgressTestAnswers.objects.filter(
            progress_test__user=user,
            progress_test__test=test,
            answer__is_correct=True
        ).count()

        total_questions_count = test.questions_qty

        # Проверяем, пройден ли тест и обновляем объект ProgressTest
        if total_questions_count > 0:
            percentage_correct_answers = (correct_answers_count / total_questions_count) * 100
            if percentage_correct_answers >= 75:
                progress_test.is_passed = True

        progress_test.save()


# end_time запишем после завершения вьюшек тестов - возьмем время клика на кнопку Завершить тест.


class ProgressTestDeleteView(DeleteView):
    model = ProgressTest
    success_url = reverse_lazy('index.html')       #как будет главная админки, нужно поменять путь
    template_name = 'progress_test_delete.html'

