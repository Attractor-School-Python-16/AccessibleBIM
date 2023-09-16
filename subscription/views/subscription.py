from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from subscription.forms.subscription_form import SubscriptionForm
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
