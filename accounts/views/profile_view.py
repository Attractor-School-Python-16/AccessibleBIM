from django.shortcuts import render

from django.views import View

from accounts.models import CustomUser



class ProfileView(View):
    def get(self, request, *args, **kwargs):
        is_moderator = self.request.user.groups.filter(name='moderators').exists()
        context = {
            'is_moderator': is_moderator
        }
        return render(request, 'accounts/profile.html', context)
