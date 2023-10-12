from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.models import CustomUser


class GrantModeratorPanelView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/grant_moderator.html'

    def has_permission(self):
        user = self.request.user
        return user.has_perm('accounts.can_grant_moderator_role')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.exclude(id=self.request.user.id)
        return context


class GrantModerators(PermissionRequiredMixin, View):
    def has_permission(self):
        user = self.request.user
        return user.has_perm('accounts.can_grant_moderator_role')

    def post(self, request):
        try:
            user_ids = request.POST.getlist('users')
            moder_group = Group.objects.get(name='moderators')
            for user_id in user_ids:
                moder_group.user_set.add(user_id)
        except IntegrityError:
            pass
        return redirect('accounts:grant_moderator_panel')


class RemoveModerators(PermissionRequiredMixin, View):
    def has_permission(self):
        user = self.request.user
        return user.has_perm('accounts.can_grant_moderator_role')

    def post(self, request):
        try:
            user_ids = request.POST.getlist('users')
            moder_group = Group.objects.get(name='moderators')
            for user_id in user_ids:
                moder_group.user_set.remove(user_id)
        except IntegrityError:
            pass
        return redirect('accounts:grant_moderator_panel')
