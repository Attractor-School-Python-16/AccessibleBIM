import os

from django.db import models
from django.utils.translation import gettext_lazy as _


def module_upload_to(instance, filename):
    module = instance.title
    if not module:
        module = "unknown"
    return os.path.join('modules', str(module), 'image', filename)


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
    title = models.CharField(_('Module title'), max_length=50, null=False, blank=False)
    description = models.TextField(_('Module description'), max_length=150, null=False, blank=False)
    image = models.ImageField(_('Module image'), null=False, blank=False, upload_to=module_upload_to)

    class Meta:
        db_table = 'module'
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')

    def __str__(self):
        return f'{self.title}'
