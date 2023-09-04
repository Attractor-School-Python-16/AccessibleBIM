from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class AbstractModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='Создано',
    #                                blank=True, null=True)
    # updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='Обновлено',
    #                                blank=True, null=True)

    class Meta:
        abstract = True


class Subscription(AbstractModel):
    # course = models.ForeignKey('courses.Course', on_delete=models.PROTECT, related_name='courses', verbose_name='Курс')
    price = models.IntegerField(null=False, blank=False, verbose_name='Цена за курс')
    discount = models.IntegerField(null=True, blank=True, default=0, verbose_name='Скидка на курс')
    end_date = models.DateTimeField(verbose_name='Дата обновления')