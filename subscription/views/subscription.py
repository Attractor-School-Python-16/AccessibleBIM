import uuid
import xmltodict
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.views.generic.edit import FormMixin
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from accounts.models import CustomUser
from subscription.forms.subscription_form import SubscriptionForm
from subscription.forms.subscription_user_add_form import SubscriptionUserAddForm
from subscription.forms.subscription_user_delete_form import SubscriptionUserDeleteForm
from subscription.models.subscription import SubscriptionModel
from subscription.models.user_subscription import UsersSubscription
from django.utils.functional import cached_property
import requests
import hashlib
from django.utils import timezone


class SubscriptionListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = SubscriptionModel
    template_name = 'subscription/subscription_list.html'
    context_object_name = 'subscriptions'
    ordering = ("-create_at",)
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "subscription/subscription_create.html"
    model = SubscriptionModel
    form_class = SubscriptionForm
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscriptionmodel_list")


class SubscriptionDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = SubscriptionModel
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_detail.html'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = SubscriptionModel
    form_class = SubscriptionForm
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_update.html'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscriptionmodel_list")


class SubscriptionDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = SubscriptionModel
    template_name = "subscription/subscription_delete.html"
    context_object_name = 'subscription'
    success_url = reverse_lazy("subscription:subscriptionmodel_list")
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUserListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_list.html"
    context_object_name = 'users'
    queryset = CustomUser.objects.all().filter(is_superuser=0)
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    @cached_property
    def crumbs(self):
        return [("Подписки", reverse("subscription:subscriptionmodel_user_list"))]


class SubscriptionUserAddView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView, FormMixin):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_add.html"
    context_object_name = 'user'
    form_class = SubscriptionUserAddForm
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_button_form()
        self.button_value = self.get_button_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['subscriptions'] = SubscriptionModel.objects.all()
        kwargs['user_subscriptions'] = UsersSubscription.objects.all().filter(user=kwargs['object'].id)
        return super().get_context_data(**kwargs)

    def form_valid(self, form, *args, **kwargs):
        subscription = get_object_or_404(SubscriptionModel, pk=self.button_value)
        user = get_object_or_404(CustomUser, pk=self.object.pk)
        user_subscription = UsersSubscription.objects.all().filter(
            Q(user_id=self.object.pk) & Q(subscription_id=self.button_value))
        if user_subscription:
            user_subscription = get_object_or_404(UsersSubscription,
                                                  (Q(user_id=self.object.pk) & Q(subscription_id=self.button_value)))
            user_subscription.end_time = timezone.now() + timedelta(days=30)
            user_subscription.subscription_id = self.button_value
            user_subscription.is_active = True
            user_subscription.save()
            return redirect('subscription:subscriptionmodel_user_list')
        else:
            UsersSubscription.objects.create(subscription=subscription, user=user,
                                             end_time=timezone.now() + timedelta(days=30))
            return redirect('subscription:subscriptionmodel_user_list')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_button_form(self):
        return SubscriptionUserAddForm(self.request.POST)

    def get_button_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['button']
        return None

    @cached_property
    def crumbs(self):
        return [("Выдать подписку", reverse("subscription:subscriptionmodel_user_add", kwargs={'pk': self.object.pk}))]


class SubscriptionUserDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_delete.html"
    context_object_name = 'user'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        subscription_m2m = get_object_or_404(UsersSubscription, (Q(user_id=self.object.pk) & Q(is_active=True)))
        kwargs['subscription'] = SubscriptionModel.objects.get(pk=subscription_m2m.subscription_id)
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_delete_form()
        self.delete_value = self.get_delete_value()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        user_subscription = get_object_or_404(UsersSubscription,
                                              (Q(user_id=self.object.pk) & Q(subscription_id=self.delete_value)))
        user_subscription.is_active = False
        user_subscription.save()
        return redirect('subscription:subscriptionmodel_user_list')

    def get_delete_form(self):
        return SubscriptionUserDeleteForm(self.request.POST)

    def get_delete_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['delete']
        return None

    @cached_property
    def crumbs(self):
        return [("Отключить подписку",
                 reverse("subscription:subscriptionmodel_user_delete", kwargs={'pk': self.object.pk}))]


class SubscriptionBuyView(PermissionRequiredMixin, View):
    user = get_user_model()

    def has_permission(self):
        current_user = self.user
        return current_user.email_verified

    def get(self, request, *args, **kwargs):
        subscription = get_object_or_404(SubscriptionModel, pk=kwargs['pk'])
        url = "https://api.freedompay.money/init_payment.php"

        pg_merchant_id = 0
        secret_key = '11'

        request = {
            'pg_order_id': '13',  # Номер ордера
            'pg_merchant_id': pg_merchant_id,  # ID Магазина в Freedom Pay
            'pg_amount': subscription.price,  # Цена товара
            'pg_description': f"Подписка за курс '{subscription.course.description}'",  # Описание товара
            'pg_salt': uuid.uuid4().hex,  # Соль (сделал рандомную каждый раз)
            'pg_sig': '',  # Поле куда будем записывать с генерированный ключ
            # 'pg_currency': 'KGZ',               # Валюта (надо уточнить как это работает)
            # 'pg_check_url': 'http://site.kz/check',    # URL для проверки возможности платежа
            # 'pg_result_url': 'http://site.kz/result',    # URL для сообщения о результате платежа
            # 'pg_request_method': 'POST',                   # Метод вызова скриптов магазина Check URL, Result URL, для передачи информации от платежного гейта.
            # 'pg_success_url': 'http://site.kz/success',     # URL редиректа после успешной оплаты
            # 'pg_failure_url': 'http://site.kz/failure',     # URL редиректа после неуспешной оплаты
            # 'pg_success_url_method': 'GET',                  # Метод для отправки пользователя на страницу после успешной оплаты
            # 'pg_failure_url_method': 'GET',                   # Метод для отправки пользователя на страницу после неуспешной оплаты
            # 'pg_state_url': 'http://site.kz/state',            #URL скрипта на сайте магазина, куда перенаправляется покупатель для ожидания ответа от платежной системы.
            # 'pg_state_url_method': 'GET',                       # Метод для отправки пользователя на страницу ожидания
            # 'pg_site_url': 'http://site.kz/return',              # URL сайта магазина для показа покупателю ссылки Применяется для offline ПС (наличные).
            # 'pg_payment_system': 'EPAYWEBKZT',                    # Данный параметр не обязательный так как выбор платежки будет идти от FreedomPay
            # 'pg_lifetime': '86400',                                # Время (в секундах) в течение которого платеж должен быть завершен, в противном случае заказ при проведении платежа FreedomPay откажет платежной системе в проведении
            # 'pg_user_phone': '77777777777',                       # Данный параметр не обязательный так как ввод номер будета идти от FreedomPay
            # 'pg_user_contact_email': 'mail@customer.kz',            # Данный параметр не обязательный так как ввод email будета идти от FreedomPay
            # 'pg_user_ip': '127.0.0.1',                            # Данный параметр не обязательный так как IP FreedomPay возьмет сам
            # 'pg_postpone_payment': '0',                             # Параметр для постоплаты (думаю нам это не понадобиться
            'pg_language': 'ru',  # Для отображения языка в платежной системе
            # 'pg_testing_mode': '1',                                   # Параметр для тестовых платежей (не работает (надо уточнить как это работает))
            # 'pg_user_id': f"{self.user.pk}",
            # ID пользователя в системе заказчика (не работает (надо уточнить как это работает))
            # 'pg_recurring_start': '1',                                # 0 или 1. Рекуррентные платежи. Для использования данного параметра Вам следует обратиться к своему менеджеру.
            # 'pg_recurring_lifetime': '156',                           # Время на продолжении которого мерчант рассчитывает использовать профиль рекуррентных платежей
            # 'pg_receipt_positions': [
            #     {
            #         В случае формирования чеков в Республике Узбекистан, в параметре "name" необходимо передавать
            #         дополнительные значения в определённой последовательности.
            #         Детальную информацию можно найти в разделе "Особенности формирования фискальных чеков"
            #         'name': 'название товара',
            #         'count': '1',
            #         'tax_type': '3',
            #         'price': '900',
            #     }
            # ],
            # 'pg_param1': 'дополнительные данные',
            # 'pg_param2': 'дополнительные данные',
            # 'pg_param3': 'дополнительные данные',
        }

        # Превращаем объект запроса в плоский словарь
        request_for_signature = self.make_sort_dict(request)

        # Генерация подписи
        sorted_request = dict(sorted(request_for_signature.items()))  # Сортировка по ключу
        sorted_request = {
                             'url': 'init_payment.php'} | sorted_request  # Добавление в начало имени скрипта init_payment.php
        fdp_data = ";".join(sorted_request.values()) + secret_key  # Добавление секретного ключа
        request['pg_sig'] = hashlib.md5(fdp_data.encode()).hexdigest()  # Шифруем готовый словарь и добавляем ключ
        response = requests.request("POST", url, data=request)
        dict_response = (xmltodict.parse(response.text)['response'])
        if dict_response['pg_status'] == 'ok':
            return redirect(dict_response['pg_redirect_url'])
        return redirect('subscription:subscriptionmodel_error')

    def make_sort_dict(self, params, parent_name=''):
        start_ditct = {}
        i = 0
        for key, val in params.items():
            i += 1
            name = parent_name + key + f'{i:03d}'
            if isinstance(val, dict):
                start_ditct.update(self.make_sort_dict(val, name))
                continue
            start_ditct[name] = str(val)
        return start_ditct

    # class SubscriptionSuccsesView(APIView):
    #     pass
    #     Нужна будет логика обработки успешности\неуспешности оплаты через API


class SubscriptionErrorView(TemplateView):
    template_name = "subscription/error_payments.html"
