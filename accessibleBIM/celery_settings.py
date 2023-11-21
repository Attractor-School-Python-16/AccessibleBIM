import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accessibleBIM.settings')
app = Celery('accessibleBIM')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# при запуске выходило предупреждение: Celery информирует вас о том,
# что в будущей версии (Celery 6.0 и выше) параметр конфигурации
# broker_connection_retry больше не будет определять поведение
# попыток переподключения к брокеру при запуске. Поэтому необходимо добавить код ниже:
broker_connection_retry_on_startup = True


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
