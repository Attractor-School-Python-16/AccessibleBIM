from django.db import models
from django.utils.translation import gettext_lazy as _

from subscription.models.subscription import AbstractModel


class Company(AbstractModel):
    title = models.CharField(_('company_title'), max_length=150, null=False, blank=False)
    pin = models.IntegerField(_('company_pin'), max_length=15, null=True, blank=True)
    # country = models.ForeignKey()
    # type_corp = models.ForeignKey()

    def __str__(self):
        return f'{self.pk}. {self.title}'

    class Meta:
        app_label = 'accounts'
        # unique_together = ('country', 'pin',)
