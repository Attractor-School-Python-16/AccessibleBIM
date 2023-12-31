from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyChoices(models.TextChoices):
    USD = 'USD', _("USD")
    RUB = 'RUB', _("RUB")


class CurrencyRateModel(models.Model):
    base_currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, verbose_name='Валюта')
    goal_currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, verbose_name='Валюта')
    rate = models.DecimalField(max_digits=18, decimal_places=8)
    created_at = models.DateTimeField(verbose_name='Cоздано', auto_now_add=True)
    source = models.CharField(max_length=500, verbose_name='Источник')
    timestamp = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return f'{self.base_currency}{self.goal_currency} {self.rate} at {self.created_at}'

    class Meta:
        app_label = 'currency'
        db_table = 'currency_rate'
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курсы валют'
