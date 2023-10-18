from django import template
from currency.models import CurrencyRateModel

register = template.Library()


@register.simple_tag
def currency_price(price, lang):
    if lang == 'ru':
        currency_rate = CurrencyRateModel.objects.filter(base_currency='USD', goal_currency='RUB').\
            order_by('timestamp').last()
        new_price = change_currency(price, currency_rate.rate)
        return f"{new_price} RUB"
    else:
        return f"{price} USD"


def change_currency(price, currency_rate):
    print(price)
    exact_price = price * currency_rate
    if exact_price % 1 != 0:
        rounded_price = exact_price // 1 + 1
    else:
        rounded_price = exact_price
    if rounded_price % 10 != 0:
        rounded_price = rounded_price - rounded_price % 10 + 10
    return rounded_price
