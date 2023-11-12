from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models import AbstractModel


class PartnerModel(AbstractModel):
    title = models.CharField(_('partner title'), max_length=50)
    image = models.ImageField(_('partner image'), upload_to='partners')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'partner'
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
