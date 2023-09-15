from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from accounts.models import CustomUser
from subscription.forms.subscription_form import SubscriptionForm
from subscription.forms.subscription_user_add_form import SubscriptionUserAddForm
from subscription.models.subscription import SubscriptionModel


class SubscriptionListView(ListView):
    model = SubscriptionModel
    template_name = 'subscription/subscription_list.html'
    context_object_name = 'subscriptions'
    ordering = ("-create_at",)


class SubscriptionCreateView(CreateView):
    template_name = "subscription/subscription_create.html"
    model = SubscriptionModel
    form_class = SubscriptionForm

    def get_success_url(self):
        return reverse("subscription:subscription_detail", kwargs={"pk": self.object.pk})


class SubscriptionDetailView(DetailView):
    model = SubscriptionModel
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_detail.html'


class SubscriptionUpdateView(UpdateView):
    model = SubscriptionModel
    form_class = SubscriptionForm
    context_object_name = 'subscription'
    template_name = 'subscription/subscription_update.html'

    def get_success_url(self):
        return reverse("subscription:subscription_detail", kwargs={"pk": self.object.pk})


class SubscriptionDeleteView(DeleteView):
    model = SubscriptionModel
    template_name = "subscription/subscription_delete.html"
    context_object_name = 'subscription'
    success_url = reverse_lazy("subscription:subscription_list")


class SubscriptionUserListView(ListView):
    model = CustomUser
    template_name = "subscription/subscription_user_list.html"
    context_object_name = 'users'


class SubscriptionUserAddView(DetailView, FormMixin):
    model = CustomUser
    template_name = "subscription/subscription_user_add.html"
    context_object_name = 'user'
    form_class = SubscriptionUserAddForm
    success_url = reverse_lazy("subscription:subscription_users_list")

    def get_context_data(self, **kwargs):
        kwargs['subscriptions'] = SubscriptionModel.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form, *args, **kwargs):
        subscription = form.save(commit=False)
        subscription_pk = subscription
        print(subscription_pk.us_users)
        subscription_pk.us_users.add(self.object.pk)
        # return redirect("topics:detail", pk=topic.pk)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
