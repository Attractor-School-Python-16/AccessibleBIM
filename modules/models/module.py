import os

from django.db import models


def module_upload_to(instance, filename):
    print(instance)
    # module_pk = instance.module.pk
    # if not module_pk:
    #     module_pk = "unknown"
    # return os.path.join('media', str(module_pk), 'video', filename)


class AbstractModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='created_by',
    # verbose_name='Создано', blank=True, null=True)
    # updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='updated_by',
    # verbose_name='Обновлено', blank=True, null=True)

    class Meta:
        abstract = True


class ModuleModel(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название модуля')
    description = models.TextField(max_length=150, null=False, blank=False, verbose_name='Описание модуля')
    image = models.ImageField(null=False, blank=False, upload_to='module', verbose_name='Фото для модуля')

    class Meta:
        db_table = 'module'
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.title}'
