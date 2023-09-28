from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
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


class SubscriptionListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = SubscriptionModel
    template_name = 'subscription/subscription_list.html'
    context_object_name = 'subscriptions'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "subscription/subscription_create.html"
    model = SubscriptionModel
    form_class = SubscriptionForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscriptionmodel_list")


class SubscriptionDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = SubscriptionModel
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = SubscriptionModel
    form_class = SubscriptionForm
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscriptionmodel_detail", kwargs={"pk": self.object.pk})


class SubscriptionDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = SubscriptionModel
    template_name = "subscription/subscription_delete.html"
    context_object_name = 'subscription'
    success_url = reverse_lazy("subscription:subscriptionmodel_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUserListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_list.html"
    context_object_name = 'users'
    queryset = CustomUser.objects.all().filter(is_superuser=0)

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

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_button_form()
        self.button_value = self.get_button_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['subscriptions'] = SubscriptionModel.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form, *args, **kwargs):
        subscription = get_object_or_404(SubscriptionModel, pk=self.button_value)
        user = get_object_or_404(CustomUser, pk=self.object.pk)
        user_subscription = UsersSubscription.objects.all().filter(Q(user_id=self.object.pk) & Q(subscription_id=self.button_value))
        if user_subscription:
            user_subscription = get_object_or_404(UsersSubscription,
                                                  (Q(user_id=self.object.pk) & Q(subscription_id=self.button_value)))
            user_subscription.end_time = datetime.now() + timedelta(days=30)
            user_subscription.subscription_id = self.button_value
            user_subscription.is_active = True
            user_subscription.save()
            return redirect('subscription:subscriptionmodel_user_list')
        else:
            UsersSubscription.objects.create(subscription=subscription, user=user, end_time=datetime.now() + timedelta(days=30))
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
        return [("Отключить подписку", reverse("subscription:subscriptionmodel_user_delete", kwargs={'pk': self.object.pk}))]
