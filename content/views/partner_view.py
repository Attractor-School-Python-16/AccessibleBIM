from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from content.forms import PartnerForm
from content.models import PartnerModel


class ListPartnersView(PermissionRequiredMixin, ListView):
    template_name = 'partners/partners_list.html'
    permission_required = 'view_partnermodel'
    queryset = PartnerModel.objects.order_by('pk')
    context_object_name = 'partners'


class AddPartnerView(PermissionRequiredMixin, CreateView):
    template_name = 'partners/partners_create.html'
    model = PartnerModel
    form_class = PartnerForm
    permission_required = 'add_partnermodel'
    success_url = reverse_lazy('content:partners_list')


class UpdatePartnerView(PermissionRequiredMixin, UpdateView):
    template_name = 'partners/partners_update.html'
    model = PartnerModel
    form_class = PartnerForm
    permission_required = 'change_partnermodel'


class DeletePartnerView(PermissionRequiredMixin, DeleteView):
    template_name = 'partners/partners_delete.html'
    model = PartnerModel
    permission_required = 'delete_partnermodel'
