from django.db import models


# Create your models here.
class AbstractModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='created_by',
    # verbose_name='Создано', blank=True, null=True)
    # updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='updated_by',
    # verbose_name='Обновлено', blank=True, null=True)

    class Meta:
        abstract = True
