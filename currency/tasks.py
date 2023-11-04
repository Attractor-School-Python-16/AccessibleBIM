import requests
from datetime import date

from celery import shared_task
from environ import Env

from currency.models.currency_rate import CurrencyChoices, CurrencyRateModel


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 6, 'countdown': 600})
def get_currency_rates(self):
    source = 'https://openexchangerates.org/api/latest.json'
    app_id = Env().str('OPEN_EXCHANGE_RATES_API_KEY')
    response = requests.get(f'{source}?app_id={app_id}')
    response_json = response.json()
    if response_json.get('error'):
        raise Exception
    rates = response_json.get('rates')
    timestamp = response_json.get('timestamp')
    date_time = date.fromtimestamp(timestamp) if timestamp else None
    if rates and date_time:
        for currency in CurrencyChoices:
            if currency != 'USD':
                rate = rates.get(currency)
                if rate:
                    existing_records = CurrencyRateModel.objects.filter(base_currency='USD', goal_currency=currency,
                                                                        rate=rate, source=source, timestamp=date_time)
                    if not existing_records:
                        record = CurrencyRateModel.objects.create(base_currency='USD', goal_currency=currency,
                                                                  rate=rate, source=source, timestamp=date_time)
                        record.save()
                    return
    raise Exception
