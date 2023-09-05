from django.db import models


# from django.urls import reverse


# Create your models here.

class AbstractModel(models.Model):
    pass


class TestBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Название теста')
    questions_qty = models.IntegerField(verbose_name='Количество вопросов')

    # progress_id = models.ForeignKey('progress.Progress', related_name='test_bim', on_delete=models.CASCADE,
    #                            verbose_name='Прогресс теста')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'test_bim'
        verbose_name = 'Тест Bim'
        verbose_name_plural = 'Тесты Bim'


class QuestionBim(AbstractModel):
    title = models.CharField(max_length=100, verbose_name='Вопрос')
    test_bim = models.ForeignKey('test_bim.TestBim', related_name='question_bim', on_delete=models.CASCADE,
                                 verbose_name='Тест Bim')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'question_bim'
        verbose_name = 'Вопрос Bim'
        verbose_name_plural = 'Вопрос Bim'


class AnswerBim(AbstractModel):
    answer = models.CharField(max_length=100, verbose_name='Ответ')
    is_correct = models.BooleanField(verbose_name='Валидация ответа',
                                     choices=[(False, 'Неверный ответ'), (True, 'Верный ответ')],
                                     default=False)
    question_bim = models.ForeignKey('test_bim.QuestionBim',
                                     related_name='answer_bim',
                                     on_delete=models.CASCADE,
                                     verbose_name='Вопрос')

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        db_table = 'answer_bim'
        verbose_name = 'Ответ Bim'
        verbose_name_plural = 'Ответ Bim'


