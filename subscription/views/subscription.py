from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from accounts.models import CustomUser
from subscription.forms.subscription_form import SubscriptionForm
from subscription.forms.subscription_user_add_form import SubscriptionUserAddForm
from subscription.forms.subscription_user_delete_form import SubscriptionUserDeleteForm
from subscription.models.subscription import SubscriptionModel
from subscription.models.user_subscription import UsersSubscription


class SubscriptionListView(PermissionRequiredMixin, ListView):
    model = SubscriptionModel
    template_name = 'subscription/subscription_list.html'
    context_object_name = 'subscriptions'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionCreateView(PermissionRequiredMixin, CreateView):
    template_name = "subscription/subscription_create.html"
    model = SubscriptionModel
    form_class = SubscriptionForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscription_detail", kwargs={"pk": self.object.pk})


class SubscriptionDetailView(PermissionRequiredMixin, DetailView):
    model = SubscriptionModel
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUpdateView(PermissionRequiredMixin, UpdateView):
    model = SubscriptionModel
    form_class = SubscriptionForm
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("subscription:subscription_detail", kwargs={"pk": self.object.pk})


class SubscriptionDeleteView(PermissionRequiredMixin, DeleteView):
    model = SubscriptionModel
    template_name = "subscription/subscription_delete.html"
    context_object_name = 'subscription'
    success_url = reverse_lazy("subscription:subscription_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUserListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_list.html"
    context_object_name = 'users'
    queryset = CustomUser.objects.all().filter(is_superuser=0)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class SubscriptionUserAddView(PermissionRequiredMixin, DetailView, FormMixin):
    model = CustomUser
    template_name = "subscription/subscription_admin/user_add.html"
    context_object_name = 'user'
    form_class = SubscriptionUserAddForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_button_form()
        self.button_value = self.get_button_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['subscriptions'] = SubscriptionModel.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form, *args, **kwargs):
        find_subscription = get_object_or_404(SubscriptionModel, pk=self.button_value)
        user = get_object_or_404(CustomUser, pk=self.object.pk)
        if UsersSubscription.objects.all().filter(Q(user_id=self.object.pk) & Q(subscription_id=self.button_value)):
            user_subscription = get_object_or_404(UsersSubscription,
                                                  (Q(user_id=self.object.pk) & Q(subscription_id=self.button_value)))
            user_subscription.end_time = datetime.now() + timedelta(days=30)
            user_subscription.subscription_id = self.button_value
            user_subscription.is_active = True
            user_subscription.save()
        find_subscription.user_subscription.add(user)
        return redirect('subscription:subscription_users_list')

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


class SubscriptionUserDeleteView(PermissionRequiredMixin, DeleteView):
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
        return redirect('subscription:subscription_users_list')

    def get_delete_form(self):
        return SubscriptionUserDeleteForm(self.request.POST)

    def get_delete_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['delete']
        return None
