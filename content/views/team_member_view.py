from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from content.forms import TeamForm
from content.models import TeamModel


class ListTeamView(PermissionRequiredMixin, ListView):
    template_name = 'team/team_list.html'
    permission_required = 'content.view_teammodel'
    queryset = TeamModel.objects.order_by('pk')
    context_object_name = 'team'


class AddTeamView(PermissionRequiredMixin, CreateView):
    template_name = 'team/team_create.html'
    model = TeamModel
    form_class = TeamForm
    permission_required = 'content.add_teammodel'
    success_url = reverse_lazy('content:team_list')


class UpdateTeamView(PermissionRequiredMixin, UpdateView):
    template_name = 'team/team_update.html'
    model = TeamModel
    form_class = TeamForm
    permission_required = 'content.change_teammodel'
    success_url = reverse_lazy('content:team_list')


class DeleteTeamView(PermissionRequiredMixin, DeleteView):
    template_name = 'team/team_delete.html'
    model = TeamModel
    permission_required = 'content.delete_teammodel'
    success_url = reverse_lazy('content:team_list')
    context_object_name = 'team'

